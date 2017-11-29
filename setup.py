import re
from pathlib import Path

from setuptools import setup


def get_version():
    init_file = Path(__file__).parent / 'aiohttp_flashbag' / '__init__.py'

    content = init_file.read_text(encoding='utf-8')

    try:
        return re.findall(r"^__version__ = '([^']+)'$", content, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


def read(*parts):
    return Path(__file__).parent.joinpath(*parts).read_text(encoding='utf-8')


install_requires = ['aiohttp>=2.3.0', 'aiohttp-session>=1.2.0']


setup(
    name='aiohttp-flashbag',
    version=get_version(),
    description=('Flashbag (flash messages) support for aiohttp.web',),
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=[
        'flashbag',
        'flash messages',
        'aiohttp',
    ],
)
