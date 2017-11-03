#!/usr/bin/env python
import os
import sys
import threading

if __name__ == "__main__":
    # Must be set before accessing settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rustedbunions.settings")

    from rustedbunions import settings
    if not os.path.exists(settings.CRAPDB_PATH) and "runserver" in sys.argv:
        print("Run setup_site.sh first to create the crapdb.sqlite3 file and set permissions")
        sys.exit(1)

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

    # Loads initial data for Session
    from core.session import Session

    needs_cleanup = False
    if "runserver" in sys.argv and not settings.DEBUG:
        # Only bother with this in production
        thread = threading.Thread(target=Session.cleanup)
        thread.start()
        needs_cleanup = True

    execute_from_command_line(sys.argv)

    if needs_cleanup:
        # App exiting
        Session.CLEANUP_EVENT.set()
        print("Waiting up to 5 minutes for thread to finish...")
        thread.join(timeout=300)
