import json
from typing import Any


class JsonFile:
    def __init__(self, data: "bytes"):
        self.json = json.loads(data)

    @staticmethod
    def from_object(js: Any) -> "JsonFile":
        return JsonFile(json.dumps(js).encode("utf-8"))

    @staticmethod
    def from_data(data: "bytes") -> "JsonFile":
        return JsonFile(data)

    def to_data(self) -> "bytes":
        return json.dumps(self.json, indent=4).encode("utf-8")

    def to_data_request(self) -> "bytes":
        return json.dumps(self.json).replace(" ", "").encode("utf-8")

    def get_json(self) -> Any:
        return self.json

    def get(self, key: str) -> Any:
        return self.json[key]

    def set(self, key: str, value: Any) -> None:
        self.json[key] = value

    def __str__(self) -> str:
        return str(self.json)

    def __getitem__(self, key: str) -> Any:
        return self.json[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.json[key] = value
