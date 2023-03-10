# -*- coding: utf-8 -*-
#
# Copyright © 2023 Saeed Rasooli <saeed.gnu@gmail.com> (ilius)
#
# based on https://github.com/abelcheung/types-lxml
# under Apache License, Version 2.0, January 2004
# http://www.apache.org/licenses/

from typing import (
    AnyStr,
    AsyncContextManager,
    ContextManager,
    Literal,
    Mapping,
    TypeAlias,
)

from lxml.etree import QName, _Element

from .interfaces import Interface

_TextArg: TypeAlias = str | bytes | QName
_TagName: TypeAlias = _TextArg


_OutputMethodArg = Literal[
    "html",
    "text",
    "xml",
    "HTML",
    "TEXT",
    "XML",
]

class IncrementalFileWriter(metaclass=Interface):
    def write_declaration(
        self,
        version: AnyStr | None = ...,
        standalone: bool | None = ...,
        doctype: AnyStr | None = ...,
    ) -> None: ...
    def write_doctype(self, doctype: AnyStr | None) -> None: ...
    def write(
        self,
        *args: AnyStr | _Element,
        with_tail: bool = ...,
        pretty_print: bool = ...,
        method: _OutputMethodArg | None = ...,
    ) -> None: ...
    def flush(self) -> None: ...
    def method(self, method: _OutputMethodArg | None) -> ContextManager[None]: ...
    def element(
        self,
        tag: _TagName,
        attrib: Mapping[str, AnyStr] | None = ...,
        nsmap: dict[str | None, AnyStr] | None = ...,
        method: _OutputMethodArg | None = ...,
        **_extra: AnyStr,
    ) -> ContextManager[None]: ...

class AsyncIncrementalFileWriter(metaclass=Interface):
    async def write_declaration(
        self,
        version: AnyStr | None = ...,
        standalone: bool | None = ...,
        doctype: AnyStr | None = ...,
    ): ...
    async def write_doctype(self, doctype: AnyStr | None) -> None: ...
    async def write(
        self,
        *args: AnyStr | _Element | None,
        with_tail: bool = ...,
        pretty_print: bool = ...,
        method: _OutputMethodArg | None = ...,
    ) -> None: ...
    async def flush(self) -> None: ...
    def method(self, method: _OutputMethodArg | None) -> AsyncContextManager[None]: ...
    def element(
        self,
        tag: _TagName,
        attrib: Mapping[str, AnyStr] | None = ...,
        nsmap: dict[str | None, AnyStr] | None = ...,
        method: _OutputMethodArg | None = ...,
        **_extra: AnyStr,
    ) -> AsyncContextManager[None]: ...

class T_htmlfile(
    IncrementalFileWriter,
    AsyncIncrementalFileWriter,
    ContextManager[IncrementalFileWriter],
    AsyncContextManager[AsyncIncrementalFileWriter],
):
    pass


# T_htmlfile: TypeAlias = AsyncContextManager[AsyncIncrementalFileWriter]

# typing.AsyncContextManager
# is generic version of contextlib.AbstractAsyncContextManager

#T_htmlfile: TypeAlias = Union[
#    ContextManager[IncrementalFileWriter],
#    AsyncContextManager[AsyncIncrementalFileWriter],
#]

