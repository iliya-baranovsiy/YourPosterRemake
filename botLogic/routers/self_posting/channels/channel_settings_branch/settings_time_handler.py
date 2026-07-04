from datetime import datetime
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from business_logic.services.channels_service.channel_settings_service import ChannelSettingsService
from business_logic.services.user_service import UserService
from .keyboards.time_kb import TimeKb, back_to_time_menu, request_to_delete_time
from .function_tools.time_validator import time_validator
from .states.time_input_state import WaitTime
from botLogic.common_bot_tools.callback_data import ChannelSettingsCb, TimeCb
from botLogic.common_bot_tools.tools.decorators import save_work

router = Router(name=__name__)


@router.callback_query(ChannelSettingsCb.filter(F.action == "openTimeList"))
@save_work()
async def get_channel_times_menu(call: CallbackQuery, state: FSMContext, callback_data: ChannelSettingsCb):
    await state.clear()
    channel_id = callback_data.channel_id
    user_service = UserService()
    channel_settings_s = ChannelSettingsService()
    payment_plan = await user_service.get_only_payment_plan(tg_id=call.message.chat.id)
    channel = await channel_settings_s.get_channel_settings(channel_id=channel_id, tg_id=call.message.chat.id)
    kb = TimeKb(channel_id=channel_id, times=channel.time, payment_plan=payment_plan)
    buttons = kb.get_time_kb()
    await call.message.edit_text("Меню времени", reply_markup=buttons)


@router.callback_query(TimeCb.filter(F.action == "addTime"))
@save_work()
async def request_to_time(call: CallbackQuery, state: FSMContext, callback_data: TimeCb):
    channel_id = callback_data.channel_id
    buttons = back_to_time_menu(channel_id=channel_id)
    await call.message.edit_text("Введи время в формате чч:мм", reply_markup=buttons)
    await state.update_data(channel_id=channel_id)
    await state.set_state(WaitTime.wait_time_input)


@router.message(WaitTime.wait_time_input)
@save_work()
async def set_time(msg: Message, state: FSMContext):
    time_ = msg.text
    state_data = await state.get_data()
    channel_id = int(state_data.get("channel_id"))
    buttons = back_to_time_menu(channel_id=channel_id)
    if time_validator(time_):
        ch_service = ChannelSettingsService()
        channel = await ch_service.get_channel_settings(channel_id=channel_id, tg_id=msg.chat.id)
        format_time = datetime.strptime(time_, '%H:%M').strftime('%H:%M')
        if format_time in channel.time:
            await msg.answer("Это время уже записано попробуй снова", reply_markup=buttons)
        else:
            channel.time.append(format_time)
            await ch_service.update_channel_time(channel)
            await state.clear()
            await msg.answer("Время успешно сохранено", reply_markup=buttons)
    else:
        await msg.answer("Формат даты неверный, повтори поптыку ввода, или выйди в меню", reply_markup=buttons)


@router.callback_query(TimeCb.filter(F.action == "openTime"))
@save_work()
async def request_to_drop_time(call: CallbackQuery, callback_data: TimeCb):
    channel_id = callback_data.channel_id
    time_ = callback_data.time_.replace("-", ":")
    buttons = request_to_delete_time(channel_id=channel_id, time_=time_)
    await call.message.edit_text(f"Ты действительно хочешь удалить время {time_} из списка ?", reply_markup=buttons)


@router.callback_query(TimeCb.filter(F.action == "dropTime"))
@save_work()
async def drop_time_handler(call: CallbackQuery, callback_data: TimeCb):
    channel_service = ChannelSettingsService()
    channel_id = callback_data.channel_id
    time_ = callback_data.time_.replace("-", ":")
    channel = await channel_service.get_channel_settings(channel_id=channel_id, tg_id=call.message.chat.id)
    channel.time.remove(time_)
    await channel_service.update_channel_time(channel)
    buttons = back_to_time_menu(channel_id=channel_id)
    await call.message.edit_text("Время успешно удалено", reply_markup=buttons)
