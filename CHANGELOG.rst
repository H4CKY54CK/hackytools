Change Log
==========

Unreleased
----------

0.1.2 (2020/12/29)
-----------------

**Added**

* Added the function `flatten` to the main library, for flattening lists of any nestedness.

**Changed**

* Added a fallback to `bork` in case the usual temperature file does not exist. Still may fail, as not everyone has the package `sensors` on Linux.
* Modified the `whatsmyip` command so that it can get a more consistent local IP, if it's requested.

0.0.6 (2020/10/9)
-----------------

**Added**

* Change Log: `CHANGELOG.rst`
* Spritesheet/stylesheet generator.
* Logging decorator.
* Command line command, `whatsmyip` to output your public IP address.

**Fixed**

* An issue where the timing decorators could possibly return an incorrect converted time. All converted times are now correct.
