import os
from glob import glob

from setuptools import setup

setup(
    name="open-mcp-blender",
    version="0.1.0",
    packages=["open-mcp-blender"],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/open-mcp-blender"]),
        ("share/open-mcp-blender", ["package.xml"]),
        (
            os.path.join("share", "open-mcp-blender", "launch"),
            glob(os.path.join("launch", "*launch.[pxy][yma]*")),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Emanuel Buholzer",
    maintainer_email="emanuel0xb@gmail.com",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [],
    },
)
