# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: panzer.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='panzer.proto',
  package='panzer',
  syntax='proto3',
  serialized_pb=_b('\n\x0cpanzer.proto\x12\x06panzer\"7\n\x0c\x44riveRequest\x12\x12\n\nleft_level\x18\x01 \x01(\x01\x12\x13\n\x0bright_level\x18\x02 \x01(\x01\" \n\rDriveResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"<\n\x0e\x43ontrolRequest\x12*\n\x0c\x64riveRequest\x18\x01 \x01(\x0b\x32\x14.panzer.DriveRequest\"\"\n\x0f\x43ontrolResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32~\n\x06Panzer\x12\x36\n\x05\x44rive\x12\x14.panzer.DriveRequest\x1a\x15.panzer.DriveResponse\"\x00\x12<\n\x07\x43ontrol\x12\x16.panzer.ControlRequest\x1a\x17.panzer.ControlResponse\"\x00\x62\x06proto3')
)




_DRIVEREQUEST = _descriptor.Descriptor(
  name='DriveRequest',
  full_name='panzer.DriveRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='left_level', full_name='panzer.DriveRequest.left_level', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='right_level', full_name='panzer.DriveRequest.right_level', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=79,
)


_DRIVERESPONSE = _descriptor.Descriptor(
  name='DriveResponse',
  full_name='panzer.DriveResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='panzer.DriveResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=81,
  serialized_end=113,
)


_CONTROLREQUEST = _descriptor.Descriptor(
  name='ControlRequest',
  full_name='panzer.ControlRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='driveRequest', full_name='panzer.ControlRequest.driveRequest', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=115,
  serialized_end=175,
)


_CONTROLRESPONSE = _descriptor.Descriptor(
  name='ControlResponse',
  full_name='panzer.ControlResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='panzer.ControlResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=177,
  serialized_end=211,
)

_CONTROLREQUEST.fields_by_name['driveRequest'].message_type = _DRIVEREQUEST
DESCRIPTOR.message_types_by_name['DriveRequest'] = _DRIVEREQUEST
DESCRIPTOR.message_types_by_name['DriveResponse'] = _DRIVERESPONSE
DESCRIPTOR.message_types_by_name['ControlRequest'] = _CONTROLREQUEST
DESCRIPTOR.message_types_by_name['ControlResponse'] = _CONTROLRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DriveRequest = _reflection.GeneratedProtocolMessageType('DriveRequest', (_message.Message,), dict(
  DESCRIPTOR = _DRIVEREQUEST,
  __module__ = 'panzer_pb2'
  # @@protoc_insertion_point(class_scope:panzer.DriveRequest)
  ))
_sym_db.RegisterMessage(DriveRequest)

DriveResponse = _reflection.GeneratedProtocolMessageType('DriveResponse', (_message.Message,), dict(
  DESCRIPTOR = _DRIVERESPONSE,
  __module__ = 'panzer_pb2'
  # @@protoc_insertion_point(class_scope:panzer.DriveResponse)
  ))
_sym_db.RegisterMessage(DriveResponse)

ControlRequest = _reflection.GeneratedProtocolMessageType('ControlRequest', (_message.Message,), dict(
  DESCRIPTOR = _CONTROLREQUEST,
  __module__ = 'panzer_pb2'
  # @@protoc_insertion_point(class_scope:panzer.ControlRequest)
  ))
_sym_db.RegisterMessage(ControlRequest)

ControlResponse = _reflection.GeneratedProtocolMessageType('ControlResponse', (_message.Message,), dict(
  DESCRIPTOR = _CONTROLRESPONSE,
  __module__ = 'panzer_pb2'
  # @@protoc_insertion_point(class_scope:panzer.ControlResponse)
  ))
_sym_db.RegisterMessage(ControlResponse)



_PANZER = _descriptor.ServiceDescriptor(
  name='Panzer',
  full_name='panzer.Panzer',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=213,
  serialized_end=339,
  methods=[
  _descriptor.MethodDescriptor(
    name='Drive',
    full_name='panzer.Panzer.Drive',
    index=0,
    containing_service=None,
    input_type=_DRIVEREQUEST,
    output_type=_DRIVERESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Control',
    full_name='panzer.Panzer.Control',
    index=1,
    containing_service=None,
    input_type=_CONTROLREQUEST,
    output_type=_CONTROLRESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_PANZER)

DESCRIPTOR.services_by_name['Panzer'] = _PANZER

# @@protoc_insertion_point(module_scope)
