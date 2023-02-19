#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
#
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'app_core_dressdrive.settings')

    default_addr = '0.0.0.0'
    default_port = '8000'
    default_url = f"{default_addr}:{default_port}"

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if len(sys.argv) == 2 and "runserver" in sys.argv:
        execute_from_command_line(
            sys.argv + [default_url]
        )
    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
