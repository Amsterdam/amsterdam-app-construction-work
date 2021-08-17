#!/usr/bin/env python3
import string
import random
import os


def create_password():
    while True:
        letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        password = ''.join(random.choice(letters) for _ in range(8))
        if any(x.islower() for x in password) and any(x.isupper() for x in password) and any(x.isnumeric() for x in password):
            return password


def questions():
    # DATABASE NAME
    while True:
        try:
            random_password = create_password()

            postgres_database = input('Please enter your POSTGRES database (default: amsterdam_app_backend): ') or 'amsterdam_app_backend'
            postgres_user = input('Please enter your POSTGRES username (default: backend): ') or 'backend'
            postgres_password = input('Please enter your POSTGRES password (use: {random_password}): '.format(random_password=random_password)) or random_password
            satisfied = input('Save values to environment? (Y/N/A(bort)): ') or 'n'
            if satisfied.lower() in ['y', 'a']:
                if satisfied.lower() == 'y':
                    path = '{cwd}/env'.format(cwd=os.getcwd())
                    with open(path, 'w') as f:
                        f.write('POSTGRES_PASSWORD={postgres_password}\n'.format(postgres_password=postgres_password))
                        f.write('POSTGRES_USER={postgres_user}\n'.format(postgres_user=postgres_user))
                        f.write('POSTGRES_DB={postgres_database}\n'.format(postgres_database=postgres_database))
                    print('Environment written to: {path}'.format(path=path))
                    return
                else:
                    raise(KeyboardInterrupt)
        except KeyboardInterrupt:
            print('Aborted, nothing is saved.')
            return
        except Exception as error:
            print('Caught error: {error}'.format(error=error))
            print('Aborted, nothing is saved.')
            return


questions()
