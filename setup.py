from setuptools import setup, find_packages

setup(
    name='cognito-scanner',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "boto3", "typer"
    ],
    entry_points={
        'console_scripts': [
            'cognito-scanner = scanner.scanner:cli',
        ],
    },
    author='Clement Fgs',
    author_email='clementfa@padok.fr',
    description='A tool to attack Cognito instances',
    url='https://github.com/padok-team/cognito-scanner',
    license='Apache2',
)
