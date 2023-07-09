"""Module for downloading event data from the game server"""
import binascii
import datetime
import time
from typing import Any

from bcedd import country_code, crypto, game_version, json_file, request


class EventData:
    """Class for downloading event data from the game server
    Lots of this code is taken from the PackPack discord bot: https://github.com/battlecatsultimate/PackPack
    """

    def __init__(
        self,
        file_name: str,
        cc: "country_code.CountryCode",
        gv: "game_version.GameVersion",
        use_old: bool = False,
    ):
        """Initializes the class

        Args:
            file_name (str): File to download
        """
        self.use_old = use_old
        self.aws_access_key_id = "AKIAJCUP3WWCHRJDTPPQ"
        self.aws_secret_access_key = "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"
        self.region = "ap-northeast-1"
        self.service = "s3"
        self.request = "aws4_request"
        self.algorithm = "AWS4-HMAC-SHA256"
        self.domain = "nyanko-events-prd.s3.ap-northeast-1.amazonaws.com"
        self.cc = cc
        self.gv = gv

        if not self.use_old:
            self.domain = "nyanko-events.ponosgames.com"

        self.url = f"https://{self.domain}/battlecats{self.cc.get_patching_code()}_production/{file_name}"

    def to_hex(self, data: "bytes") -> str:
        """Converts bytes to hex

        Args:
            data (bytes): Data to convert

        Returns:
            str: Hex string
        """
        return binascii.hexlify(data).decode("utf-8")

    def get_auth_header(self) -> str:
        """Gets the authorization header

        Returns:
            str: Authorization header
        """
        output = self.algorithm + " "
        output += f"Credential={self.aws_access_key_id}/{self.get_date()}/{self.region}/{self.service}/{self.request}, "
        output += "SignedHeaders=host;x-amz-content-sha256;x-amz-date, "
        signature = self.get_signing_key(self.get_amz_date())
        output += f"Signature={self.to_hex(signature)}"

        return output

    def get_date(self) -> str:
        """Gets the date

        Returns:
            str: Date in YYYYMMDD format
        """
        return datetime.datetime.utcnow().strftime("%Y%m%d")

    def get_amz_date(self) -> str:
        """Gets the amz date

        Returns:
            str: Date in YYYYMMDDTHHMMSSZ format
        """
        return datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    def get_signing_key(self, amz: str) -> "bytes":
        """Gets the signing key for the given amz date

        Args:
            amz (str): Amz date

        Returns:
            bytes: Signing key
        """
        k = "AWS4" + self.aws_secret_access_key
        k_date = self.hmacsha256(k.encode("utf-8"), self.get_date())
        date_region_key = self.hmacsha256(k_date, self.region)
        date_region_service_key = self.hmacsha256(date_region_key, self.service)
        signing_key = self.hmacsha256(date_region_service_key, self.request)

        string_to_sign = self.get_string_to_sign(amz)

        final = self.hmacsha256(signing_key, string_to_sign)
        return final

    def hmacsha256(self, key: "bytes", message: str) -> "bytes":
        """Gets the hmacsha256 of the given key and message

        Args:
            key (bytes): Key
            message (str): Message

        Returns:
            bytes: Hmacsha256 of the given key and message
        """
        return crypto.Hmac(key, crypto.HashAlgorithm.SHA256).get_hmac(
            message.encode("utf-8")
        )

    def get_string_to_sign(self, amz: str) -> str:
        """Gets the string to sign for the given amz date

        Args:
            amz (str): Amz date

        Returns:
            str: String to sign
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
        rq = self.get_canonical_request(amz)
        output += self.to_hex(
            crypto.Hash(crypto.HashAlgorithm.SHA256).get_hash(rq.encode("utf-8"))
        )
        return output

    def get_canonical_request(self, amz: str) -> str:
        """Gets the canonical request for the given amz date

        Args:
            amz (str): Amz date

        Returns:
            str: Canonical request
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
        """Gets the canonical uri for the current url

        Returns:
            str: Canonical uri, e.g. /battlecatsen_production/...
        """
        return self.url.split(self.domain)[1]

    def get_inquiry_code(self) -> str:
        """Gets a new inquiry code.

        Returns:
            str: The inquiry code.
        """
        url = "https://nyanko-backups.ponosgames.com/?action=createAccount&referenceId="
        return request.RequestHandler(url).get().json()["accountId"]

    def generate_signature(self, iq: str, data: str) -> str:
        """Generates a signature from the inquiry code and data.

        Returns:
            str: The signature.
        """
        random_data = crypto.Random.get_hex_string(64)
        key = iq + random_data
        hmac = crypto.Hmac(key.encode("utf-8"), crypto.HashAlgorithm.SHA256)
        signature = hmac.get_hmac(data.encode("utf-8"))

        return random_data + self.to_hex(signature)

    def get_headers(self, iq: str, data: str) -> dict[str, str]:
        """Gets the headers for the request.

        Args:
            iq (str): Inquiry code.
            data (str): Data of the request.

        Returns:
            dict[str, str]: The headers.
        """
        return {
            "accept-enconding": "gzip",
            "connection": "keep-alive",
            "content-type": "application/json",
            "nyanko-signature": self.generate_signature(iq, data),
            "nyanko-timestamp": str(int(time.time())),
            "nyanko-signature-version": "1",
            "nyanko-signature-algorithm": "HMACSHA256",
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-G955F Build/N2G48B)",
        }

    def get_password(self, inquiry_code: str) -> str:
        """Gets the password for the given inquiry code.

        Args:
            inquiry_code (str): The inquiry code.

        Returns:
            str: The password.
        """
        url = "https://nyanko-auth.ponosgames.com/v1/users"
        data = {
            "accountCode": inquiry_code,
            "accountCreatedAt": str(int(time.time())),
            "nonce": crypto.Random.get_hex_string(32),
        }
        data = json_file.JsonFile.from_object(data).to_data_request()
        headers = self.get_headers(inquiry_code, data.decode("utf-8"))
        response = request.RequestHandler(url, headers=headers, data=data).post()
        json_data: dict[str, Any] = response.json()
        payload = json_data.get("payload", {})
        password = payload.get("password", "")
        return password

    def get_client_info(self) -> dict[str, Any]:
        """Gets the client info.

        Returns:
            dict[str, Any]: The client info.
        """
        data = {
            "clientInfo": {
                "client": {
                    "countryCode": self.cc.get_request_code(),
                    "version": self.gv.game_version,
                },
                "device": {
                    "model": "SM-G955F",
                },
                "os": {
                    "type": "android",
                    "version": "9",
                },
            },
            "nonce": crypto.Random.get_hex_string(32),
        }
        return data

    def get_token(self) -> str:
        """Gets the token needed for the request.

        Returns:
            str: The token.
        """
        inquiry_code = self.get_inquiry_code()
        password = self.get_password(inquiry_code)
        url = "https://nyanko-auth.ponosgames.com/v1/tokens"
        data = self.get_client_info()
        data["password"] = password
        data["accountCode"] = inquiry_code
        data = json_file.JsonFile.from_object(data).to_data_request()
        headers = self.get_headers(inquiry_code, data.decode("utf-8"))
        response = request.RequestHandler(url, headers=headers, data=data).post()
        json_data: dict[str, Any] = response.json()
        payload = json_data.get("payload", {})
        token = payload.get("token", "")
        return token

    def make_request(self) -> "request.requests.Response":
        """Makes the request to download the event data

        Returns:
            request.requests.Response: Response
        """
        url = self.url
        headers = {
            "accept-encoding": "gzip",
            "connection": "keep-alive",
            "host": self.domain,
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 9; Pixel 2 Build/PQ3A.190801.002)",
        }
        if self.use_old:
            headers["authorization"] = self.get_auth_header()
            headers["x-amz-content-sha256"] = "UNSIGNED-PAYLOAD"
            headers["x-amz-date"] = self.get_amz_date()
        else:
            url += "?jwt=" + self.get_token()

        return request.RequestHandler(url, headers=headers).get()
