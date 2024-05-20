import random
import string

from src.models.pass_config import PasswordConfig


def gen_pass(pass_config: PasswordConfig) -> list[str]:
    all_symbs = ''
    if pass_config.get_use_uppercase():
        all_symbs += string.ascii_uppercase
    if pass_config.get_use_low():
        all_symbs += string.ascii_lowercase
    if pass_config.get_use_nums():
        all_symbs += string.digits
    if pass_config.get_use_other_symb():
        all_symbs += '+-*&$?='  # Можно добавить любые другие символы

    passwords = [''.join(random.choices(all_symbs, k=pass_config.len_pass)) for _ in range(pass_config.num_pass)]
    return passwords


if __name__ == '__main__':
    gen_pass(PasswordConfig())
