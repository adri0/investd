from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="investd",
    version="0.0.1",
    author="adri0",
    author_email="",
    url="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    packages=find_packages(exclude=["tests", "sample_data"]),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=[line.strip() for line in open("requirements-latest.txt")],
    extras_require={
        "dev": [line.strip() for line in open("requirements-dev.txt")],
    },
    entry_points={"console_scripts": ["investd = investd.__main__:cli"]},
    tests_require=["pytest", "pytest-cov", "pytest-dotenv"],
)
