from setuptools import setup

setup(
    name="omcp_blender",
    version="0.1.0",
    packages=["omcp_blender"],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/omcp_blender"]),
        ("share/omcp_blender", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Emanuel Buholzer",
    maintainer_email="emanuel0xb@gmail.com",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest", "pytest-blender"],
    entry_points={
        "console_scripts": [],
    },
)
