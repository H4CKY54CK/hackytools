Change Log
==========

Unreleased
----------

**Added**

* New function measurement decorator `perf`. It is far more efficient in it's measurements than the other two, but I believe all three function timers each serve their own purpose.
* New function `readkey` for reading either a single character or a keystroke in the terminal. Does not require sequences to be stored locally. Windows support needs further confirmation.
* Added a test for `ftime` and `ftime_ns`. Yes, that's all the tests we have right now. We'll get there.
* Added many docstrings, where applicable.
* Added Windows support for `sysutils` (formerly known as `bork`).
* Added `fetchip`, to get your IPv4, IPv6, or local IP address at any time (requires internet, of course).

**Changed**

* Completely overhauled the library. This reduced dependencies, cleaned up  unnecessary code, and organized everything.

**Removed**

* `smiter` because it was kind of pointless.

0.2.0 (2021/1/8)
-----------------

**Special Notes**

Due to an accidental overwrite, we're now 0.0.1 version behind. Due to this, we shall increment a minor version (0.1.0), in case there are breaking changes.

**Added**

* Network monitor that can store results in a SQLite3 database file, with many other options. Will be added to the documentation soon.
* Added missing meta-data to package info for PyPi.

**Changed**

* Overhauled the entire CLI system, allowing for a cleaner parsing system. The actual commands haven't changed, but the underlying parser has. This will allow for better organization of the different parts of the parser.
* Changed the extension of `LICENSE` to make it easier for anyone to open and view the contents.

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
