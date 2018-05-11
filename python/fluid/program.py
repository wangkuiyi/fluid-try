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

def create_program():
    prog = proto.fluid_pb2.Program()
    prog.blocks.append(proto.fluid_pb2.Block())
    return prog

current_program = create_program()
current_block = current_program.blocks[0]



def const_tensor(value, size=[1]):
    current_block
    return nil
