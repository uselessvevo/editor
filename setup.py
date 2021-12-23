import setuptools
from pathlib import Path


def get_description():
    with open('README.md', 'r') as fh:
        long_description = fh.read()
    return long_description


def get_install_requires():
    requirements = Path('requirements').rglob('production.install.txt')
    requirements = [i.read_text().replace('\n', ',').split(',') for i in requirements]
    requirements = [i for s in requirements for i in s if i]
    return requirements


setuptools.setup(
    name='editor-app',
    version='0.0.2',
    author='Crabs dev.',
    author_email='jcommander13@yandex.ru',
    description='Editor Core library',
    long_description=get_description(),
    long_description_content_type='text/markdown',
    install_requires=get_install_requires(),
    url='https://github.com/uselessvevo/editor-app',
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    include_package_data=True,
)
