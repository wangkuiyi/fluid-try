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

# Usage:
#
#  1. Compile the program into the intermediate representation (IR):
#
#     python fit_a_line.py
#
#  2. Interpret and run the IR:
#
#     python fit_a_line.py | fluid
#
#     where fluid is the Fluid interpreter, a C++ program.
#
from fluid.program import tensor
from fluid.program import write

W = tensor([1.0])

# with fluid.loop(steps=100):
#     x, y = fluid.data()
#     cost = fluid.mse(fluid.fc(x, W), y)
#     fluid.optimize(cost)

write(W)
