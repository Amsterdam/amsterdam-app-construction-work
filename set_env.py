#!/usr/bin/env python3
""" Setup environment file for new backend """
import string
import random
import os


class SetEnv:
    """ Simple script to create a Docker environment file for setting the DB credentials
    """
    @staticmethod
    def weak(password):
        """ Check strength of password """
        if len(password) > 7 and \
                any(x.islower() for x in password) and \
                any(x.isupper() for x in password) and \
                any(x.isnumeric() for x in password):
            return False

        return True

    def create_password(self):
        """ Create a password with at least one digit, one uppercase and one lowercase letter and a total length of 8
        """
        while True:
            letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
            password = ''.join(random.choice(letters) for _ in range(8))
            if self.weak(password) is False:
                return password

    def questions(self):
        """ Questionare for the environment file """
        path = '{cwd}/env'.format(cwd=os.getcwd())
        try:
            # check if credentials exist and ask permission to override them
            satisfied = ''
            while satisfied.lower() not in ['y', 'n', 'a']:
                if os.path.isfile(path):
                    satisfied = input('Warning: credential files already exist! '
                                      'Do you wish to override them? (Y/N/A(bort)): ') or 'n'
                    if satisfied.lower() == 'y':
                        pass
                    elif satisfied.lower() in ['n', 'a']:
                        raise KeyboardInterrupt
                else:
                    satisfied = 'y'

            # get/set credentials
            while True:
                random_psql_password = self.create_password()
                random_web_password = self.create_password()
                postgres_database = input('Please enter your POSTGRES database (default: amsterdam_app_backend): ') \
                                    or 'amsterdam_app_backend'
                postgres_user = input('Please enter your POSTGRES username (default: backend): ') or 'backend'
                postgres_password = input(f'Please enter your POSTGRES password (or use: {random_psql_password}): ') \
                                    or random_psql_password
                web_username = input('Please enter your WEB username (default: redactie@amsterdam.nl): ') \
                               or 'redactie@amsterdam.nl'
                web_password = input(f'Please enter your WEB password (or use: {random_web_password}): ') \
                               or random_web_password
                app_token = input('Please enter you Secret APP token')
                aes_secret = input('Please enter you AES secret')

                if self.weak(postgres_password) is True:
                    print('Warning: You\'re using a weak database password!')
                if self.weak(web_password) is True:
                    print('Warning: You\'re using a weak web user password!')

                satisfied = input('Save values to environment? (Y/N/A(bort)): ') or 'n'
                if satisfied.lower() in ['y', 'a']:
                    if satisfied.lower() == 'y':
                        with open(path, 'w') as f:
                            f.write(f'POSTGRES_PASSWORD={postgres_password}\n')
                            f.write(f'POSTGRES_USER={postgres_user}\n')
                            f.write(f'POSTGRES_DB={postgres_database}\n')
                            f.write(f'WEB_USERNAME={web_username}\n')
                            f.write(f'WEB_PASSWORD={web_password}\n')
                            f.write(f'APP_TOKEN={app_token}\n')
                            f.write(f'AES_SECRET={aes_secret}\n')
                        print('Environment written to: {path}'.format(path=path))
                        return
                    raise KeyboardInterrupt
        except KeyboardInterrupt:
            print('Aborted, nothing is saved.')
        except Exception as error:
            print('Caught error: {error}'.format(error=error))
            print('Aborted, nothing is saved.')


if __name__ == '__main__':
    setenv = SetEnv()
    setenv.questions()
