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
    def assert_initialize_program(self):
        # Built-in function signatures have been loaded into the program.
        self.assertEqual(len(fluid.program.the_program.functions), 2)
        self.assertEqual(fluid.program.the_program.functions[0].signature.name,
                         "write")
        self.assertEqual(fluid.program.the_program.functions[1].signature.name,
                         "abs")
        # The root block has been initialized.
        self.assertEqual(len(fluid.program.the_program.blocks), 1)
        self.assertEqual(fluid.program.the_program.blocks[0].parent, -1)

    def assert_tensor(self, tensor_var):
        self.assertEqual(tensor_var, "0-0")
        self.assertEqual(fluid.program.current_block, 0)
        blk = fluid.program.the_program.blocks[0]
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

    def assert_write(self):
        self.assertEqual(fluid.program.current_block, 0)
        blk = fluid.program.the_program.blocks[0]
        self.assertEqual(len(blk.calls), 1)
        c = blk.calls[0]
        self.assertEqual(c.name, "write")
        self.assertEqual(len(c.inputs), 1)
        self.assertEqual(c.inputs[0], "0-0")
        self.assertEqual(len(c.outputs), 0)

    def test_write_a_tensor(self):
        self.assert_initialize_program()

        r = fluid.program.tensor(
            [1, 2, 3, 4], proto.fluid_pb2.Type.FLOAT32, dim=[2, 2])

        self.assert_tensor(r)

        fluid.program.write(r)

        self.assert_write()


if __name__ == '__main__':
    unittest.main()
