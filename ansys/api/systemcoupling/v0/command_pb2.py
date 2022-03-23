# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: command.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import ansys.api.systemcoupling.v0.variant_pb2 as variant__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='command.proto',
  package='syc',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\rcommand.proto\x12\x03syc\x1a\rvariant.proto\"\x84\x01\n\x0e\x43ommandRequest\x12\x0f\n\x07\x63ommand\x18\x01 \x01(\t\x12*\n\x04\x61rgs\x18\x02 \x03(\x0b\x32\x1c.syc.CommandRequest.Argument\x1a\x35\n\x08\x41rgument\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1b\n\x03val\x18\x02 \x01(\x0b\x32\x0e.utils.Variant\"1\n\x0f\x43ommandResponse\x12\x1e\n\x06result\x18\x01 \x01(\x0b\x32\x0e.utils.Variant2G\n\x07\x43ommand\x12<\n\rInvokeCommand\x12\x13.syc.CommandRequest\x1a\x14.syc.CommandResponse\"\x00\x62\x06proto3'
  ,
  dependencies=[variant__pb2.DESCRIPTOR,])




_COMMANDREQUEST_ARGUMENT = _descriptor.Descriptor(
  name='Argument',
  full_name='syc.CommandRequest.Argument',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='syc.CommandRequest.Argument.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='val', full_name='syc.CommandRequest.Argument.val', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=117,
  serialized_end=170,
)

_COMMANDREQUEST = _descriptor.Descriptor(
  name='CommandRequest',
  full_name='syc.CommandRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='command', full_name='syc.CommandRequest.command', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='args', full_name='syc.CommandRequest.args', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_COMMANDREQUEST_ARGUMENT, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=38,
  serialized_end=170,
)


_COMMANDRESPONSE = _descriptor.Descriptor(
  name='CommandResponse',
  full_name='syc.CommandResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='syc.CommandResponse.result', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=172,
  serialized_end=221,
)

_COMMANDREQUEST_ARGUMENT.fields_by_name['val'].message_type = variant__pb2._VARIANT
_COMMANDREQUEST_ARGUMENT.containing_type = _COMMANDREQUEST
_COMMANDREQUEST.fields_by_name['args'].message_type = _COMMANDREQUEST_ARGUMENT
_COMMANDRESPONSE.fields_by_name['result'].message_type = variant__pb2._VARIANT
DESCRIPTOR.message_types_by_name['CommandRequest'] = _COMMANDREQUEST
DESCRIPTOR.message_types_by_name['CommandResponse'] = _COMMANDRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CommandRequest = _reflection.GeneratedProtocolMessageType('CommandRequest', (_message.Message,), {

  'Argument' : _reflection.GeneratedProtocolMessageType('Argument', (_message.Message,), {
    'DESCRIPTOR' : _COMMANDREQUEST_ARGUMENT,
    '__module__' : 'command_pb2'
    # @@protoc_insertion_point(class_scope:syc.CommandRequest.Argument)
    })
  ,
  'DESCRIPTOR' : _COMMANDREQUEST,
  '__module__' : 'command_pb2'
  # @@protoc_insertion_point(class_scope:syc.CommandRequest)
  })
_sym_db.RegisterMessage(CommandRequest)
_sym_db.RegisterMessage(CommandRequest.Argument)

CommandResponse = _reflection.GeneratedProtocolMessageType('CommandResponse', (_message.Message,), {
  'DESCRIPTOR' : _COMMANDRESPONSE,
  '__module__' : 'command_pb2'
  # @@protoc_insertion_point(class_scope:syc.CommandResponse)
  })
_sym_db.RegisterMessage(CommandResponse)



_COMMAND = _descriptor.ServiceDescriptor(
  name='Command',
  full_name='syc.Command',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=223,
  serialized_end=294,
  methods=[
  _descriptor.MethodDescriptor(
    name='InvokeCommand',
    full_name='syc.Command.InvokeCommand',
    index=0,
    containing_service=None,
    input_type=_COMMANDREQUEST,
    output_type=_COMMANDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_COMMAND)

DESCRIPTOR.services_by_name['Command'] = _COMMAND

# @@protoc_insertion_point(module_scope)