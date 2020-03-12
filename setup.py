from setuptools import setup

setup(
    name='nijel-thepay',
    version='0.5',
    packages=['thepay'],
    url='https://github.com/nijel/thepay',
    license='LGPL',
    author='cuchac',
    author_email='michal@cihar.com',
    description='ThePay API library',
    install_requires=(
        'suds-community',
        'six',
    )
)
