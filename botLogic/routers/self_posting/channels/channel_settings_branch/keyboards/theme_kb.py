from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from business_logic.services.channels_service.options.options import PostTheme


def get_theme_kb(channel_id: int, theme: PostTheme):
    kb = [
        [
            InlineKeyboardButton(text="Игры", callback_data=f"settheme_{theme.GAMES_NEWS.kb_value}_{channel_id}"),
            InlineKeyboardButton(text="ИИ", callback_data=f"settheme_{theme.AI_POSTS.kb_value}_{channel_id}"),
        ],
        [
            InlineKeyboardButton(text="IT", callback_data=f"settheme_{theme.IT_NEWS.kb_value}_{channel_id}"),
            InlineKeyboardButton(text="Криптовалюта",
                                 callback_data=f"settheme_{theme.CRYPTO_NEWS.kb_value}_{channel_id}"),
        ],
        [
            InlineKeyboardButton(text="Новости мира",
                                 callback_data=f"settheme_{theme.WORLD_NEWS.kb_value}_{channel_id}"),
            InlineKeyboardButton(text="Шоу бизнес",
                                 callback_data=f"settheme_{theme.SHOW_BIS_NEWS.kb_value}_{channel_id}"),
        ],
        [
            InlineKeyboardButton(text="Спорт", callback_data=f"settheme_{theme.SPORT_NEWS.kb_value}_{channel_id}"),
            InlineKeyboardButton(text="Наука", callback_data=f"settheme_{theme.SCIENCE_NEWS.kb_value}_{channel_id}"),
        ],
        [InlineKeyboardButton(text="Назад", callback_data=f"settings_{channel_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_back_button_to_settings(channel_id: int):
    kb = [
        [InlineKeyboardButton(text="Назад", callback_data=f"settings_{channel_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
