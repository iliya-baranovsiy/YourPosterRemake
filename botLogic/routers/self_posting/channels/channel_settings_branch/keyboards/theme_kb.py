from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from business_logic.services.channels_service.options.options import PostTheme
from botLogic.common_bot_tools.callback_data import ThemeCb, ChannelCb, ChannelSettingsCb


def get_theme_kb(channel_id: int, theme: PostTheme):
    kb = [
        [
            InlineKeyboardButton(text="🎮 Игры",
                                 callback_data=ThemeCb(
                                     action="set",
                                     channel_id=channel_id,
                                     theme=f"{theme.GAMES_NEWS.kb_value}",
                                 ).pack()
                                 ),
            InlineKeyboardButton(text="🤖 ИИ",
                                 callback_data=ThemeCb(
                                     action="set",
                                     channel_id=channel_id,
                                     theme=f"{theme.AI_POSTS.kb_value}",
                                 ).pack()
                                 ),
        ],
        [
            InlineKeyboardButton(text="💻 IT",
                                 callback_data=ThemeCb(
                                     action="set",
                                     channel_id=channel_id,
                                     theme=f"{theme.IT_NEWS.kb_value}",
                                 ).pack()
                                 ),
            InlineKeyboardButton(text="₿ Криптовалюты",
                                 callback_data=ThemeCb(
                                     action="set",
                                     channel_id=channel_id,
                                     theme=f"{theme.CRYPTO_NEWS.kb_value}",
                                 ).pack()),
        ],
        [
            InlineKeyboardButton(text="🌍 Мир",
                                 callback_data=ThemeCb(
                                     action="set",
                                     channel_id=channel_id,
                                     theme=f"{theme.WORLD_NEWS.kb_value}",
                                 ).pack()),
            InlineKeyboardButton(text="🎬 Шоу-бизнес",
                                 callback_data=ThemeCb(
                                     action="set",
                                     channel_id=channel_id,
                                     theme=f"{theme.SHOW_BIS_NEWS.kb_value}",
                                 ).pack()
                                 ),
        ],
        [
            InlineKeyboardButton(text="⚽ Спорт",
                                 callback_data=ThemeCb(
                                     action="set",
                                     channel_id=channel_id,
                                     theme=f"{theme.SPORT_NEWS.kb_value}",
                                 ).pack()
                                 ),
            InlineKeyboardButton(text="🔬 Наука",
                                 callback_data=ThemeCb(
                                     action="set",
                                     channel_id=channel_id,
                                     theme=f"{theme.SCIENCE_NEWS.kb_value}",
                                 ).pack()),
        ],
        [InlineKeyboardButton(text="◀️ Назад",
                              callback_data=ChannelSettingsCb(
                                  channel_id=channel_id,
                                  action="openMenu", ).pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_back_button_to_settings(channel_id: int):
    kb = [
        [InlineKeyboardButton(text="Назад",
                              callback_data=ChannelSettingsCb(
                                  channel_id=channel_id,
                                  action="openMenu", ).pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
