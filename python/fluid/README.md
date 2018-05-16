# Fluid: The Python Frontend

The compilation and execution of a Fluid program are composed of two phases:

1. The frontend phase, from the frontend language to `fluid.proto_pb2.Program`, and
1. the backend phase, interpreting and running `fluid.proto_pb2.Program` or transpiling it into C++ code.

This article is about the frontend phase.

## Type Description

### Variables Must Have Solid Types

A technical decision to be made is should we allow a variable to have multiple possible values, for example, `float16`, `float32`, or `float64`, or allow a template typed variable.

It is true that by allowing it, we have the flexibility to optimize the backend phase because, during the backend phase, we know more details about the target platform.  For example, if the target is the NVIDIA CUDA Volta GPU, which supports `float16`, the transpiler could realize all float-typed variables to be `float16` instead of `float32` by default.  However, this complicates the design of the backend system; so let us decide that variables cannot be template, and the solid type of a variable must be specified or inferred in the frontend phase.

### Template Function Parameters

A Fluid variable could be a scalar value, a tensor value, etc.  To ease the description of the challenge, let's consider the scalar and tensor case, where we could represent a type like the following:

```protobuf
message Type {
  enum FirstClass {
    INT32 = 1;
    FLOAT32 = 2;
    ...
  }
  message Tensor {
    required Type elem = 1; <-- (1)
    ...
  }
  optional FirstClass first_class = 1; <-- (2)
  optional Tensor tensor = 2;
}
```

Due to the line marked `(1)`, the message `Type` could represent a tensor of tensors or a nested tensor.  However, it cannot represent *template* types, for example, the parameter of function `Abs` (in ONNX and TensorFlow) is a *numerical tensor*, whose elements could be `int32`, `float32`, etc., which looks like a C++ Tensor template:

```c++
template <typename FirstClass>
class Tensor {...}
```

which could be specialized into `Tensor<int32>`, `Tensor<float32>`, etc.

To support the above *template* in Fluid, we have several solutions.

1. to change `(1)` to be

   ```protobuf
   repeated Type elem = 1; <-- (1)
   ```

1. to change `(2)` to be
 
   ```protobuf
   repeated FirstClass first_class = 1; <-- (2)
   ```
   
1. to change none of `(1)` or `(2)`, but use `repeated Type`, instead of `optional/required Type`, to specify the type of a parameter.

The first two solutions complicate the syntax of `Type` because they use `Type` to represent a solid and a template type.  Because a variable must have a solid type and parameters could be template, we would have to write functions like

- `is_solid_type(proto.fluid_pb2.Type)`
- `is_template_type(proto.fluid_pb2.Type)`

Another complication comes from the fact that we need the function `is_instance(solid_type, template_type)` to check if a variable is acceptable by a function as its parameter.  The first two solutions complicate the implementation of `is_instance`.

## Type Inference

To pose the problem of type inference, let us start from an example:

```python
W = fluid.tensor([-1], dtype=float32)
V = fluid.abs(W) 
```

The first line of the above program creates W as a 1x1 tensor of float32 values. The second line creates V, and calls the built-in function `abs` as:

```c++
abs(W, &V);
```

The problem is that -- what is the type of V?  Please be aware that the type of a tensor includes the element type and the dimension.

### Week Type

Given that V is the output of `abs`, and `abs` is taking W as its input, it seems intuitive that V has the same element type and dimension as W -- float32 and 1x1.


However, this is not that intuitive -- a Fluid function input/output is like a C++ template type.  For example, the signature of `abs` in C++ looks like the following:

```c++
template <typename T /* {float16, float32, int8, int16, int32, ...} */> 
void Abs(const Tensor<T, 1, 1> W, Tensor<T, ?>* V) {
}
```

We might need an `abs_infer_io_types` function to infer the element type and dimension of the outputs of `abs` from the given inputs.

### Strong Type

In statically typed language, programmers need to explicitly specify the type of both inputs and outputs of a function invocation.  Consider the following C++ code as a reference.

```c++
Tensor<float32, 1, 1> W = fluid.tensor(-1);
Tensor<float32, 1, 1> V;
abs(W, &V);
```

However, Python doesn't allow programmers to specify the type of variables, e.g., V.  We cannot write the following code:

```python
W = fluid.tensor([-1], dtype=float32)
V = fluid.tensor([-1], dtype=float32)
V = fluid.abs(W) 
```


because the Python variable V is dynamically-typed and would be changed to a type other than `Tensor<float32, 1,1>` by the `fluid.abs` call.

It seems that if we write the following code

```python
W = fluid.tensor([-1], dtype=float32)
V = fluid.tensor([-1], dtype=float32)
fluid.abs(W, V) 
```


we got a chance to create V with explicitly specified type.  However, this would make it possible to set the input and output of a function to the same variable, e.g.,

```python
fluid.abs(W, W)
```


which should be prohibited because we'd have no chance to compute the derivation of the output of `abs` in the backward pass.

The conclusion is that, to the right moment, we don't have a good idea to implement type declaration in Fluid's Python frontend.
