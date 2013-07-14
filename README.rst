restdns-cli
===========

A Command Line Interface for `Restdns <https://github.com/NaPs/restdns>`_.


Setup
-----

The fastest and more common way to install restdns-cli is using pip::

    pip install restdns-cli


Debian
~~~~~~

If you use Debian Wheezy, you can also use the Tecknet repositories. Add theses
lines in your ``/etc/apt/source.list`` file::

    deb http://debian.tecknet.org/debian wheezy tecknet
    deb-src http://debian.tecknet.org/debian wheezy tecknet

Add the Tecknet repositories key in your keyring:

    # wget http://debian.tecknet.org/debian/public.key -O - | apt-key add -

Then, update and install the ``restdns-cli`` package::

    # aptitude update
    # aptitude install restdns-cli


Tutorial
--------


Legal
-----

restdns-cli is released under MIT license, copyright 2013 Antoine Millet.


Contribute
----------

You can send your pull-request for restdns-cli through Github:

    https://github.com/NaPs/restdns-cli

I also accept well formatted git patches sent by email.

Feel free to contact me for any question/suggestion/patch: <antoine@inaps.org>.
