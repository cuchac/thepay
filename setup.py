from setuptools import setup

setup(
    name='thepay',
    version='0.4',
    packages=['thepay'],
    url='https://github.com/cuchac/thepay',
    license='LGPL',
    author='cuchac',
    author_email='cuchac@email.cz',
    description='ThePay API library',
    install_requires=(
        'suds_jurko',
        'six',
    )
)
