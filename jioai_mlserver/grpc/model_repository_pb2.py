# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: model_repository.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x16model_repository.proto\x12\x1ainference.model_repository"@\n\x16RepositoryIndexRequest\x12\x17\n\x0frepository_name\x18\x01 \x01(\t\x12\r\n\x05ready\x18\x02 \x01(\x08"\xb5\x01\n\x17RepositoryIndexResponse\x12N\n\x06models\x18\x01 \x03(\x0b\x32>.inference.model_repository.RepositoryIndexResponse.ModelIndex\x1aJ\n\nModelIndex\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\r\n\x05state\x18\x03 \x01(\t\x12\x0e\n\x06reason\x18\x04 \x01(\t"I\n\x1aRepositoryModelLoadRequest\x12\x17\n\x0frepository_name\x18\x01 \x01(\t\x12\x12\n\nmodel_name\x18\x02 \x01(\t"\x1d\n\x1bRepositoryModelLoadResponse"K\n\x1cRepositoryModelUnloadRequest\x12\x17\n\x0frepository_name\x18\x01 \x01(\t\x12\x12\n\nmodel_name\x18\x02 \x01(\t"\x1f\n\x1dRepositoryModelUnloadResponse2\xb2\x03\n\x16ModelRepositoryService\x12|\n\x0fRepositoryIndex\x12\x32.inference.model_repository.RepositoryIndexRequest\x1a\x33.inference.model_repository.RepositoryIndexResponse"\x00\x12\x88\x01\n\x13RepositoryModelLoad\x12\x36.inference.model_repository.RepositoryModelLoadRequest\x1a\x37.inference.model_repository.RepositoryModelLoadResponse"\x00\x12\x8e\x01\n\x15RepositoryModelUnload\x12\x38.inference.model_repository.RepositoryModelUnloadRequest\x1a\x39.inference.model_repository.RepositoryModelUnloadResponse"\x00\x62\x06proto3'
)


_REPOSITORYINDEXREQUEST = DESCRIPTOR.message_types_by_name["RepositoryIndexRequest"]
_REPOSITORYINDEXRESPONSE = DESCRIPTOR.message_types_by_name["RepositoryIndexResponse"]
_REPOSITORYINDEXRESPONSE_MODELINDEX = _REPOSITORYINDEXRESPONSE.nested_types_by_name[
    "ModelIndex"
]
_REPOSITORYMODELLOADREQUEST = DESCRIPTOR.message_types_by_name[
    "RepositoryModelLoadRequest"
]
_REPOSITORYMODELLOADRESPONSE = DESCRIPTOR.message_types_by_name[
    "RepositoryModelLoadResponse"
]
_REPOSITORYMODELUNLOADREQUEST = DESCRIPTOR.message_types_by_name[
    "RepositoryModelUnloadRequest"
]
_REPOSITORYMODELUNLOADRESPONSE = DESCRIPTOR.message_types_by_name[
    "RepositoryModelUnloadResponse"
]
RepositoryIndexRequest = _reflection.GeneratedProtocolMessageType(
    "RepositoryIndexRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _REPOSITORYINDEXREQUEST,
        "__module__": "model_repository_pb2"
        # @@protoc_insertion_point(class_scope:inference.model_repository.RepositoryIndexRequest)
    },
)
_sym_db.RegisterMessage(RepositoryIndexRequest)

RepositoryIndexResponse = _reflection.GeneratedProtocolMessageType(
    "RepositoryIndexResponse",
    (_message.Message,),
    {
        "ModelIndex": _reflection.GeneratedProtocolMessageType(
            "ModelIndex",
            (_message.Message,),
            {
                "DESCRIPTOR": _REPOSITORYINDEXRESPONSE_MODELINDEX,
                "__module__": "model_repository_pb2"
                # @@protoc_insertion_point(class_scope:inference.model_repository.RepositoryIndexResponse.ModelIndex)
            },
        ),
        "DESCRIPTOR": _REPOSITORYINDEXRESPONSE,
        "__module__": "model_repository_pb2"
        # @@protoc_insertion_point(class_scope:inference.model_repository.RepositoryIndexResponse)
    },
)
_sym_db.RegisterMessage(RepositoryIndexResponse)
_sym_db.RegisterMessage(RepositoryIndexResponse.ModelIndex)

RepositoryModelLoadRequest = _reflection.GeneratedProtocolMessageType(
    "RepositoryModelLoadRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _REPOSITORYMODELLOADREQUEST,
        "__module__": "model_repository_pb2"
        # @@protoc_insertion_point(class_scope:inference.model_repository.RepositoryModelLoadRequest)
    },
)
_sym_db.RegisterMessage(RepositoryModelLoadRequest)

RepositoryModelLoadResponse = _reflection.GeneratedProtocolMessageType(
    "RepositoryModelLoadResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _REPOSITORYMODELLOADRESPONSE,
        "__module__": "model_repository_pb2"
        # @@protoc_insertion_point(class_scope:inference.model_repository.RepositoryModelLoadResponse)
    },
)
_sym_db.RegisterMessage(RepositoryModelLoadResponse)

RepositoryModelUnloadRequest = _reflection.GeneratedProtocolMessageType(
    "RepositoryModelUnloadRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _REPOSITORYMODELUNLOADREQUEST,
        "__module__": "model_repository_pb2"
        # @@protoc_insertion_point(class_scope:inference.model_repository.RepositoryModelUnloadRequest)
    },
)
_sym_db.RegisterMessage(RepositoryModelUnloadRequest)

RepositoryModelUnloadResponse = _reflection.GeneratedProtocolMessageType(
    "RepositoryModelUnloadResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _REPOSITORYMODELUNLOADRESPONSE,
        "__module__": "model_repository_pb2"
        # @@protoc_insertion_point(class_scope:inference.model_repository.RepositoryModelUnloadResponse)
    },
)
_sym_db.RegisterMessage(RepositoryModelUnloadResponse)

_MODELREPOSITORYSERVICE = DESCRIPTOR.services_by_name["ModelRepositoryService"]
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _REPOSITORYINDEXREQUEST._serialized_start = 54
    _REPOSITORYINDEXREQUEST._serialized_end = 118
    _REPOSITORYINDEXRESPONSE._serialized_start = 121
    _REPOSITORYINDEXRESPONSE._serialized_end = 302
    _REPOSITORYINDEXRESPONSE_MODELINDEX._serialized_start = 228
    _REPOSITORYINDEXRESPONSE_MODELINDEX._serialized_end = 302
    _REPOSITORYMODELLOADREQUEST._serialized_start = 304
    _REPOSITORYMODELLOADREQUEST._serialized_end = 377
    _REPOSITORYMODELLOADRESPONSE._serialized_start = 379
    _REPOSITORYMODELLOADRESPONSE._serialized_end = 408
    _REPOSITORYMODELUNLOADREQUEST._serialized_start = 410
    _REPOSITORYMODELUNLOADREQUEST._serialized_end = 485
    _REPOSITORYMODELUNLOADRESPONSE._serialized_start = 487
    _REPOSITORYMODELUNLOADRESPONSE._serialized_end = 518
    _MODELREPOSITORYSERVICE._serialized_start = 521
    _MODELREPOSITORYSERVICE._serialized_end = 955
# @@protoc_insertion_point(module_scope)