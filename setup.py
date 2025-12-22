import os
from setuptools import setup

__VERSION__ = "0.1.0"

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "requirements.txt")) as fi:
    REQUIREMENTS = fi.readlines()

setup(
    name="codi",
    packages=["src"],
    entry_points={"console_scripts": ["codi=src.chat:main"]},
    version=__VERSION__,
    description="My own coding agent",
    url="https://github.com/jschnab/coding-agent",
    author="Jonathan Schnabel",
    author_email="jonathan.schnabel31@gmail.com",
    license="GNU General Public Licence v3.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.9",
    keywords="coding agent assistant",
    install_requires=REQUIREMENTS,
)
