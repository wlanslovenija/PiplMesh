Translation
===========

Making strings translatable
---------------------------

To make your strings translatable edit them as follows:

* in Django templates: ``{% trans "Some string" %}``
* in Python files: ``_("some string")``
* in JavaScript files: ``gettext("some string")``
   
Creation of translation files
-----------------------------
   
.. warning:: It is important to run folowing commands from repository root directory!

Add your wanted language(s) in ``settings.py`` under ``LANGUAGES`` and make
sure your Django applications you want translated have a directory called
``locale`` (if not, you should create one).

When all string are marked for translation and settings are prepared run
command::

    ../manage.py makemessages -l <language code>
    ../manage.py makemessages -l <language code> -d djangojs

*(You should replace <language code> with your preferred language code).*
Example for Slovenian language::

    ../manage.py makemessages -l sl
    ../manage.py makemessages -l sl -d djangojs

This will create file ``django.po`` under ``locale/sl/LC_MESSAGES/``
*(note: All other Directories are automaticly created.)*

Translation
-----------

Open file ``django.po`` with text editor or with special translation tool
(Poedit_ for example) and translate strings. Original string is named ``msgid
"Some string"`` and under it there is ``msgstr`` which contains an empty string
where you should write your translation.

.. _Poedit: http://www.poedit.net/

Compiling translation files
---------------------------

After you are done translating run the command::

     ../manage.py compilemessages
       
and a new file ``django.mo`` will be created.
   
Translated strings should now be available in PiplMesh.

Troubleshooting
---------------

You should really read `documentation on translation in Django`_, but here are
some troubleshooting notes:

* you need ``gettext`` installed (see `instructions for Windows`_)
* sometimes it is necessary to restart development HTTP server to get new
  compiled translations to work
* yes, you have to compile ``.po`` files into ``.mo`` files after you edit ``.po`` files
* verify changes to ``.po`` files and make sure that not whole files are changed just
  because your ``gettext`` changed ``/`` into ``\``, manually clean/revert such changes

.. _documentation on translation in Django: https://docs.djangoproject.com/en/dev/topics/i18n/
.. _instructions for Windows: https://docs.djangoproject.com/en/dev/topics/i18n/translation/#gettext-on-windows
