from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.models.pass_config import PasswordConfig


def get_checkbox(value: bool) -> str:
    return '☑️' if value else '🔲️'


def get_kb_for_main_menu(pass_config: PasswordConfig) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=' 🔄 Новые', callback_data='new'),
                InlineKeyboardButton(text=' 💾 Сохранить', callback_data='save'))

    builder.row(*[InlineKeyboardButton(text=f'·{t} Симв·' if pass_config.len_pass == t else f'{t} Симв',
                                       callback_data=f'len_{t}') for t in [8, 12, 16, 24]])

    builder.row(InlineKeyboardButton(text=f'{get_checkbox(pass_config.get_use_uppercase())} Прописные',
                                     callback_data='upper'),
                InlineKeyboardButton(text=f'{get_checkbox(pass_config.get_use_low())} Строчные',
                                     callback_data='lower'))

    builder.row(InlineKeyboardButton(text=f'{get_checkbox(pass_config.get_use_nums())} Цифры',
                                     callback_data='num'),
                InlineKeyboardButton(text=f'{get_checkbox(pass_config.get_use_other_symb())} Спецсимволы',
                                     callback_data='other_symb'))

    return builder.as_markup()
