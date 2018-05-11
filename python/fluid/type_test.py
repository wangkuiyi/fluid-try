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
import fluid.type
import proto.fluid_pb2
import unittest

class TestFluidType(unittest.TestCase):

    def test_tensor(self):
        elem_type = proto.fluid_pb2.Type.INT16
        dim = [1,2,3]
        t = fluid.type.tensor(elem_type, dim)
        self.assertTrue(t.HasField("tensor"))
        self.assertFalse(t.HasField("first_class"))
        self.assertFalse(t.HasField("lod_tensor"))
        self.assertTrue(t.tensor.elem.HasField("first_class"))
        self.assertFalse(t.tensor.elem.HasField("tensor"))
        self.assertFalse(t.tensor.elem.HasField("lod_tensor"))
        self.assertEqual(t.tensor.elem.first_class, elem_type)
        self.assertEqual(t.tensor.dim, dim)

if __name__ == '__main__':
    unittest.main()
