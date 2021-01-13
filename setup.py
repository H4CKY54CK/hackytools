import re
from setuptools import find_packages, setup
import os

HERE = os.path.abspath(os.path.dirname(__file__))
PACKAGE_NAME = 'hackytools'

with open(os.path.join(HERE, PACKAGE_NAME, "__init__.py"), encoding="utf-8") as fp:
    VERSION = re.search(r'''_*version_* *= *['|"](\d+(\.\d/*)*\w*)['|"]''', fp.read()).group(1)

with open('README.md') as f:
    README = f.read()

setup(name=PACKAGE_NAME,
      version=VERSION,
      url="https://github.com/H4CKY54CK/hackytools",
      license="MIT License",
      description="Tools that are hacky. Obviously.",
      long_description=README,
      long_description_content_type="text/markdown",
      author='Hackysack',
      author_email='tk13xr37@gmail.com',
      packages=find_packages(exclude=[]),
      install_requires=['speedtest-cli', 'pillow<=8.0.1'],
      python_requires='>=3.6',
      entry_points={'console_scripts':
        [
            'bork = hackytools.cli:main',
            'whatsmyip = hackytools.cli:main',
            'whatsmyspeed = hackytools.cli:main',
            'spriteit = hackytools.cli:main',
            'gifit = hackytools.cli:main',
        ]
      })
