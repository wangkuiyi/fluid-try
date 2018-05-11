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
import unittest
import fluid.program
import proto.fluid_pb2


class TestFluidProgram(unittest.TestCase):
    def test_tensor(self):
        r = fluid.program.tensor(
            [1, 2, 3, 4], proto.fluid_pb2.Type.FLOAT32, dim=[2, 2])

        self.assertEqual(r, "0-0")
        self.assertEqual(fluid.program.current_block, 0)

        blk = fluid.program.the_program.blocks[0]
        self.assertEqual(blk.parent, -1)
        self.assertEqual(len(blk.vars), 1)

        v = blk.vars[0]
        self.assertEqual(v.type,
                         fluid.type.tensor(proto.fluid_pb2.Type.FLOAT32,
                                           [2, 2]))
        self.assertEqual(len(v.initial_value.tensor.data), 4)
        self.assertEqual(v.initial_value.tensor.data[0].real, 1)
        self.assertEqual(v.initial_value.tensor.data[1].real, 2)
        self.assertEqual(v.initial_value.tensor.data[2].real, 3)
        self.assertEqual(v.initial_value.tensor.data[3].real, 4)


if __name__ == '__main__':
    unittest.main()
