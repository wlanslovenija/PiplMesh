TRANSLATION OF DJANGO APPLICATION:


1. All strings which do you want to be translated must be marked translatabe,
   in django template like: {% trans "Some string" %},
   in python files like: _("some string").
   
2. It is important to run folowing commands from application root folder!

3. Add your wanted language in settings.py under LANGUAGES, and check if there is folder
   in root of application called "locale", if not you should make one.

4. When all strings and settings are prepared run command ./manage.py makemessages -l "language_code"
   (You should replace "language_code" with your preferred language code).
   Example for Slovenian language: ./manage.py -l sl
   This will create file "djnago.po" under "locale/sl/LC_MESSAGES/" 
   (All other subfolders are automaticly created.)

5. Open file "django.po" with text editor or with special translation tool (Poedit for eaxmple)
   and tranlate strings. Original string is named msgid "Some string" and under it
   is msgstr which contains empty string where you should write your translation.

6. After you are done translating run the command ./manage.py compilemessages and a new file "django.mo"
   will be created.
   
7. Use your language in the application. :)