from setuptools import setup, find_packages

setup(
    name='evolutionapi',
    version='0.0.3',
    description='Client Python para a API Evolution',
    author='Davidson Gomes',
    author_email='contato@agenciadgcode.com',
    packages=find_packages(),
    package_data={'': ['*']},
    include_package_data=True,
    install_requires=[
        'requests>=2.25.1',
    ],
    python_requires='>=3.6',
)
