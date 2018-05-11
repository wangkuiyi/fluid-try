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
import fluid.type
import operator                 # for mul
import proto.fluid_pb2
import types

def scalar(value, type):
    v = proto.fluid_pb2.Value()
    if type in fluid.type.SIGNED_INT:
        v.int = value
    elif type in fluid.type.UNSIGNED_INT:
        v.uint = value
    elif type in fluid.type.FLOAT:
        v.real = value
    elif type in fluid.type.BOOL:
        v.bool = value
    elif type in fluid.type.STRING:
        v.string = value
    elif type in fluid.type.BLOCK:
        v.block = value
    else:
        raise ValueError('Unknown type:', type)
    return v

        
def tensor(elem_values, elem_type, dim):
    assert type(elem_values) is types.ListType
    assert len(elem_values) == reduce(operator.mul, dim, 1)
    
    v = proto.fluid_pb2.Value()
    v.tensor.data.extend(list(map(lambda x : scalar(x, elem_type),
                             elem_values)))
    return v
    
