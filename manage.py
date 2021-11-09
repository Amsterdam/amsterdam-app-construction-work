#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def source_environment():
    cwd = os.getcwd()
    env_file = os.path.join(cwd, 'env')
    if os.path.isfile(env_file):
        with open(env_file, 'r') as f:
            try:
                lines = f.readlines()
                for line in lines:
                    line = line.replace('\n', '')
                    pair = line.split('=')
                    key = line.split('=')[0]
                    value = "".join([pair[i] for i in range(1, len(pair))])
                    os.environ[key] = value
            except Exception as error:
                print('Caught error in reading enviroment file: {error}'.format(error=error))
                exit(False)
    else:
        print('No environment file found: {env_file}. Hint: set_env.py'.format(env_file=env_file))
        exit(False)


def set_fcm_credentials_location():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '{cwd}/fcm-credentials.json'.format(cwd=os.getcwd())


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amsterdam_app_backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Source environment file (DB settings) if DEBUG=true
    if os.getenv('DEBUG', False) == 'true':
        source_environment()

    # print friendly message for easy access to apidocs
    print('API documentation: http://0.0.0.0:8000/api/v1/apidocs')

    is_testing = 'test' in sys.argv

    if is_testing:
        import coverage
        cov = coverage.coverage(source=['amsterdam_app_api'], omit=['*/tests/*'])
        cov.erase()
        cov.start()

        execute_from_command_line(sys.argv)

        cov.stop()
        cov.save()
        cov.report()
    else:
        # Start the application
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
