# Copyright 2018 Yi Wang <yi.wang.2005@gmail.com> All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import proto.fluid_pb2

SIGNED_INT = [
    proto.fluid_pb2.Type.INT8, proto.fluid_pb2.Type.INT16,
    proto.fluid_pb2.Type.INT32, proto.fluid_pb2.Type.INT64
]
UNSIGNED_INT = [
    proto.fluid_pb2.Type.UINT8, proto.fluid_pb2.Type.UINT16,
    proto.fluid_pb2.Type.UINT32, proto.fluid_pb2.Type.UINT64
]
LONG = [proto.fluid_pb2.Type.INT64, proto.fluid_pb2.Type.UINT64]
FLOAT = [
    proto.fluid_pb2.Type.FLOAT16, proto.fluid_pb2.Type.FLOAT32,
    proto.fluid_pb2.Type.FLOAT64
]
BOOL = [proto.fluid_pb2.Type.BOOL]
STRING = [proto.fluid_pb2.Type.STRING]
BLOCK = [proto.fluid_pb2.Type.BLOCK]
INT = SIGNED_INT + UNSIGNED_INT
NUMERIC = INT + FLOAT
SCALAR = NUMERIC + BOOL


def is_compatible_dim(dim1, dim2):
    """is_compatible_dim returns True if dim1 and dim2 are compatible with
    each other, or an error message.  Both dim1 and dim2 are
    proto.fluid_pb2.Type.Tensor.dim.
    """
    if len(dim1) != len(dim2):
        return "%s and %s have different dimensionality" % (dim1, dim2)
    for i in range(len(dim1)):
        if dim1[i] >= 0 and dim2[i] >= 0 and dim1[i] != dim2[i]:
            return "the %d-th dimension of %s and %s are not equal" % (i, dim1,
                                                                       dim2)
    return True


def var_match_param(var_type, parameter_types):
    """var_type is a proto.fluid_pb2.Type, parameter_types is
    proto.fluid_pb2.FunctionSignature.Parameter.types."""
    for t in parameter_types:
        if str(t) == str(var_type):
            return True
    return False


def infer_outputs(fn, inputs_types):
    """infer_outputs returns a list of output types inferred from the list
    of input types, where fn is a proto.fluid_pb2.FunctionDefinition.
    """
    if fn.body == -1:  # this is a built-in function
        ots = getattr(fluid.builtins, fn.name + "_infer_types")(input_types)
    else:
        raise Exception("We don't support calling users defined function yet")
    return ots


def tensor(elem_type, dim):
    t = proto.fluid_pb2.Type()
    t.tensor.elem.first_class = elem_type
    t.tensor.dim[:] = dim
    return t
