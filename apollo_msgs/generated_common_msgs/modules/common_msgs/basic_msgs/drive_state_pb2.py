# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: modules/common_msgs/basic_msgs/drive_state.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0modules/common_msgs/basic_msgs/drive_state.proto\x12\rapollo.common\"\xcd\x01\n\x0c\x45ngageAdvice\x12\x43\n\x06\x61\x64vice\x18\x01 \x01(\x0e\x32\".apollo.common.EngageAdvice.Advice:\x0f\x44ISALLOW_ENGAGE\x12\x0e\n\x06reason\x18\x02 \x01(\t\"h\n\x06\x41\x64vice\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x13\n\x0f\x44ISALLOW_ENGAGE\x10\x01\x12\x13\n\x0fREADY_TO_ENGAGE\x10\x02\x12\x10\n\x0cKEEP_ENGAGED\x10\x03\x12\x15\n\x11PREPARE_DISENGAGE\x10\x04')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'modules.common_msgs.basic_msgs.drive_state_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_ENGAGEADVICE']._serialized_start=68
  _globals['_ENGAGEADVICE']._serialized_end=273
  _globals['_ENGAGEADVICE_ADVICE']._serialized_start=169
  _globals['_ENGAGEADVICE_ADVICE']._serialized_end=273
# @@protoc_insertion_point(module_scope)