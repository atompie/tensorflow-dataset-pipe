from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='dataset_pipe',
    version='0.7.5',
    description='Utils for encoding and data set reading',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atompie/tensorflow-dataset-pipe",
    author='Risto Kowaczewski',
    author_email='risto.kowaczewski@gmail.com',
    packages=['dataset_pipe'],
    install_requires=[
        'tensorflow',
        'numba'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True
)
