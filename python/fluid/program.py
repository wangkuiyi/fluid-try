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
import fluid.type
import fluid.value
import types

def create():
    prog = proto.fluid_pb2.Program()
    blk = prog.blocks.add()
    blk.parent = -1        # -1 indicates the root block in a program.
    return prog


the_program = create()
current_block = the_program.blocks[0]


def define_var(blk, var_type, initial_value):
    var = proto.fluid_pb2.Block.Variable()
    var.type.CopyFrom(var_type)
    var.initial_value.CopyFrom(initial_value)
    blk.vars.extend([var])
    return var


#------------------------------------------------------------
# Public interfaces
#------------------------------------------------------------

def tensor(values, elem_type=proto.fluid_pb2.Type.FLOAT32, dim=[1]):
    return define_var(current_block,
                      fluid.type.tensor(elem_type, dim),
                      fluid.value.tensor(values, elem_type, dim))
