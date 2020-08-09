import setuptools

with open("../README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dulp-tombs",
    version="0.0.1",
    author="Rupert Tombs",
    author_email="rt500@cam.ac.uk",
    description="Floating point differences",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/Rupt/dulp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
) 
