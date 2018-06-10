from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.install import install
import os.path

HERE = os.path.abspath(os.path.dirname(__file__))
PROTO_DIR = os.path.join(HERE, "protos")
PACKAGE_DIR = os.path.join(HERE, "panzerserver")


def generate_proto():
    import grpc_tools.protoc

    # https://grpc.io/docs/tutorials/basic/python.html#generating-client-and-server-code
    # proto_files = [os.path.basename(proto_file) for proto_file in glob.glob(os.path.join(PROTO_DIR, "*.proto"))]
    command_arguments = [
        "",                     # dummy
        "--proto_path",         PROTO_DIR,
        "--python_out",         PACKAGE_DIR,
        "--grpc_python_out",    PACKAGE_DIR,
        os.path.join(PROTO_DIR, "panzer.proto")
    ]
    print("Building protoc: " + "python -m grpc_tools.protoc " + " ".join(command_arguments))
    result = grpc_tools.protoc.main(command_arguments)

    if result != 0:
        raise RuntimeError("grpc_tools.protoc exited with {}".format(result))


class BuildPy(build_py):

    def __init__(self, dist):
        super().__init__(dist)
        self.my_outputs = []

    def run(self):
        generate_proto()
        super().run()
        self.my_outputs = [ os.path.join(PACKAGE_DIR, p) for p in ["panzer_pb2.py", "panzer_pb2_grpc.py"]]

    def get_outputs(self):
        outputs = build_py.get_outputs(self)
        outputs.extend(self.my_outputs)
        return outputs


class Install(install):
    """Customized install command

    https://blog.niteo.co/setuptools-run-custom-code-in-setup-py/
    """

    def run(self):
        self.run_command("build_py")
        print("custom install")
        generate_proto()
        install.run(self)


setup(
    name='panzerserver',
    version='',
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
    cmdclass={"install": Install, "build_py": BuildPy}
)
