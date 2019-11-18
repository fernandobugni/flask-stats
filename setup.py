import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='flask-api-stats',
    version='0.5',
    author="Fernando Bugni",
    author_email="fernando.bugni@gmail.com",
    description="A plugin for flask to obtain API statistics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gaturron/flask-stats",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
