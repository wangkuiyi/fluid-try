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
    proto.fluid_pb2.Type.INT8 ,
    proto.fluid_pb2.Type.INT16 ,
    proto.fluid_pb2.Type.INT32 ,
    proto.fluid_pb2.Type.INT64
]
UNSIGNED_INT = [
    proto.fluid_pb2.Type.UINT8 ,
    proto.fluid_pb2.Type.UINT16 ,
    proto.fluid_pb2.Type.UINT32 ,
    proto.fluid_pb2.Type.UINT64
]
FLOAT = [
    proto.fluid_pb2.Type.FLOAT16 ,
    proto.fluid_pb2.Type.FLOAT32 ,
    proto.fluid_pb2.Type.FLOAT64
]

def tensor(elem_types=SIGNED_INT + UNSIGNED_INT + FLOAT + [proto.fluid_pb2.Type.BOOL], dim=[1]):
    t = proto.fluid_pb2.Type()
    t.tensor.elem_types[:] = elem_types
    t.dim[:] = dim
    return t

def signed_int_tensor(dim=[1]):
    return tensor(SIGNED_INT, dim)

def unsigned_int_tensor(dim=[1]):
    return tensor(UNSIGNED_INT, dim)

def int_tensor(dim=[1]):
    return tensor(SIGNED_INT + UNSIGNED_INT, dim)

def float_tensor(dim=[1]):
    return tensor(FLOAT, dim)

def numeric_tensor(dim=[1]):
    return tensor(SIGNED_INT + UNSIGNED_INT + FLOAT, dim)

def bool_tensor(dim=[1]):
    return tensor([proto.fluid_pb2.Type.BOOL], dim)
