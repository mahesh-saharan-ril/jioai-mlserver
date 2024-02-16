import os

from typing import Dict
from setuptools import setup, find_packages

ROOT_PATH = os.path.dirname(__file__)
PKG_NAME = "jioai_mlserver"
PKG_PATH = os.path.join(ROOT_PATH, PKG_NAME)


def _load_version() -> str:
    version = ""
    version_path = os.path.join(PKG_PATH, "version.py")
    with open(version_path) as fp:
        version_module: Dict[str, str] = {}
        exec(fp.read(), version_module)
        version = version_module["__version__"]

    return version


def _load_description() -> str:
    readme_path = os.path.join(ROOT_PATH, "README.md")
    with open(readme_path) as fp:
        return fp.read()


env_marker_cpython = (
    "sys_platform != 'win32'"
    " and (sys_platform != 'cygwin'"
    " and platform_python_implementation != 'PyPy')"
)

setup(
    name=PKG_NAME,
    version=_load_version(),
    url="https://devops.jio.com/AICOE/jioai-vision/_git/jioai-mlserver",
    author="Pulkit Mishra",
    author_email="pulkit.mishra@ril.com",
    description="JioAI ML server",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "click",
        "fastapi",
        "python-dotenv",
        "grpcio",
        "importlib-metadata;python_version<'3.8'",
        "numpy",
        "pandas",
        "protobuf",
        "uvicorn",
        "starlette_exporter",
        "py-grpc-prometheus",
        "uvloop;" + env_marker_cpython,
        "aiokafka",
        "tritonclient[http]>=2.24",
        "aiofiles",
        "orjson",
    ],
    entry_points={"console_scripts": ["jioai_mlserver=jioai_mlserver.cli:main"]},
    long_description=_load_description(),
    long_description_content_type="text/markdown",
    license="Apache 2.0",
)
