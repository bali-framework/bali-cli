import cli
from setuptools import find_packages, setup

INSTALL_REQUIREMENTS = [
    'grpcio==1.32.0',
    'grpcio-tools==1.32.0',
    'typer==0.3.2',
]

setup(
    name='bali-cli',
    version=cli.__version__,
    description='Simplify gRPC services and clients',
    url='https://github.com/JoshYuJump/bali',
    author='Josh.Yu',
    author_email='josh.yu_8@live.com',
    license='MIT',
    install_requires=INSTALL_REQUIREMENTS,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
