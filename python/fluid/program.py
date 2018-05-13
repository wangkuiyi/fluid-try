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
import google.protobuf.text_format
import proto.fluid_pb2
import fluid.type
import fluid.value
import types

# TODO(yi): We need a much simpler syntax, e.g., JSON or a
# self-defined one, than prototxt, for the description of built-in
# function signatures.
BUILTIN_FUNCTION_SPEC = """
signatures {
  name: "Print"
  inputs {
    name: "x"
    type {
      tensor {
        elem {
          first_class: INT8
          first_class: INT16
          first_class: INT32
          first_class: INT64
          first_class: UINT8
          first_class: UINT16
          first_class: UINT32
          first_class: UINT64
          first_class: FLOAT16
          first_class: FLOAT32
          first_class: FLOAT64
          first_class: BOOL
          first_class: STRING
        }
      }
    }
  }
  inputs {
    name: "indentation"
    type {
      first_class: INT8
      first_class: INT16
      first_class: INT32
      first_class: INT64
      first_class: UINT8
      first_class: UINT16
      first_class: UINT32
      first_class: UINT64
    }
  }
}
"""


def load_builtin_spec(prog):
    builtins = proto.fluid_pb2.BuiltinFunctionSpec()
    google.protobuf.text_format.Merge(BUILTIN_FUNCTION_SPEC, builtins)
    for sig in builtins.signatures:
        prog.functions.add().signature.CopyFrom(sig)


def initialize_program():
    prog = proto.fluid_pb2.Program()
    load_builtin_spec(prog)
    blk = prog.blocks.add()
    blk.parent = -1  # -1 indicates the root block in a program.
    return prog


the_program = initialize_program()
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
