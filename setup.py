from bioptim_gui import __version__ as bioptim_gui_version
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bioptim",
    version=bioptim_gui_version,
    author="Pariterre",
    author_email="pariterre@hotmail.com",
    description="A gui to create and launch bioptim optimization program",
    long_description=long_description,
    url="https://github.com/pyomeca/bioptim_gui",
    packages=[
        ".",
        "bioptim_gui",
    ],
    license="LICENSE",
    keywords=["biorbd", "Ipopt", "CasADi", "Optimal control", "biomechanics"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    include_package_data=True,
    python_requires=">=3.10",
    zip_safe=False,
)
