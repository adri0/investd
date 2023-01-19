from setuptools import find_packages, setup


def read_contents(path: str) -> str:
    with open(path, "r") as file:
        return file.read()


setup(
    name="investd",
    version="0.0.1",
    author="adri0",
    author_email="",
    url="",
    long_description=read_contents("README.md"),
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
    install_requires=read_contents("requirements-latest.txt").strip().split(),
    extras_require={
        "dev": read_contents("requirements-dev.txt").strip().split(),
    },
    entry_points={"console_scripts": ["investd = investd.__main__:cli"]},
    tests_require=["pytest", "pytest-cov", "pytest-dotenv"],
)
