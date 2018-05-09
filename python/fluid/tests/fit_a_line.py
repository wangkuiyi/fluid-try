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
import fluid

W = fluid.Tensor(1.0)

with fluid.loop(steps=100):
    x, y = fluid.data()
    cost = fluid.mse(fluid.fc(x, W), y)
    fluid.optimize(cost)

fluid.print(W)
