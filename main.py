import random

SYMB_OTHER = '+-*&$?=<>'
SYMB_NUMS = '123456789'
SYMB_LETTERS_UP = 'ABCDEFGHIJKLMNPQRSTUVWXYZ'
SYMB_LETTERS_LOW = 'abcdefghijklmnopqrstuvwxyz'


def gen_pass(num_pass=10, len_pass=8, use_nums=False, use_other_symb=False, use_uppercase=False, use_low=True):
    all_symbs = SYMB_LETTERS_LOW if use_low else ''
    all_symbs += SYMB_NUMS if use_nums else ''
    all_symbs += SYMB_LETTERS_UP if use_uppercase else ''
    all_symbs += SYMB_OTHER if use_other_symb else ''

    pass_lst = []

    for _ in range(num_pass):
        password = ''
        for i in range(len_pass):
            password += random.choice(all_symbs)

        pass_lst.append(password)

    reply_txt = '\n\n'.join(pass_lst)

    return reply_txt


if __name__ == '__main__':
    gen_pass(num_pass=10,
             len_pass=10,
             use_nums=True,
             use_other_symb=True,
             use_uppercase=True)
