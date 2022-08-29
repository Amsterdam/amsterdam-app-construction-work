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


def create_users():
    source_environment()

    model = get_user_model()
    webuser = os.getenv('WEB_USERNAME')
    webpass = os.getenv('WEB_PASSWORD')
    teamuser = os.getenv('TEAM_USERNAME')
    teampass = os.getenv('TEAM_PASSWORD')

    users = [[webuser, webpass], [teamuser, teampass]]

    for user in users:
        if not model.objects.filter(username=user[0]).exists():
            account = model.objects.create_user(user[0], password=user[1])
            account.is_superuser = False
            account.is_staff = True
            account.save()


if __name__ == '__main__':
    create_users()
