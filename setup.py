from setuptools import setup

setup(
    name='dataset_pipe',
    version='0.2',
    description='Utils for encoding and data set reading',
    author='Risto Kowaczewski',
    author_email='risto.kowaczewski@gmail.com',
    packages=['dataset_pipe', 'encoders'],
    install_requires=[
        'tensorflow'
        'numpy',
        'python-interface==1.5.3',
        'numba',
        'numpy'
    ],
    include_package_data=True
)
