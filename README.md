# hypermatix64

Hypermatix64 will be a graphical interface for automating the installation
of the most commonly requested applications for Ubuntu. In the future,
various other Linux distributions will be supported. (Actually, although
the program is intended for beginners to Linux and as such is planned
to target Ubuntu in its first release, development is currently
taking place on Arch to preserve my own sanity.)

It is a graphical frontend for traditional package managers intended
to abstract away the need for the user to deal with 3rd-party repos
- just select the wanted application and press a button to install
it. It will be written entirely in Python.

It is based on the Automatix2 and Ultamatix projects, with various
modifications to fix some of the dangerous mistakes made by those
projects. Most notably, the Bash backend will be entirely replaced
with an additional Python component for interfacing with different
package managers, allowing the program to manage packages more
flexibly and remove packages safely (uninstalling an option will
ONLY remove dependencies which were both installed because of that
option and are not needed by anything else).

It is completely useless in its current state, with parts of the old
backend rooted out already with nothing to replace them yet. I'm working
on it.