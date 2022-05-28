from setuptools import setup, find_packages

setup(
    name='pypact-lang',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'pynacl'
    ],
    url='https://github.com/cyberfly-io/pypact'
)

