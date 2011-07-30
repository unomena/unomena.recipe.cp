from setuptools import setup, find_packages

setup(
    name='unomena.recipe.cp',
    version='0.0.1',
    description='Unomena linux cp buildout recipe',
    author='Unomena',
    author_email='dev@unomena.com',
    url='http://unomena.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    zip_safe=False,
    entry_points = {'zc.buildout': ['default = unomena.recipe.cp:CP']},
)
