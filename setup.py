import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as inn:
    version = inn.read().strip()

setuptools.setup(
    name="pyastroschema",
    version=version,
    author="Luke Zoltan Kelley",
    author_email="lzkelley@gmail.com",
    description="Standardized specifications for astronomy and astrophysics data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/astrocatalogs/astroschema",
    include_package_data=True,
    packages=["pyastroschema"],
    test_suite="nose.collector",
    license="GNU",
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent"
    )
)
