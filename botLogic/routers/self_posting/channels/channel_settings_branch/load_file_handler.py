from pathlib import Path
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext

from botLogic.common_bot_tools.callback_data import ChannelSettingsCb, LoadCb
from .keyboards.load_file_kb import LoadFileKb, get_request_to_del_kb
from business_logic.services.channels_service.extension_service import ExtensionService
from business_logic.common_options.status_option import Status
from .keyboards.theme_kb import get_back_button_to_settings
from .states.load_file_state import LoadFileState
from botLogic.common_bot_tools.tools.state_cleaner import clean_state
from botLogic.common_bot_tools.tools.file_work import FileWork

router = Router(name=__name__)


@router.callback_query(ChannelSettingsCb.filter(F.action == "loadFileMenu"))
async def request_to_load_file_menu(call: CallbackQuery, callback_data: ChannelSettingsCb):
    channel_id = callback_data.channel_id
    ext_service = ExtensionService()
    posts_count = await ext_service.get_file_posts_count(channel_id=channel_id)
    status = await ext_service.request_to_load_file(channel_id=channel_id)
    buttons = LoadFileKb(channel_id=channel_id, status=status, file_posts_count=posts_count).get_kb()
    await call.message.edit_text("Выбери один из пунктов меню", reply_markup=buttons)


@router.callback_query(LoadCb.filter((F.action == "requestToDel")))
async def request_to_delete(call: CallbackQuery, callback_data: LoadCb):
    buttons = get_request_to_del_kb(channel_id=callback_data.channel_id)
    await call.message.edit_text("Ты действительно хочешь удалить все загруженные данные ?", reply_markup=buttons)


@router.callback_query(LoadCb.filter(F.action == "delete"))
async def request_to_delete(call: CallbackQuery, callback_data: LoadCb):
    channel_id = callback_data.channel_id
    ext_service = ExtensionService()
    status = await ext_service.delete_file_records(channel_id=channel_id)
    buttons = get_back_button_to_settings(channel_id=channel_id)
    if status == Status.OK:
        await call.message.edit_text("Удалено успешно", reply_markup=buttons)
    else:
        await call.message.edit_text("Что-то пошло не так", reply_markup=buttons)


@router.callback_query(LoadCb.filter(F.action == "load"))
async def request_to_load_file(call: CallbackQuery, callback_data: LoadCb, state: FSMContext):
    channel_id = callback_data.channel_id
    buttons = get_back_button_to_settings(channel_id=channel_id)
    await call.message.edit_text("Отправь мне файл по примеру ниже или вернись в меню")
    await call.message.answer_document(document=FSInputFile(Path("src") / "example.xlsx"))
    await call.message.answer("Вернуться в меню", reply_markup=buttons)
    await state.update_data(channel_id=channel_id)
    await state.set_state(LoadFileState.wait_file_loading)


@router.message(LoadFileState.wait_file_loading)
async def load_file_handler(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    channel_id = int(state_data.get("channel_id"))
    buttons = get_back_button_to_settings(channel_id)
    if msg.document is not None:
        try:
            file_work = FileWork(msg)
            records = await file_work.handle_exel(channel_id=channel_id)
            if records:
                ext = ExtensionService()
                await ext.add_file_records(channel_id=channel_id, records=records)
                await clean_state(state)
                await msg.answer(f"Файл успешно загружен, найдено {len(records)} записей", reply_markup=buttons)
            else:
                await msg.answer("Записей не найдено", reply_markup=buttons)
        except:
            await msg.answer("Что-то пошло не так, проверь правильность файла", reply_markup=buttons)
    else:
        await msg.answer("Отправь пожалуйста файл", reply_markup=buttons)
