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
import fluid


def create_generator_parameters():
    return {"Gw": fluid.tensor(dim=[2, 20]), "Gb": fluid.tensor(dim=[20])}


def create_discriminator_parameters():
    return {"Dw": fluid.tensor(dim=[20, 2]), "Db": fluid.tensor(dim=[2])}


def generate(noise, params):
    return fluid.fc(noise, params["Gw"], params["Gb"])


with fluid.defun("train_discriminator", mb, params):
    fluid.optimize(
        fluid.mse(
            fluid.softmax(fluid.fc(mb[0], params["Dw"], params["Db"])), mb[1]),
        params)

with fluid.defun("train_generator", noise, g_params, d_params):
    fluid.optimize(
        fluid.mse(
            fluid.softmax(
                fluid.fc(
                    generate(noise, g_params), d_params["Dw"], d_params["Db"]),
                fluid.reshape(True, fluid.sizeof(noise)))), g_params)

generator_params = create_generator_parameters()
discriminator_params = create_discriminator_parameters()

with fluid.loop(iter=1000):
    # Read real images
    real_images = fluid.data("images")

    # Generate fake images
    noise = fluid.random()
    fake_images = generate(noise, generator_params)

    # Mix real and fake images
    mb = fluid.enssamble_minibatch(real_images, True, fake_images, False)

    # Train discriminator
    fluid.call("train_discriminator", mb, discriminator_params)

    # Train generator
    fluid.call("train_generator", noise, generator_params,
               discriminator_params)
