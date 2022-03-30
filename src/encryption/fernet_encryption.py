from cryptography.fernet import Fernet

import click


@click.group()
def secure_files():
    pass


@secure_files.command(help="generates a python module with a key inside it")
@click.option("--path", help="path in which to write the .py module containing the key",
              default="fernet_key.py", type=click.Path())
@click.option("--var_name",
              help="the name of the python variable to hold the key inside the module",
              default="key")
def generate_key_module(path="fernet_key.py", var_name="key"):
    key = generate_key_inner()
    with open(path, 'wt') as f:
        line = f"\n{var_name} = '{key}'\n"
        f.writelines([line])


@secure_files.command(help="generate a fernet key and print it")
def generate_key():
    return generate_key_inner()


@secure_files.command(help="encrypt a file and write it to file system")
@click.argument('key')
@click.argument('source_path')
@click.argument('target_path', default=None)
def encrypt_file(key, source_path, target_path=None):
    return encrypt_file_inner(key, source_path, target_path)


@secure_files.command()
@click.argument('key')
@click.argument('source_path')
@click.argument('target_path', default=None)
def decrypt_file(key, source_path, target_path=None):
    return decrypt_file_inner(key, source_path, target_path)


def generate_key_inner():
    key = Fernet.generate_key().decode("utf-8")
    print(key)
    return key


def encrypt_file_inner(key, source_path, target_path=None):
    f = Fernet(key)
    with open(source_path, 'rb') as original_file:
        original = original_file.read()

    encrypted = f.encrypt(original)

    target = target_path or f'{source_path}.safe'
    with open(target, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    return target


def decrypt_file_inner(key, source_path, target_path=None):
    f = Fernet(key)
    with open(source_path, 'rb') as original_file:
        original = original_file.read()

    decrypted = f.decrypt(original)
    if target_path:
        with open(target_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted)

    return decrypted


if __name__ == '__main__':
    secure_files()
