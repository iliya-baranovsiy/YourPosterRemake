from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from business_logic.services.channels_service.channel_settings_service import ChannelSettingsService
from business_logic.services.user_service import UserService
from business_logic.entities.channel_entity import PostTheme
from .keyboards.settings_kb import SettingsKb
from .function_tools.text import SettingsMenuText
from .keyboards.theme_kb import get_theme_kb, get_back_button_to_settings
from .keyboards.time_kb import TimeKb, back_to_time_menu, request_to_delete_time
from .function_tools.time_validator import time_validator
from .states.time_input_state import WaitTime

router = Router(name=__name__)


# ------------------------------Menu----------------------------
async def get_settings_menu(call: CallbackQuery, channel_id: int):
    channel_service = ChannelSettingsService()
    user_service = UserService()
    payment_plan = await user_service.get_only_payment_plan(tg_id=call.message.chat.id)
    channel_data = await channel_service.get_channel_settings(channel_id=channel_id)
    kb = SettingsKb(channel_id=channel_id, payment_plan=payment_plan, is_active=channel_data.posting_is_active,
                    theme=channel_data.theme, resource=channel_data.resource)
    text_cls = SettingsMenuText(theme=channel_data.theme,
                                is_active=channel_data.posting_is_active,
                                payment_plan=payment_plan,
                                source=channel_data.resource)
    text = text_cls.get_text() or "test text"
    buttons = kb.get_kb()
    await call.message.edit_text(text=text, reply_markup=buttons)


@router.callback_query(F.data.startswith("settings"))
async def settings_menu_handler(call: CallbackQuery):
    channel_id = int(call.data.split("_")[1])
    await get_settings_menu(call=call, channel_id=channel_id)


# ----------------------------------Menu------------------------------------

# ----------------------------------Theme------------------------------------
@router.callback_query(F.data.startswith("theme"))
async def theme_menu(call: CallbackQuery):
    channel_id = int(call.data.split("_")[1])
    service = ChannelSettingsService()
    data = await service.get_channel_settings(channel_id=channel_id)
    buttons = get_theme_kb(channel_id=channel_id, theme=data.theme)
    await call.message.edit_text("Выбери желаемую тему поста из списка", reply_markup=buttons)


@router.callback_query(F.data.startswith("settheme"))
async def set_theme(call: CallbackQuery):
    channel_service = ChannelSettingsService()
    data = call.data.split("_")
    channel_id = int(data[2])
    theme = PostTheme.enum_value(kb_value=data[1])
    channel = await channel_service.get_channel_settings(channel_id=channel_id)
    channel.theme = theme
    await channel_service.update_channel_settings(channel=channel)
    buttons = get_back_button_to_settings(channel_id=channel_id)
    await call.message.edit_text("Тема успешно установлена !", reply_markup=buttons)


# ----------------------------------Theme------------------------------------

# ----------------------------------Posting start/stop------------------------------------

@router.callback_query(F.data.startswith("start"))
async def activate_self_posting(call: CallbackQuery):
    channels_set_srvice = ChannelSettingsService()
    channel_id = int(call.data.split("_")[2])
    channel = await channels_set_srvice.get_channel_settings(channel_id=channel_id)
    channel.posting_is_active = True
    await channels_set_srvice.update_channel_settings(channel)
    await get_settings_menu(call=call, channel_id=channel_id)
    await call.answer(text="Постинг активирован", show_alert=True)


@router.callback_query(F.data.startswith("deactivate"))
async def deactivate_self_posting(call: CallbackQuery):
    channels_set_srvice = ChannelSettingsService()
    channel_id = int(call.data.split("_")[2])
    channel = await channels_set_srvice.get_channel_settings(channel_id=channel_id)
    channel.posting_is_active = False
    await channels_set_srvice.update_channel_settings(channel)
    await get_settings_menu(call=call, channel_id=channel_id)
    await call.answer(text="Постинг выключен", show_alert=True)


# ----------------------------------Posting start/stop------------------------------------

# ----------------------------------Time work------------------------------------

@router.callback_query(F.data.startswith("timelist"))
async def get_channel_times_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    channel_id = int(call.data.split("_")[1])
    user_service = UserService()
    channel_settings_s = ChannelSettingsService()
    payment_plan = await user_service.get_only_payment_plan(tg_id=call.message.chat.id)
    channel = await channel_settings_s.get_channel_settings(channel_id=channel_id)
    kb = TimeKb(channel_id=channel_id, times=channel.time, payment_plan=payment_plan)
    buttons = kb.get_time_kb()
    await call.message.edit_text("Меню времени", reply_markup=buttons)


@router.callback_query(F.data.startswith("inserttime"))
async def request_to_time(call: CallbackQuery, state: FSMContext):
    channel_id = int(call.data.split("_")[1])
    buttons = back_to_time_menu(channel_id=channel_id)
    await call.message.edit_text("Введи время в формате чч:мм", reply_markup=buttons)
    await state.update_data(channel_id=channel_id)
    await state.set_state(WaitTime.wait_time_input)


@router.message(WaitTime.wait_time_input)
async def set_time(msg: Message, state: FSMContext):
    time_ = msg.text
    state_data = await state.get_data()
    channel_id = int(state_data.get("channel_id"))
    buttons = back_to_time_menu(channel_id=channel_id)
    if time_validator(time_):
        ch_service = ChannelSettingsService()
        channel = await ch_service.get_channel_settings(channel_id=channel_id)
        channel.time.append(time_)
        await ch_service.update_channel_time(channel)
        await state.clear()
        await msg.answer("Время успешно сохранено", reply_markup=buttons)
    else:
        await msg.answer("Формат даты неверный, повтори поптыку ввода, или выйди в меню", reply_markup=buttons)


@router.callback_query(F.data.startswith("chtime"))
async def request_to_drop_time(call: CallbackQuery):
    call_data = call.data.split("_")
    channel_id = int(call_data[1])
    time_ = call_data[2]
    buttons = request_to_delete_time(channel_id=channel_id, time_=time_)
    await call.message.edit_text(f"Ты действительно хочешь удалить время {time_} из списка ?", reply_markup=buttons)


@router.callback_query(F.data.startswith("dchanneltime"))
async def drop_time_handler(call: CallbackQuery):
    call_data = call.data.split("_")
    channel_service = ChannelSettingsService()
    channel_id = int(call_data[1])
    time_ = call_data[2]
    channel = await channel_service.get_channel_settings(channel_id=channel_id)
    channel.time.remove(time_)
    await channel_service.update_channel_time(channel)
    buttons = back_to_time_menu(channel_id=channel_id)
    await call.message.edit_text("Время успешно удалено", reply_markup=buttons)
