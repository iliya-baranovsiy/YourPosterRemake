from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.payments.options import PaymentOptions
from business_logic.services.channels_service.options.options import PostTheme, Resource


class SettingsKbBuilder:
    def __init__(self, channel_id: int):
        self.kb = []
        self.channel_id = channel_id

    def create_theme_button(self):
        self.kb.append([InlineKeyboardButton(text="Тема поста", callback_data=f"theme_{self.channel_id}")])

    def create_source_button(self):
        self.kb.append([InlineKeyboardButton(text="Сменить ресурс", callback_data=f"sourceChange_{self.channel_id}")])

    def create_load_file_button(self):
        self.kb.append([InlineKeyboardButton(text="Загрузить файл", callback_data=f"loadFile_{self.channel_id}")])

    def create_generate_ai_button(self):
        self.kb.append(
            [InlineKeyboardButton(text="Сгенерировать файл", callback_data=f"generateFile_{self.channel_id}")])

    def create_posts_time_button(self):
        self.kb.append([InlineKeyboardButton(text="Время постов", callback_data=f"timelist_{self.channel_id}")])

    def create_activate_button(self):
        self.kb.append(
            [InlineKeyboardButton(text="Включить автопостинг", callback_data=f"start_selfposting_{self.channel_id}")])

    def create_deactivate_button(self):
        self.kb.append(
            [InlineKeyboardButton(text="Выключить автопостинг",
                                  callback_data=f"deactivate_selfposting_{self.channel_id}")])

    def create_back_button(self):
        self.kb.append([InlineKeyboardButton(text="Назад", callback_data=f"channel_{self.channel_id}")])


class SettingsKb:
    def __init__(self, channel_id: int, payment_plan: PaymentOptions, is_active: bool, theme: PostTheme,
                 resource: Resource):
        self.channel_id = channel_id
        self.builder = SettingsKbBuilder(channel_id=self.channel_id)
        self.payment_plan = payment_plan
        self.is_active = is_active
        self.theme = theme
        self.resource = resource

    def get_kb(self):
        if self.payment_plan == PaymentOptions.STANDART:
            return InlineKeyboardMarkup(inline_keyboard=self.get_kb_for_standard())
        if self.payment_plan == PaymentOptions.PRO:
            return InlineKeyboardMarkup(inline_keyboard=self.get_kb_for_pro())
        if self.payment_plan == PaymentOptions.VIP:
            return InlineKeyboardMarkup(inline_keyboard=self.get_kb_for_vip())

    def get_kb_for_standard(self) -> list:
        self.builder.create_theme_button()
        self.builder.create_posts_time_button()
        if self.theme != PostTheme.UNDEFINED:
            if self.is_active:
                self.builder.create_deactivate_button()
            else:
                self.builder.create_activate_button()
        self.builder.create_back_button()
        return self.builder.kb

    def get_kb_for_pro(self) -> list:
        if self.resource == Resource.DATABASE:
            self.builder.create_theme_button()
        else:
            self.builder.create_load_file_button()
        self.builder.create_posts_time_button()
        self.builder.create_source_button()
        if self.is_active:
            self.builder.create_deactivate_button()
        else:
            self.builder.create_activate_button()
        self.builder.create_back_button()
        return self.builder.kb

    def get_kb_for_vip(self) -> list:
        if self.resource == Resource.DATABASE:
            self.builder.create_theme_button()
        elif self.resource == Resource.FILE:
            self.builder.create_load_file_button()
        else:
            self.builder.create_generate_ai_button()
        self.builder.create_posts_time_button()
        self.builder.create_source_button()
        if self.is_active:
            self.builder.create_deactivate_button()
        else:
            self.builder.create_activate_button()
        self.builder.create_back_button()
        return self.builder.kb
