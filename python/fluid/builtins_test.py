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
import fluid.builtins
import unittest


class TestFluidBuildins(unittest.TestCase):
    def test_load_spec(self):
        prog = proto.fluid_pb2.Program()
        fluid.builtins.load_spec(prog)
        found = False
        for f in prog.functions:
            if f.signature.name == "write":
                found = True
                ground_truth = fluid.builtins.print_signature()
                self.assertEqual(
                    len(f.signature.inputs[0].types),
                    len(ground_truth.inputs[0].types))
                self.assertEqual(f.signature.name, ground_truth.name)
        self.assertTrue(found)


if __name__ == '__main__':
    unittest.main()
