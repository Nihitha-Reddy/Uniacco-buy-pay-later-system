
#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bnpl_system.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # If the error is due to a missing Django package, we'll raise an ImportError with a helpful message.
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

if __name__ == '__main__':
    main()
