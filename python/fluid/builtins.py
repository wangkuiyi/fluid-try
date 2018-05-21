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
def write_signature(sig):
    sig.name = "write"
    p = sig.inputs.add(name="x")
    for e in fluid.type.SCALAR + fluid.type.STRING:
        t = p.types.add().tensor.elem.first_class = e
    p.variadic = True
    return sig


def write_infer_types(input_types):
    return []


def abs_signature(sig):
    sig.name = "abs"
    i = sig.inputs.add(name="x")
    o = sig.inputs.add(name="y")
    for e in fluid.type.NUMERIC:
        t = i.types.add().tensor.elem.first_class = e
        t = o.types.add().tensor.elem.first_class = e
    return sig


def abs_infer_types(input_types):
    return input_types


def add_signature(sig):
    sig.name = "add"
    i = sig.inputs.add(name="x", variadic=True)
    o = sig.inputs.add(name="y")
    for e in fluid.type.NUMERIC:
        t = i.types.add().tensor.elem.first_class = e
        t = o.types.add().tensor.elem.first_class = e
    return sig


def add_infer_types(input_types):
    return input_types[0:1]


def matmul_signature(sig):
    add_signature(sig)  # It is almost the signature as that of add.
    sig.name = "matmul"
    return sig


def matmul_infer_types(input_types):
    return input_types[0:1]


BUILTIN_SPECS = ["write", "abs", "add", "matmul"]


def load_spec(prog):
    for spec in BUILTIN_SPECS:
        sig = prog.functions.add().signature
        getattr(fluid.builtins, spec + "_signature")(sig)
