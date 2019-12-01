from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='text_summarizer',
    version='0.2',
    url='https://github.com/fourplusone41/turkish-text-summarizer',
    author='Houssem MENHOUR',
    packages=find_packages(),
    install_requires=requirements
)