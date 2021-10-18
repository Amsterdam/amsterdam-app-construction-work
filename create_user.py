import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amsterdam_app_backend.settings")
from django.contrib.auth import get_user_model
import django
django.setup()


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


def create_user():
    source_environment()

    UserModel = get_user_model()
    username = os.getenv('WEB_USERNAME')
    password = os.getenv('WEB_PASSWORD')
    print(username, password)

    if not UserModel.objects.filter(username=username).exists():
        user = UserModel.objects.create_user(username, password=password)
        user.is_superuser = False
        user.is_staff = True
        user.save()


if __name__ == '__main__':
    create_user()
