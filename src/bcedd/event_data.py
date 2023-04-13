import datetime
import hashlib
import hmac

import requests


class EventData:
    """Class for downloading event data from the Battle Cats servers.
    Some code is taken from the PackPack discord bot:https://github.com/battlecatsultimate/PackPack
    """

    def __init__(self, file_name: str, cc: str):
        """Initializes the EventData class.

        Args:
            file_name (str): File name to download.
            cc (str): Country code to download the file from.
        """
        if cc == "jp":
            cc = ""
        self.aws_access_key_id = "AKIAJCUP3WWCHRJDTPPQ"
        self.aws_secret_access_key = "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"
        self.region = "ap-northeast-1"
        self.service = "s3"
        self.request = "aws4_request"
        self.algorithm = "AWS4-HMAC-SHA256"
        self.domain = "nyanko-events-prd.s3.ap-northeast-1.amazonaws.com"
        self.url = f"https://{self.domain}/battlecats{cc}_production/{file_name}"

    def get_auth_header(self) -> str:
        """Gets the Authorization header for the request.

        Returns:
            str: Authorization header.
        """
        output = self.algorithm + " "
        output += f"Credential={self.aws_access_key_id}/{self.get_date()}/{self.region}/{self.service}/{self.request}, "
        output += f"SignedHeaders=host;x-amz-content-sha256;x-amz-date, "
        signature = self.get_signing_key(self.get_amz_date())
        output += f"Signature={signature.hex()}"

        return output

    def get_date(self) -> str:
        """Gets the date in the format YYYYMMDD.

        Returns:
            str: Date in the format YYYYMMDD.
        """
        return datetime.datetime.utcnow().strftime("%Y%m%d")

    def get_amz_date(self) -> str:
        """Gets the date in the format YYYYMMDDTHHMMSSZ.

        Returns:
            str: Date in the format YYYYMMDDTHHMMSSZ.
        """
        return datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    def get_signing_key(self, amz: str) -> bytes:
        """Gets the signing key for the request.

        Args:
            amz (str): Date in the format YYYYMMDDTHHMMSSZ.

        Returns:
            bytes: Signing key.
        """
        k = ("AWS4" + self.aws_secret_access_key).encode()
        k_date = self.hmacsha256(k, self.get_date())
        date_region_key = self.hmacsha256(k_date, self.region)
        date_region_service_key = self.hmacsha256(date_region_key, self.service)
        signing_key = self.hmacsha256(date_region_service_key, self.request)

        string_to_sign = self.get_string_to_sign(amz)

        final = self.hmacsha256(signing_key, string_to_sign)
        return final

    def hmacsha256(self, key: bytes, message: str) -> bytes:
        """Gets the HMAC-SHA256 of a message.

        Args:
            key (bytes): Key to use for the HMAC-SHA256.
            message (str): Message to get the HMAC-SHA256 of.

        Returns:
            bytes: HMAC-SHA256 of the message.
        """
        return hmac.new(key, message.encode(), hashlib.sha256).digest()

    def get_string_to_sign(self, amz: str) -> str:
        """Gets the string to sign for the request.

        Args:
            amz (str): Date in the format YYYYMMDDTHHMMSSZ.

        Returns:
            str: String to sign.
        """
        output = self.algorithm + "\n"
        output += amz + "\n"
        output += (
            self.get_date()
            + "/"
            + self.region
            + "/"
            + self.service
            + "/"
            + self.request
            + "\n"
        )
        request = self.get_canonical_request(amz)
        output += hashlib.sha256(request.encode()).hexdigest()
        return output

    def get_canonical_request(self, amz: str) -> str:
        """Gets the canonical request for the request.

        Args:
            amz (str): Date in the format YYYYMMDDTHHMMSSZ.

        Returns:
            str: Canonical request.
        """
        output = "GET\n"
        output += self.get_canonical_uri() + "\n" + "\n"
        output += "host:" + self.domain + "\n"
        output += "x-amz-content-sha256:UNSIGNED-PAYLOAD\n"
        output += "x-amz-date:" + amz + "\n"
        output += "\n"
        output += "host;x-amz-content-sha256;x-amz-date\n"
        output += "UNSIGNED-PAYLOAD"
        return output

    def get_canonical_uri(self) -> str:
        """Gets the canonical URI for the request.

        Returns:
            str: Canonical URI.
        """
        return self.url.split(self.domain)[1]

    def make_request(self) -> requests.Response:
        """Makes the request.

        Returns:
            requests.Response: Response from the request.
        """
        url = self.url
        headers = {
            "accept-encoding": "gzip",
            "authorization": self.get_auth_header(),
            "connection": "keep-alive",
            "host": self.domain,
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 9; Pixel 2 Build/PQ3A.190801.002)",
            "x-amz-content-sha256": "UNSIGNED-PAYLOAD",
            "x-amz-date": self.get_amz_date(),
        }

        return requests.get(url, headers=headers)

    def to_file(self, file_path: str):
        """Saves the response to a file.

        Args:
            file_path (str): Path to save the file to.
        """
        response = self.make_request()
        with open(file_path, "wb") as f:
            f.write(response.content)
