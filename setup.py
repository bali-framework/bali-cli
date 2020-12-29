import cli
from setuptools import find_packages, setup

with open("requirements.txt", "r") as fh:
    install_requires = fh.read().splitlines()

setup(
    name='bali-cli',
    version=cli.__version__,
    description='Simplify gRPC services and clients',
    url='https://github.com/JoshYuJump/bali-cli',
    author='Josh.Yu',
    author_email='josh.yu_8@live.com',
    license='MIT',
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={"console_scripts": ["bali = cli.main:app", ]}
)
