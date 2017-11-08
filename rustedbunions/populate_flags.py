'''
Adds the flags to the database
'''
import os

if __name__ == "__main__":
    # Must be set before accessing settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rustedbunions.settings")

    import django

    django.setup()

    from core.models import Flag
    from flags import FLAGS

    # TODO: Don't add duplicate flags

    for flag in FLAGS.values():
        f = Flag()
        f.flag = flag[0]
        f.value = flag[1]
        f.save()
