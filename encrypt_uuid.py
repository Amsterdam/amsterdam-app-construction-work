"""Encrypt UUID with AES tool"""

#!/usr/bin/env python
import os
import sys
import uuid

from construction_work.generic_functions.aes_cipher import AESCipher


def source_environment():
    """Source environment file"""
    cwd = os.getcwd()
    env_file = os.path.join(cwd, "env")
    if os.path.isfile(env_file):
        with open(env_file, "r") as f:
            try:
                lines = f.readlines()
                for line in lines:
                    line = line.replace("\n", "")
                    pair = line.split("=", 1)
                    key = pair[0]
                    value = pair[1]
                    os.environ[key] = value
            except Exception as error:
                print(f"Caught error in reading enviroment file: {error}")
                sys.exit(False)
    else:
        print(f"No environment file found: {env_file}. Hint: set_env.py")
        sys.exit(False)


source_environment()

AES_SECRET = os.getenv("AES_SECRET")
print(f"Given secret: {AES_SECRET}")

APP_TOKEN = os.getenv("APP_TOKEN")
if APP_TOKEN is None:
    print("No APP_TOKEN env var found, creating new one:")
    APP_TOKEN = str(uuid.uuid4())
print(f"Given UUID: {APP_TOKEN}")

aes = AESCipher(APP_TOKEN, AES_SECRET)
print("\n")
print(aes.encrypt())
