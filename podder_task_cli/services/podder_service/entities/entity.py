import copy
from pathlib import Path
from typing import Dict, Optional

import yaml


class Entity(object):
    _properties = {}

    def __init__(self,
                 data: Optional[Dict] = None,
                 path: Optional[Path] = None,
                 encoding: str = "utf-8"):
        self._property_names = self._properties.keys()
        self._data = data
        self._path = path
        self._encoding = encoding
        if self._data is None and self._path is not None:
            self._load_file()
        self._parse_objects()

    def _load_file(self):
        if self._path.exists():
            self._data = yaml.load(
                self._path.read_text(encoding=self._encoding),
                Loader=yaml.SafeLoader)

    def _parse_objects(self):
        if not isinstance(self._data, dict):
            self._data = {}
        data = copy.deepcopy(self._data)
        for key in self._property_names:
            if isinstance(self._properties[key], list):
                self._data[key] = []
                if key in data and isinstance(data[key], list):
                    for element in data[key]:
                        self._data[key].append(
                            self._properties[key][0](element))
            else:
                if key in data:
                    self._data[key] = self._properties[key](data[key])
                else:
                    self._data[key] = None

    def to_dict(self) -> dict:
        result = {}
        for key in self._property_names:
            if isinstance(self._properties[key], list):
                if isinstance(self._data[key], list):
                    result[key] = []
                    for element in self._data[key]:
                        if hasattr(element, "to_dict"):
                            result[key].append(element.to_dict())
                        else:
                            result[key].append(element)
            else:
                if self._data[key] is not None:
                    if hasattr(self._data[key], "to_dict"):
                        result[key] = self._data[key].to_dict()
                    else:
                        result[key] = self._data[key]

        return result

    def save(self,
             path: Optional[Path] = None,
             encoding: Optional[str] = None):
        data = self.to_dict()
        if path is None:
            if self._path is not None:
                path = self._path
            else:
                return

        if encoding is None:
            encoding = self._encoding

        yaml_data = yaml.dump(data)
        path.write_text(yaml_data, encoding=encoding)

    def __getattr__(self, item):
        if item in self._property_names:
            if item in self._data:
                return self._data[item]
            else:
                return None
        raise AttributeError

    @classmethod
    def load(cls, path: Path):
        return cls(path=path)
