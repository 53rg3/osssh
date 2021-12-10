from setuptools import setup, find_packages

setup(
    name="osssh",
    version="1.0",
    packages=find_packages(),
    py_modules=['osssh'],
    install_requires=[
        'click',
        'prompt_toolkit',
        'ruamel.yaml',
        'pathlib'
    ]
)
