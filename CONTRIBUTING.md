# Contributing

To ensure the efficiency of collaborative development, developers please do NOT configure your own development environment, but please use the `/Dockerfile` to build a Docker image as your development environment.

## Build the Development Environment as a Docker Image

```bash
git clone https://github.com/wangkuiyi/fluid
cd fluid
docker build -t fluid:dev .
```

The above commands create a Docker image named `fluid:dev`, which has all development tools installed, including clang, llvm, python, protoc, open-ssh etc.  For more details, please check the `/Dockerfile`.

## Run the Development Environment as a Docker Container

Use the following command to run the above Docker image as a container:

```bash
docker run -v $PWD:/paddle -d --rm -P --name fluid fluid:dev
```

The `--name fluid` flag gives the container a name `fluid`.

The `-v $PWD:/paddle` flag maps the current directory, which is supposed to be the local `fluid` repo, to the `/paddle` directory in the container.

The `-d` flag runs the container in the background. But the default entry-point of the container starts the SSH service, which accepts users to log in as `root`, and the password is also `root`.

The `-P` flag maps all listening ports inside the container, particularly, the SSH service port 22, to a port of the host computers, which could be revealed by the following command

```bash
docker port fluid 22
```

## Login to the Development Environment

Suppose that the above command prints the host network address `0.0.0.0:32770`, we could log in by running

```bash
ssh root@localhost -P 32770
```

Within the SSH session, type the following command to build the Fluid source code:

```bash
cd /paddle
mkdir build
cd build
cmake ..
make -j10
```

The `cd /paddle` works because that the flag `-v $PWD:/paddle` in the Docker container startup command maps the source directory on the host to directory `/paddle` in the container.

The mapping also enables developers to run the editors (Emacs, VIM, Eclipse, etc) on the host computer -- whenever they save the edits, the changes are mapped into the container, so the developers can run

```bash
make -j10
```

in the SSH session again to rebuild.
