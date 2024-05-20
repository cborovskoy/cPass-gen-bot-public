import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.config import load_config
from src.handlers import main_handler

logging.basicConfig(level=logging.ERROR)


async def main():
    config = load_config()
    bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    dp.include_routers(main_handler.router)

    # Запускаем бота и пропускаем все накопленные входящие
    await bot.send_message(chat_id=config.admin_id, text='🚀 Bot was started!')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
