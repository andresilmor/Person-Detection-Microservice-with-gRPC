from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DetectionBox(_message.Message):
    __slots__ = ["point"]
    class PointEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    POINT_FIELD_NUMBER: _ClassVar[int]
    point: _containers.ScalarMap[str, int]
    def __init__(self, point: _Optional[_Mapping[str, int]] = ...) -> None: ...

class PersonDetectionInferenceReply(_message.Message):
    __slots__ = ["filter", "persons"]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PERSONS_FIELD_NUMBER: _ClassVar[int]
    filter: _containers.RepeatedCompositeFieldContainer[DetectionBox]
    persons: _containers.RepeatedCompositeFieldContainer[DetectionBox]
    def __init__(self, persons: _Optional[_Iterable[_Union[DetectionBox, _Mapping]]] = ..., filter: _Optional[_Iterable[_Union[DetectionBox, _Mapping]]] = ...) -> None: ...

class PersonDetectionRequest(_message.Message):
    __slots__ = ["image"]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    image: bytes
    def __init__(self, image: _Optional[bytes] = ...) -> None: ...
