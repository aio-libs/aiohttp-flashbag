import codecs
import io
import os
import re

from setuptools import setup


def get_version():
    with codecs.open(
        os.path.join(
            os.path.abspath(
                os.path.dirname(__file__),
            ),
            'aiohttp_flashbag',
            '__init__.py',
        ),
        'r',
        'utf-8',
    ) as fp:
        try:
            return re.findall(r"^__version__ = '([^']+)'$", fp.read(), re.M)[0]
        except IndexError:
            raise RuntimeError('Unable to determine version.')


def read(*parts):
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)

    with io.open(filename, encoding='utf-8', mode='rt') as fp:
        return fp.read()


install_requires = ['aiohttp>=2.3.2', 'aiohttp-session>=1.2.0']


setup(
    name='aiohttp-flashbag',
    version=get_version(),
    description=('Flashbag support for aiohttp.web',),
    long_description=read('README.rst'),
    author='Ocean S.A.',
    author_email='osf@ocean.io',
    url='https://github.com/wikibusiness/aiohttp-flashbag',
    packages=['aiohttp_flashbag'],
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=[
        'flashbag',
        'aiohttp',
    ],
)
