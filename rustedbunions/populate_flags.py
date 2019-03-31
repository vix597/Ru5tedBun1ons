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
    from flags import FlagGenerator

    FLAGS = FlagGenerator.generate_flags()

    for flag in FLAGS.values():
        #pylint: disable=E1101
        search = Flag.objects.filter(flag=flag[0])
        if not search:
            f = Flag()
            f.flag = flag[0]
            f.value = flag[1]
            f.save()
        else:
            print("Not adding flag: '{}'. Already in DB".format(flag[0]))
