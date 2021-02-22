#!/usr/bin/env python3
__author__ = "WH-2099"
__version__ = "beta"


import json
from collections import UserDict
from typing import IO, Any, AnyStr, Callable, Optional, Protocol, TypeVar, Union

import chardet
import jsonschema
import toml
import xmltodict
import yaml

_T_co = TypeVar("_T_co", covariant=True)


class SupportsRead(Protocol[_T_co]):
    def read(self, __length: int = ...) -> _T_co:
        ...


DEFAULT_CODER = {
    "json": {"encoder": json.dumps, "decoder": json.loads},
    "toml": {"encoder": toml.dumps, "decoder": toml.loads},
    "yaml": {"encoder": yaml.safe_dump, "decoder": yaml.safe_load},
    "xml": {"encoder": xmltodict.unparse, "decoder": xmltodict.parse},
}


def guess_type(string) -> str:
    return


# object 替换 dict
class ConfigDict(UserDict):
    def __init__(self, initialdata: Optional[dict] = None) -> None:
        super().__init__(initialdata)

    def load(
        self,
        fp: SupportsRead[AnyStr],
        type: Optional[str] = None,
        *,
        decoder: Optional[Callable] = None,
        **kwargs: Any
    ) -> "ConfigDict":
        return self.loads(string=fp.read(), type=type, decoder=decoder, **kwargs)

    def loads(
        self,
        string: AnyStr,
        type: Optional[str] = None,
        *,
        decoder: Optional[Callable] = None,
        **kwargs: Any
    ) -> "ConfigDict":

        # 解码 bytes
        if isinstance(string, bytes):
            encoding = chardet.detect(string)["encoding"]
            string = string.decode(encoding)

        if type is None:
            type = guess_type(string)
        else:
            if type not in DEFAULT_CODER:
                raise TypeError("type not supported")
        # xml 文档总是需要根
        if type == "xml" and len(self.data) == 1:
            self.data = {"config": self.data}

        if decoder is None:
            decoder = DEFAULT_CODER[type]["decoder"]

        return self._loads(string=string, decoder=decoder, **kwargs)

    def _loads(self, string: str, decoder: Callable, **kwargs: Any) -> "ConfigDict":
        self.data = decoder(string, **kwargs)
        return self

    def dump(
        self, fp: IO[str], type: str, *, encoder: Optional[Callable] = None, **kwargs
    ) -> None:
        fp.write(self.dumps(type=type, encoder=encoder, **kwargs))

    def dumps(self, type: str, *, encoder: Optional[Callable] = None, **kwargs) -> str:
        if type not in DEFAULT_CODER:
            raise TypeError("type not supported")
        if encoder is None:
            encoder = DEFAULT_CODER[type]["encoder"]

        return self._dumps(encoder=encoder, **kwargs)

    def _dumps(self, encoder: Callable, **kwargs) -> str:
        return encoder(self.data)

    def __getattr__(self, name: str) -> str:
        if name in DEFAULT_CODER:
            return self.dumps(name)
        else:
            raise AttributeError("probably not suporrt this type")


if __name__ == "__main__":

    # TEST
    from pprint import pp

    cd = ConfigDict()
    with open("example.toml") as f:
        cd.load(f, "toml")
        pp(cd)
    for type in ("toml", "json", "yaml"):
        x = getattr(cd, type)
        pp(x)
