from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='pypact-lang',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'pynacl'
    ],
    url='https://github.com/cyberfly-io/pypact',
    long_description=long_description,
    long_description_content_type='text/markdown'
)

