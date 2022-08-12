import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-hs-afm",
    version="0.0.1",
    author="Arheneos",
    author_email="arheneos@gmail.com",
    description="Reads HS-AFM image and converts to numpy ndarray.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arheneos/py-hs-afm",
    packages=setuptools.find_packages('afm.py'),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        'numpy'
    ],
    keywords='hs-afm, .asd, afm, asd file',
    project_urls={
        'Homepage': 'https://github.com/arheneos/py-hs-afm',
    },
)
