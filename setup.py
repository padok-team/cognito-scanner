from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='cognito-scanner',
    version='1.0.3',
    packages=find_packages(),
    install_requires=[
        "boto3", "typer"
    ],
    entry_points={
        'console_scripts': [
            'cognito-scanner = scanner.scanner:cli',
        ],
    },
    authors = [ { 'name': "Thibault Lengagne", 'email': 'thibaultl@padok.fr' }, { 'name':"Clement Fgs", 'email':'clementfa@padok.fr' }, ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author_email='thibaultl@padok.fr',
    url='https://github.com/padok-team/cognito-scanner',
    license='Apache2',
)