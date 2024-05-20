class PasswordConfig:
    def __init__(self,
                 num_pass: int = 10,
                 len_pass: int = 8,
                 use_nums: bool = False,
                 use_other_symb: bool = False,
                 use_uppercase: bool = False,
                 use_low: bool = True):
        self.num_pass = num_pass
        self.len_pass = len_pass
        self.__use_nums = use_nums
        self.__use_other_symb = use_other_symb
        self.__use_uppercase = use_uppercase
        self.__use_low = use_low

    def switch_use_low(self):
        self.__use_low = not self.__use_low
        self.check_pass_config()

    def get_use_low(self) -> bool:
        return self.__use_low

    def switch_use_uppercase(self):
        self.__use_uppercase = not self.__use_uppercase
        self.check_pass_config()

    def get_use_uppercase(self) -> bool:
        return self.__use_uppercase

    def switch_use_other_symb(self):
        self.__use_other_symb = not self.__use_other_symb
        self.check_pass_config()

    def get_use_other_symb(self) -> bool:
        return self.__use_other_symb

    def switch_use_nums(self):
        self.__use_nums = not self.__use_nums
        self.check_pass_config()

    def get_use_nums(self) -> bool:
        return self.__use_nums

    def check_pass_config(self):
        if not self.get_use_nums() \
                and not self.get_use_other_symb() \
                and not self.get_use_uppercase() \
                and not self.get_use_low():
            self.__use_low = True
