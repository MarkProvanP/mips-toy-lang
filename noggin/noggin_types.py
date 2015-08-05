class NogginType:
	typeName = None

	def __init__(self, typeName):
		self.typeName = typeName

	def __eq__(self, other):
		return self.typeName == other.typeName

	def to_key(self):
		return typeName

NT_types_base = {}

NT_void = NogginType("void")
NT_types_base['void'] = NT_void
NT_char = NogginType("char")
NT_types_base['char'] = NT_char
NT_uint = NogginType("uint")
NT_types_base['uint'] = NT_uint
NT_int = NogginType("int")
NT_types_base['int'] = NT_int
NT_bool = NogginType("bool")
NT_types_base['bool'] = NT_bool
NT_string = NogginType("string")
NT_types_base['string'] = NT_string
