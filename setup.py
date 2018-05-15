from setuptools import setup
import glob
import os.path
import subprocess

HERE = os.path.abspath(os.path.dirname(__file__))
PROTO_DIR = os.path.join(HERE, "protos")
PACKAGE_DIR = os.path.join(HERE, "tigerserver")

def generate_proto():
    # https://grpc.io/docs/tutorials/basic/python.html#generating-client-and-server-code
    # proto_files = [os.path.basename(proto_file) for proto_file in glob.glob(os.path.join(PROTO_DIR, "*.proto"))]
    o = subprocess.run([
        "python",
        "-m", "grpc_tools.protoc",
        "-I", PROTO_DIR,
        "--python_out="+PACKAGE_DIR,
        "--grpc_python_out="+PACKAGE_DIR,
        os.path.join(PROTO_DIR, "panzer.proto")
    ])
    if o != 0:
        raise RuntimeError("grpc_tools.proto failed")


setup(
    name='tigerserver',
    version='',
    packages=['tigerserver'],
    url='',
    license='',
    author='xeno14',
    author_email='',
    description='',
    install_requres=[
        "grpcio",
        "grpcio-tools",
        "fake-rpi",
    ],
)
