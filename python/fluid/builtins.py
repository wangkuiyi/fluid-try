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
import google.protobuf.text_format
import fluid.type


# TODO(yi): In the future, we should write a C++ parser using
# Clang/LLVM to derive the following specifications by parsing the C++
# source code of the built-in functions, so that built-in developers
# don't have to write the following specifications manually.
def print_signature():
    f = proto.fluid_pb2.FunctionSignature()
    f.name = "write"
    p = f.inputs.add()
    p.name = "x"
    for e in fluid.type.SCALAR + fluid.type.STRING:
        t = p.types.add()
        t.tensor.elem.first_class = e
    p.variadic = True
    return f


def print_infer_types(input_types):
    return None


def abs_signature():
    f = proto.fluid_pb2.FunctionSignature()
    f.name = "abs"
    i = f.inputs.add()
    i.name = "x"
    o = f.inputs.add()
    o.name = "y"
    for e in fluid.type.NUMERIC:
        t = i.types.add()
        t.tensor.elem.first_class = e
        t = o.types.add()
        t.tensor.elem.first_class = e
    return f


def abs_infer_types(input_types):
    return input_types


BUILTIN_SPECS = [print_signature, abs_signature]


def load_spec(prog):
    for spec in BUILTIN_SPECS:
        prog.functions.add().signature.CopyFrom(spec())
