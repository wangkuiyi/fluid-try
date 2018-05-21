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
import fluid.builtins
import types
import inspect


def initialize_program():
    prog = proto.fluid_pb2.Program()
    fluid.builtins.load_spec(prog)
    blk = prog.blocks.add()
    blk.parent = -1  # -1 indicates the root block in a program.
    return prog


the_program = initialize_program()
current_block = 0


def var_name(blk):
    """var_name returns the name of the last variable currently defined in
    the given block as a Block.VarName.
    """
    return proto.fluid_pb2.VarName(
        block=blk, var=len(the_program.blocks[blk].vars) - 1)


def get_var(var_name):
    """get_var returns the variable proto message given the
    var_name. @param var_name: proto.fluid_pb2.VarName @return:
    proto.fluid_pb2.Block.Variable
    """
    return the_program.blocks[var_name.block].vars[var_name.var]


def define_var(location, blk, var_type, initial_value=None):
    """define_var adds a Variable to Program.blocks[blk].vars. Please be
    aware that blk is an integer indexing the block in the program.
    It returns the var_name of the defined variable.
    """
    var = the_program.blocks[blk].vars.add()
    var.location = location
    var.type.CopyFrom(var_type)
    if initial_value != None:
        var.initial_value.CopyFrom(initial_value)
    return var_name(blk)


def assert_input_types_match(location, inputs, signature):
    """assert_input_types_match checks that the types of inputs match the
    function signature, wehre inputs is a list of var_names, and
    signature is proto.fluid_pb2.FunctionSignature.  It returns a list
    of proto.fluid_pb2.Type instances, each corresponds to an input.
    It raises exception if any input does not match the function
    signature.
    """
    j = 0  # indexing parameters
    for var in inputs:
        v = get_var(var)
        param = signature.inputs[j]
        if not fluid.type.var_match_param(v.type, param.types):
            raise Exception(
                "%s : the %s-th argument (%s) does not match parameter type" %
                (location, j, v.location))
        if not param.variadic:
            j = j + 1
    return [get_var(v).type for v in inputs]


def infer_output_types(fn, input_types):
    """infer_outputs returns a list of output types inferred from the list
    of input types, where fn is a proto.fluid_pb2.FunctionDefinition.
    """
    if fn.body == -1:  # this is a built-in function
        ots = getattr(fluid.builtins,
                      fn.signature.name + "_infer_types")(input_types)
    else:
        raise Exception("We don't support calling users defined function yet")
    return ots


def call_func(location, blk, fn_name, inputs):
    """call_func adds a FunctionInvocation to Program.blocks[blk]. It
    returns a list of variables returned by the function."""
    for fn in the_program.functions:
        if fn.signature.name == fn_name:  # NOTE: No function overloading
            ot = infer_output_types(fn,
                                    assert_input_types_match(location, inputs,
                                                             fn.signature))
            outputs = list(map(lambda o: define_var(location, blk, o), ot))
            c = the_program.blocks[blk].calls.add(name=fn_name,
                                                  inputs=inputs,
                                                  outputs=outputs)
            return outputs[0] if len(outputs) == 1 else tuple(outputs)
    raise Exception("%s : Function %s is not defined" % (location, fn_name))


#------------------------------------------------------------
# Public interfaces
#------------------------------------------------------------


def tensor(values, elem_type=proto.fluid_pb2.Type.FLOAT32, dim=[1]):
    """tensor defines a tensor-typed variable and returns the variable
    name.  For example: tensor([-1.0]) defines a 1x1-tensor whose
    element type is float32. tensor([1,2,3,4],
    proto.fluid_pb2.Type.INT16, [2,2]) defines a 2x2-tensor of int16
    elements.
    """
    caller = inspect.getframeinfo(inspect.stack()[1][0])
    return define_var(caller.filename + ":" + str(caller.lineno),
                      current_block,
                      fluid.type.tensor(elem_type, dim),
                      fluid.value.tensor(values, elem_type, dim))


def write(*args):
    """print prints the value of the given variables."""
    caller = inspect.getframeinfo(inspect.stack()[1][0])
    return call_func(caller.filename + ":" + str(caller.lineno), current_block,
                     "write", args)


def abs(t):
    "abs returns the abstract value of t, which is a numerical tensor." ""
    caller = inspect.getframeinfo(inspect.stack()[1][0])
    return call_func(caller.filename + ":" + str(caller.lineno), current_block,
                     "abs", [t])


def add(*args):
    "add returns the summation of its variadic parameter, which is a numerical tensor." ""
    caller = inspect.getframeinfo(inspect.stack()[1][0])
    return call_func(caller.filename + ":" + str(caller.lineno), current_block,
                     "add", args)


def matmul(*args):
    "matmul returns the product of its variadic parameter, which is a numerical tensor." ""
    caller = inspect.getframeinfo(inspect.stack()[1][0])
    return call_func(caller.filename + ":" + str(caller.lineno), current_block,
                     "matmul", args)
