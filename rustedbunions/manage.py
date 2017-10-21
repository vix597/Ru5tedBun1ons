#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    from rustedbunions import settings
    if not os.path.exists(settings.CRAPDB_PATH):
        print("Run setup_site.sh first to create the crapdb.sqlite3 file and set permissions")
        sys.exit(1)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rustedbunions.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    execute_from_command_line(sys.argv)
