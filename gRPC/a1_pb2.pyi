from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Article(_message.Message):
    __slots__ = ["author", "content", "time", "type"]
    class ArticleType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    FASHION: Article.ArticleType
    POLITICS: Article.ArticleType
    SPORTS: Article.ArticleType
    TIME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    author: str
    content: str
    time: int
    type: Article.ArticleType
    def __init__(self, type: _Optional[_Union[Article.ArticleType, str]] = ..., author: _Optional[str] = ..., time: _Optional[int] = ..., content: _Optional[str] = ...) -> None: ...

class ArticleRequest(_message.Message):
    __slots__ = ["article", "name"]
    ARTICLE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    article: Article
    name: str
    def __init__(self, name: _Optional[str] = ..., article: _Optional[_Union[Article, _Mapping]] = ...) -> None: ...

class Client(_message.Message):
    __slots__ = ["address", "name"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    address: str
    name: str
    def __init__(self, name: _Optional[str] = ..., address: _Optional[str] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Response(_message.Message):
    __slots__ = ["status"]
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    FAILURE: Response.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUCCESS: Response.Status
    status: Response.Status
    def __init__(self, status: _Optional[_Union[Response.Status, str]] = ...) -> None: ...

class Server(_message.Message):
    __slots__ = ["address", "name"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    address: str
    name: str
    def __init__(self, name: _Optional[str] = ..., address: _Optional[str] = ...) -> None: ...
