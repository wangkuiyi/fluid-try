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
    blk.parent = -1  # -1 indicates the root block in a program.
    return prog


the_program = create()
current_block = 0


# var_name returns the name of the last variable currently defined in
# the given block.  The naming convention is
# <current_block_id>-<var_index>.
def var_name(blk):
    n = str(len(the_program.blocks[blk].vars) - 1)
    return str(blk) + '-' + n


# define_var adds a Variable to Program.blocks[blk].vars. Please be
# aware that blk is an integer indexing the block in the program.
def define_var(blk, var_type, initial_value=None):
    var = the_program.blocks[blk].vars.add()
    var.type.CopyFrom(var_type)
    if initial_value != None:
        var.initial_value.CopyFrom(initial_value)
    return var_name(blk)


#def call_func(fn_name, inputs):
# 1. check signature by function fn_name
# 2. create variables according to signature outputs
# 3. call function-specific type inferener to set output variable types
# 4. add output variables and their types to Block.vars
# 5. add an element into Block.calls.

#------------------------------------------------------------
# Public interfaces
#------------------------------------------------------------


def tensor(values, elem_type=proto.fluid_pb2.Type.FLOAT32, dim=[1]):
    return define_var(current_block,
                      fluid.type.tensor(elem_type, dim),
                      fluid.value.tensor(values, elem_type, dim))
