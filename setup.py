from setuptools import setup, Command
import os.path
import glob
import re

HERE = os.path.abspath(os.path.dirname(__file__))
PROTO_DIR = os.path.join(HERE, "protos")
PACKAGE_DIR = os.path.join(HERE, "panzerserver")


def generate_proto():
    import grpc_tools.protoc

    # https://grpc.io/docs/tutorials/basic/python.html#generating-client-and-server-code
    # proto_files = [os.path.basename(proto_file) for proto_file in glob.glob(os.path.join(PROTO_DIR, "*.protos"))]
    command_arguments = [
        "",  # dummy
        "--proto_path", PROTO_DIR,
        "--python_out", PACKAGE_DIR,
        "--grpc_python_out", PACKAGE_DIR,
        os.path.join(PROTO_DIR, "panzer.proto")
    ]
    print("Building protoc: " + "python -m grpc_tools.protoc " + " ".join(command_arguments))
    result = grpc_tools.protoc.main(command_arguments)

    if result != 0:
        raise RuntimeError("grpc_tools.protoc exited with {}".format(result))

    # hack gRPC generated code
    for grpc_code in glob.glob(os.path.join(PACKAGE_DIR, "*pb2_grpc.py")):
        with open(grpc_code, "r") as f:
            code = f.read()
            code = re.sub(r"import (.+_pb2) as (.+__pb2)", r"from . import \1 as \2", code)
        with open(grpc_code, "w") as f:
            f.write(code)


class Protoc(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        generate_proto()


setup(
    name='panzerserver',
    version='0.0.1',
    packages=['panzerserver'],
    url='',
    license='',
    author='xeno14',
    author_email='',
    description='',
    install_requires=[
        "grpcio==1.11.0",
        "grpcio-tools",
        "fake-rpi",
        "pyyaml",
    ],
    cmdclass={"protoc": Protoc}
)
