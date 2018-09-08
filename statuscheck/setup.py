import os
import re

from setuptools import find_packages, setup


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__),
                           'aiohttp_statuscheck', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            msg = 'Cannot find version in aiohttp_statuscheck/__init__.py'
            raise RuntimeError(msg)

# FIXME: This does not handle git+ssh packages
# source: https://github.com/dave-shawley/python-cookiecutter/blob/844e6bfcf8639eab4feef0c2a83ac61f3aea412c/%7B%7Bcookiecutter.package_name%7D%7D/setup.py


def read_requirements(name):
    requirements = []
    try:
        with open(name) as req_file:
            for line in req_file:
                # source: http://www.diveintopython.net/native_data_types/lists.html
                if "#" in line:
                    line = line[: line.index("#")]
                line = line.strip()
                if line.startswith("-r"):
                    requirements.extend(read_requirements(line[2:].strip()))
                elif not line.startswith("-"):
                    if line is "":
                        continue
                    requirements.append(line)
    except IOError:
        pass

    return requirements


requirements = read_requirements("requirements.txt")


# install_requires = ['aiohttp',
#                     'aiopg[sa]',
#                     'aiohttp-jinja2',
#                     'trafaret-config']


setup(name='aiohttp_statuscheck',
      version=read_version(),
      description='baseweb project example from aiohttp',
      platforms=['POSIX'],
      packages=find_packages(),
      package_data={
          '': ['templates/*.html', 'static/*.*']
      },
      include_package_data=True,
      install_requires=requirements,
      zip_safe=False)
