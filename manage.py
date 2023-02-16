#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def source_environment():
    """ Source environment file """
    cwd = os.getcwd()
    env_file = os.path.join(cwd, 'env')
    if os.path.isfile(env_file):
        with open(env_file, 'r') as f:
            try:
                lines = f.readlines()
                for line in lines:
                    line = line.replace('\n', '')
                    pair = line.split('=', 1)
                    key = pair[0]
                    value = pair[1]
                    os.environ[key] = value
            except Exception as error:
                print(f'Caught error in reading enviroment file: {error}')
                sys.exit(False)
    else:
        print(f'No environment file found: {env_file}. Hint: set_env.py')
        sys.exit(False)


def set_fcm_credentials_location():
    """ Source fcm"""
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'{os.getcwd()}/fcm-credentials.json'


def main():
    """ Run administrative tasks. """
    is_testing = 'test' in sys.argv
    if is_testing:
        os.environ['DEBUG'] = 'true'

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
    if os.getenv('DEBUG', 'false') == 'true':
        source_environment()

    # print friendly message for easy access to apidocs
    print('API documentation: http://0.0.0.0:8000/api/v1/apidocs')

    if is_testing:
        os.environ['AES_SECRET'] = 'aes_mock_secret'
        os.environ['APP_TOKEN'] = 'app_mock_token'

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
