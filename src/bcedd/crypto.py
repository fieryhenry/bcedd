"""A module for cryptography."""
import enum
import hashlib
import hmac
import random
from typing import Optional


class HashAlgorithm(enum.Enum):
    """An enum representing a hash algorithm."""

    MD5 = enum.auto()
    SHA1 = enum.auto()
    SHA256 = enum.auto()


class Hash:
    """A class to hash data."""

    def __init__(self, algorithm: HashAlgorithm):
        """Initializes a new instance of the Hash class.

        Args:
            algorithm (HashAlgorithm): The hash algorithm to use.
        """
        self.algorithm = algorithm

    def get_hash(
        self,
        data: bytes,
        length: Optional[int] = None,
    ) -> bytes:
        """Gets the hash of the given data.

        Args:
            data (bytes): The data to hash.
            length (Optional[int], optional): The length of the hash. Defaults to None.

        Raises:
            ValueError: Invalid hash algorithm.

        Returns:
            bytes: The hash of the data.
        """
        if self.algorithm == HashAlgorithm.MD5:
            hash = hashlib.md5()
        elif self.algorithm == HashAlgorithm.SHA1:
            hash = hashlib.sha1()
        elif self.algorithm == HashAlgorithm.SHA256:
            hash = hashlib.sha256()
        else:
            raise ValueError("Invalid hash algorithm")
        hash.update(data)
        if length is None:
            return bytes(hash.digest())
        return bytes(hash.digest()[:length])


class Hmac:
    """A class to do HMAC stuff."""

    def __init__(self, key: "bytes", algorithm: HashAlgorithm):
        """Initializes a new instance of the Hmac class.

        Args:
            key (bytes): Key to use.
            algorithm (HashAlgorithm): Algorithm to use.
        """
        self.key = key
        self.algorithm = algorithm

    def get_hmac(self, data: "bytes") -> "bytes":
        """Gets the HMAC of the given data.

        Args:
            data (bytes): The data to get the HMAC of.

        Raises:
            ValueError: Invalid hash algorithm.

        Returns:
            bytes: The HMAC.
        """
        if self.algorithm == HashAlgorithm.MD5:
            hash = hashlib.md5
        elif self.algorithm == HashAlgorithm.SHA1:
            hash = hashlib.sha1
        elif self.algorithm == HashAlgorithm.SHA256:
            hash = hashlib.sha256
        else:
            raise ValueError("Invalid hash algorithm")
        return bytes(hmac.new(self.key, data, hash).digest())


class Random:
    """A class to get random data"""

    @staticmethod
    def get_bytes(length: int) -> bytes:
        """Gets random bytes.

        Args:
            length (int): The length of the bytes.

        Returns:
            bytes: The random bytes.
        """
        return bytes(random.getrandbits(8) for _ in range(length))

    @staticmethod
    def get_alpha_string(length: int) -> str:
        """Gets a random string of the given length.

        Args:
            length (int): The length of the string.

        Returns:
            str: The random string.
        """
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join(random.choice(characters) for _ in range(length))

    @staticmethod
    def get_hex_string(length: int) -> str:
        """Gets a random hex string of the given length.

        Args:
            length (int): The length of the string.

        Returns:
            str: The random string.
        """
        characters = "0123456789abcdef"
        return "".join(random.choice(characters) for _ in range(length))
