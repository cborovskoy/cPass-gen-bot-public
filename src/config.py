from dataclasses import dataclass
from pathlib import PurePath, Path
import configparser


@dataclass
class Config:
    bot_token: str
    admin_id: int


def load_config(path=None):
    path = PurePath(Path(__file__).parents[1], 'bot.ini') if path is None else path
    config = configparser.ConfigParser()
    config.read(path)
    config = config['DEFAULT']

    return Config(bot_token=config.get("tg_token"), admin_id=int(config.get("admin")))
