from business_logic.entities.channel_entity import ChannelSettings, PostTheme, Resource
from database.payments.options import PaymentOptions


def get_settings_menu_text(data: ChannelSettings):
    text = (f"Меню канала: {data.channel_name}\n"
            f"Доступных постов: {data.posts_available_count - data.posts_count}/{data.posts_available_count}")
    return text


class SettingsMenuBuilder:
    def __init__(self, theme: PostTheme, source: Resource):
        self.text = "Информация о настройках\n"
        self._theme = theme
        self._source = source

    def add_theme_str(self):
        self.text += f"Тема поста: {self._theme.value}\n"

    def add_posting_is_active_str(self):
        self.text += "Постинг активен\n"

    def add_posting_non_active_str(self):
        self.text += "Постинг не активен\n"

    def add_source_str(self):
        self.text += f"Источник: {self._source.value}\n"


class SettingsMenuText:
    def __init__(self, theme: PostTheme, is_active: bool, payment_plan: PaymentOptions, source: Resource):
        self.theme = theme
        self.is_active = is_active
        self.payment_plan = payment_plan
        self.builder = SettingsMenuBuilder(theme=self.theme, source=source)

    def get_text_for_standard(self):
        self.builder.add_theme_str()
        if self.is_active:
            self.builder.add_posting_is_active_str()
        else:
            self.builder.add_posting_non_active_str()
        self.builder.add_source_str()
        return self.builder.text

    def get_text_for_pro(self):
        self.builder.add_source_str()
        if self.is_active:
            self.builder.add_posting_is_active_str()
        else:
            self.builder.add_posting_non_active_str()
        return self.builder.text

    def get_text(self):
        if self.payment_plan == PaymentOptions.STANDART:
            return self.get_text_for_standard()
        elif self.payment_plan == PaymentOptions.PRO:
            return self.get_text_for_pro()
