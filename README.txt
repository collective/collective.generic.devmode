Introduction
============

This provide a script ``cg.devmode`` which can do some actions on a zope instance.

The main use is when you grab the production datafs, you 'll need to sanitize the content a little.
The sanitization include changing all passwords and all emails at once.

Another use is for running scripts without any security (we just give us all rights ;))

.. contents::

Svn : http://svn.plone.org/svn/collective/collective.generic.devmode/trunk/


Actions & usage
==================

Changing all email for all users:
-------------------------------------
::

    ./bin/cg.devmode -m --mail=some@mail.foo

Changing all passwords
------------------------------
::

    ./bin/cg.devmode -p  --password=secret

Changing the administrator password
-----------------------------------------
::

    ./bin/cg.devmode -a  --password=secret



Running a script with all security stuff removed
---------------------------------------------------
::

    ./bin/cg.devmode -r --script=</path/to/file.py>  [--script-args="String"] # equivalent of ./bin/instance run toto.py String except for security


Modifiers
============

Running with debug
-----------------------
::

    ./bin/cg.devmode -v [ARGS]


Giving an alternative zope configuration file
--------------------------------------------------
::

    ./bin/cg.devmode -c <CONFIGGILE>

Specifying the plone site id
--------------------------------
::

    ./bin/cg.devmode -l <PLONE_SITE_ID>

Specifying the admin user
------------------------------
::

    ./bin/cg.devmode --user <ADMIN_USER>



