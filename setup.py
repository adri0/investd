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
    ],
    packages=find_packages(exclude=["tests"]),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        "pandas",
        "openpyxl",
        "pydantic",
        "PyYAML",
        "click",
        "python-dotenv",
        "ipython",
        "jupyter",
        "jupytext",
        "seaborn",
    ],
    extras_require={
        "dev": [
            "pip",
            "wheel",
            "mypy",
            "pytest",
            "pytest-cov",
            "isort",
            "black",
        ],
    },
    entry_points={"investd.__main__": {"main = investd.__main__:cli"}},
    tests_require=["pytest", "pytest-cov"],
)
