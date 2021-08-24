#!/usr/bin/env python3
import string
import random
import os


class SetEnv:
    """ Simple script to create a Docker environment file for setting the DB credentials
    """
    @staticmethod
    def weak(password):
        if len(password) > 7 and any(x.islower() for x in password) and any(x.isupper() for x in password) and any(x.isnumeric() for x in password):
            return False
        return True

    def create_password(self):
        # Create a password with at least one digit, one uppercase and one lowercase letter and a total length of 8
        while True:
            letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
            password = ''.join(random.choice(letters) for _ in range(8))
            if self.weak(password) is False:
                return password

    def questions(self):
        path = '{cwd}/env'.format(cwd=os.getcwd())
        try:
            # check if credentials exist and ask permission to override them
            satisfied = ''
            while satisfied.lower() not in ['y', 'n', 'a']:
                if os.path.isfile(path):
                    satisfied = input('Database credential files already exist! Do you wish to override them? (Y/N/A(bort)): ') or 'n'
                    if satisfied.lower() == 'y':
                        pass
                    elif satisfied.lower() in ['n', 'a']:
                        raise KeyboardInterrupt
                else:
                    satisfied = 'y'

            # get/set credentials
            while True:
                random_password = self.create_password()

                postgres_database = input('Please enter your POSTGRES database (default: amsterdam_app_backend): ') or 'amsterdam_app_backend'
                postgres_user = input('Please enter your POSTGRES username (default: backend): ') or 'backend'
                postgres_password = input('Please enter your POSTGRES password (or use: {random_password}): '.format(random_password=random_password)) or random_password
                if self.weak(postgres_password) is True:
                    print('Warning: You\'re using a weak password!')
                satisfied = input('Save values to environment? (Y/N/A(bort)): ') or 'n'
                if satisfied.lower() in ['y', 'a']:
                    if satisfied.lower() == 'y':
                        with open(path, 'w') as f:
                            f.write('POSTGRES_PASSWORD={postgres_password}\n'.format(postgres_password=postgres_password))
                            f.write('POSTGRES_USER={postgres_user}\n'.format(postgres_user=postgres_user))
                            f.write('POSTGRES_DB={postgres_database}\n'.format(postgres_database=postgres_database))
                        print('Environment written to: {path}'.format(path=path))
                        return
                    else:
                        raise KeyboardInterrupt
        except KeyboardInterrupt:
            print('Aborted, nothing is saved.')
        except Exception as error:
            print('Caught error: {error}'.format(error=error))
            print('Aborted, nothing is saved.')


if __name__ == '__main__':
    setenv = SetEnv()
    setenv.questions()
