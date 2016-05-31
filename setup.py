from setuptools import setup
from rangeplus import __version__

setup(
    name = 'rangeplus',
    packages = [ 'rangeplus' ],
    version = __version__,
    description = 'Extended Python Range Class',
    author = 'Avner Herskovits',
    author_email = 'avnr_ at outlook.com',
    url = 'https://github.com/avnr/rangeplus',
    download_url = 'https://github.com/avnr/rangeplus/tarball/' + __version__,
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
)
