from business_logic.entities.channel_entity import ChannelSettings, PostTheme, Resource
from database.payments.options import PaymentOptions


def get_settings_menu_text(data: ChannelSettings):
    text = (f"📢 <b>{data.channel_name}</b>\n"
            f"📝 <b>Доступно публикаций:</b> {data.posts_available_count - data.posts_count} из {data.posts_available_count}")
    return text


class SettingsMenuBuilder:
    def __init__(self, theme: PostTheme, source: Resource, count: int):
        self.text = "⚙️ <b>Настройки постинга</b>\n"
        self._theme = theme
        self._source = source
        self._count = count

    def add_theme_str(self):
        self.text += f"📫 <b>Тема публикации:</b> {self._theme.value}\n"

    def add_posting_is_active_str(self):
        self.text += "📡 <b>Статус:</b> 🟢 Активен\n"

    def add_posting_non_active_str(self):
        self.text += "📡 <b>Статус:</b> 🔴 Неактивен\n"

    def add_source_str(self):
        self.text += f"📰 <b>Источник:</b> {self._source.value}\n"

    def add_file_posts_count_text(self):
        self.text += f"🗄 <b>Записей из файла:</b> {self._count}\n"


class SettingsMenuText:
    def __init__(self, theme: PostTheme, is_active: bool, payment_plan: PaymentOptions, source: Resource, count: int):
        self.theme = theme
        self.is_active = is_active
        self.payment_plan = payment_plan
        self.source = source
        self.builder = SettingsMenuBuilder(theme=self.theme, source=source, count=count)

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
        if self.source == Resource.FILE:
            self.builder.add_file_posts_count_text()
        else:
            self.builder.add_theme_str()
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
