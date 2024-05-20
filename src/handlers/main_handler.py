from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.models.pass_config import PasswordConfig
from src.utils.gen_pass import gen_pass
from src.utils.keyboards import get_kb_for_main_menu

router = Router()


async def send_main_menu(bot: Bot, chat_id: int, state: FSMContext, bot_msg_to_edit: Message = None):
    state_data = await state.get_data()
    pass_config = state_data.get('pass_config', PasswordConfig())
    await state.update_data(pass_config=pass_config)

    passwords = gen_pass(pass_config=pass_config)
    text = '\n\n'.join(passwords)
    kb = get_kb_for_main_menu(pass_config=pass_config)

    if bot_msg_to_edit:
        await bot_msg_to_edit.edit_text(text=text, reply_markup=kb)
    else:
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=kb)


@router.message()
async def user_msg_handler(message: Message, state: FSMContext):
    await send_main_menu(bot=message.bot, chat_id=message.from_user.id, state=state)


@router.callback_query()
async def main_menu_btn_handler(callback: CallbackQuery, state: FSMContext):
    bot = callback.bot
    chat_id = callback.from_user.id
    bot_msg = callback.message

    state_data = await state.get_data()
    pass_config = state_data.get('pass_config', PasswordConfig())
    await state.update_data(pass_config=pass_config)

    if callback.data == 'new':
        await send_main_menu(bot=bot, chat_id=chat_id, state=state, bot_msg_to_edit=bot_msg)

    elif callback.data == 'save':
        await callback.message.delete_reply_markup()
        await send_main_menu(bot=bot, chat_id=chat_id, state=state)

    elif callback.data.startswith('len_') and callback.data.split('_')[-1].isdigit():
        pass_config.len_pass = int(callback.data.split('_')[-1])
        await state.update_data(pass_config=pass_config)
        await send_main_menu(bot=bot, chat_id=chat_id, state=state, bot_msg_to_edit=bot_msg)

    elif callback.data == 'upper':
        pass_config.switch_use_uppercase()
        await state.update_data(pass_config=pass_config)
        await send_main_menu(bot=bot, chat_id=chat_id, state=state, bot_msg_to_edit=bot_msg)

    elif callback.data == 'lower':
        pass_config.switch_use_low()
        await state.update_data(pass_config=pass_config)
        await send_main_menu(bot=bot, chat_id=chat_id, state=state, bot_msg_to_edit=bot_msg)

    elif callback.data == 'num':
        pass_config.switch_use_nums()
        await state.update_data(pass_config=pass_config)
        await send_main_menu(bot=bot, chat_id=chat_id, state=state, bot_msg_to_edit=bot_msg)

    elif callback.data == 'other_symb':
        pass_config.switch_use_other_symb()
        await state.update_data(pass_config=pass_config)
        await send_main_menu(bot=bot, chat_id=chat_id, state=state, bot_msg_to_edit=bot_msg)
