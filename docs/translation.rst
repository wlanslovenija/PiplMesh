Translation of PiplMesh
=======================

Making strings translatable
---------------------------

All strings which do you want to be translated must be marked translatabe,
in Django template like: ``{% trans "Some string" %}``,
in Python files like: ``_("some string")``.
   
Creation of translation files
-----------------------------
   
.. warning:: It is important to run folowing commands from repository root directory!

Add your wanted language in ``settings.py`` under ``LANGUAGES``, make sure that in your Django applications
you want translated there is a directory called ``locale``, if not you should make one.

When all string are marked for translation and settings are prepared run command::

    ./manage.py makemessages -l <language code>
    
*(You should replace <language code> with your preferred language code).* 
Example for Slovenian language::
   
    ./manage.py -l sl
   
This will create file ``django.po`` under ``locale/sl/LC_MESSAGES/``
*(note: All other Directories are automaticly created.)*

Translation
-----------

Open file ``django.po`` with text editor or with special translation tool (Poedit_ for eaxmple)
and tranlate strings. Original string is named ``msgid "Some string"`` and under it
is ``msgstr`` which contains empty string where you should write your translation.

.. _Poedit: http://www.poedit.net/

Compiling translation files
---------------------------

After you are done translating run the command::

     ./manage.py compilemessages
       
and a new file ``django.mo`` will be created.
   
Translated strings should now be available in PiplMesh.
