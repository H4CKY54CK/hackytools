from setuptools import setup, Extension
import hackytools

PACKAGE_NAME = hackytools.__package_name__
VERSION =  hackytools.__version__

with open('README.md') as f:
    README = f.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    url="https://github.com/H4CKY54CK/hackytools",
    license="MIT License",
    description="Tools that are hacky. Obviously.",
    long_description=README,
    long_description_content_type="text/markdown",
    author='Hackysack',
    author_email='tk13xr37@gmail.com',
    packages=['hackytools'],
    # tests_require=['pytest'],
    # install_requires=['pillow'],
    python_requires='>=3.6',
    entry_points={'console_scripts':
        [
            'fetchip = hackytools.netutils:main',
            'sysutils = hackytools.sysutils:main',
        ]
    }
)
