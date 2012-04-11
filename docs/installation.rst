Installation
============

The procedure of installing and running your own instance of PiplMesh follows.

*Note: we are assuming that you are running an UNIX-like operating system.*

Warning Regarding Database Backend
----------------------------------

PiplMesh assumes working support for transactional savepoints in the database
backend. **This is only supported in PostgreSQL version 8.0 or higher** and
therefore this is the only database that is supported by PiplMesh.

**The system will still work with MySQL and SQLite but some features regarding
error handling and validation may cause unexpected results and even data
corruption!** Do not use them for production deployment. You have been warned.

Prerequisites
-------------

In addition to Python_ and a Django-supported_ relation database system the
following is required on the system to run PiplMesh:

* Python virtualenv_ package
* Python pip_ package (1.0+)
.. _Python: http://python.org/
.. _Django-supported: https://docs.djangoproject.com/en/1.3/ref/databases/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _pip: http://pypi.python.org/pypi/pip
.. _MongoDB: http://www.mongodb.org/

Other prerequisites (Python packages) are installed later.

Getting Source
--------------

Use ``master`` branch which contains stable PiplMesh source from the project
git_ repository. Get it using this command::

    git clone https://github.com/mitar/PiplMesh.git

If you are not familiar with git_, please refer to its tutorial_.

.. _git: http://git-scm.com/
.. _tutorial: http://schacon.github.com/git/gittutorial.html

Development/Testing Instance
----------------------------

Deploying
^^^^^^^^^
	
Once you have all prerequisites and PiplMesh itself, you can create Python
virtualenv_ for PiplMesh::

    virtualenv --no-site-packages env_piplmesh
    source env_piplmesh/bin/activate

This will create a local virtualenv directory named ``env_piplmesh`` in your
current working directory. Once you have made it, you can install Python
packages into using pip_::

    pip install -r requirements.txt

This will install all required Python packages into a local virtualenv
directory. Afterwards, you have to initialize the database. Run the following
``manage.py`` command from the ``piplmesh`` subdirectory::

    ./manage.py syncdb

More about above ``manage.py`` command can be read in `Django documentation`_.

.. _Django documentation: https://docs.djangoproject.com/en/1.3/ref/django-admin/

Running
^^^^^^^

Run the following::

    ./manage.py runserver

PiplMesh is now available at http://localhost:8000/.

More about Django development server in its `documentation`_.

.. _documentation: https://docs.djangoproject.com/en/1.3/intro/tutorial01/#the-development-server

Platform Specific Instructions
------------------------------

Mac OS X
^^^^^^^^

Prerequisites can be installed with MacPorts_ or Homebrew_. For MacPorts::

    sudo port install py27-virtualenv py27-pip

For Homebrew, install Python_, pip_, and virtualenv_::

    brew install python --universal --framework
    brew install pip
    pip install virtualenv

.. _MacPorts: http://www.macports.org/
.. _Homebrew: http://mxcl.github.com/homebrew/

Installing mongoDB

The easiest way to install MongoDB is to use a package manager or the pre-built binaries:

	OSX - Homebrew::
		$ brew update
		$ brew install mongodb
	OSX - MacPorts::
		$ sudo port install mongodb
		
By default MongoDB will store data in /data/db, but it won't automatically create that directory. To create it, do:
	OSX::
		$ sudo mkdir -p /data/db/
		$ sudo chown `id -u` /data/db

	Run the server:		
		$ mongod

	Connect to server:
		$ mongo


Debian
^^^^^^

The following Debian packages are needed:

* ``python-virtualenv``
* ``python-pip``
* ``mongodb-10gen``
Be careful about required versions. It could be necessary to use packages from Debian testing or backports distribution.

Installing MongoDB in debian:

DEBIAN (Ubuntu)::
	sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
	sudo add-apt-repository 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen'
	sudo apt-get update 
	sudo apt-get install mongodb-10gen


