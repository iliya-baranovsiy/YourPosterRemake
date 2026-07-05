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
from .function_tools.decorators import required_plan
from botLogic.common_bot_tools.tools.decorators import save_work

router = Router(name=__name__)


@router.callback_query(ChannelSettingsCb.filter(F.action == "loadFileMenu"))
@required_plan()
@save_work()
async def request_to_load_file_menu(call: CallbackQuery, callback_data: ChannelSettingsCb):
    channel_id = callback_data.channel_id
    ext_service = ExtensionService()
    posts_count = await ext_service.get_file_posts_count(channel_id=channel_id)
    status = await ext_service.request_to_load_file(channel_id=channel_id)
    buttons = LoadFileKb(channel_id=channel_id, status=status, file_posts_count=posts_count).get_kb()
    await call.message.edit_text("📄 Файл с публикациями\n\nВыберите действие.", reply_markup=buttons)


@router.callback_query(LoadCb.filter((F.action == "requestToDel")))
@required_plan()
@save_work()
async def request_to_delete(call: CallbackQuery, callback_data: LoadCb):
    buttons = get_request_to_del_kb(channel_id=callback_data.channel_id)
    await call.message.edit_text("🗑️ Удалить все загруженные публикации?\n\nЭто действие нельзя отменить.",
                                 reply_markup=buttons)


@router.callback_query(LoadCb.filter(F.action == "delete"))
@required_plan()
@save_work()
async def request_to_delete(call: CallbackQuery, callback_data: LoadCb):
    channel_id = callback_data.channel_id
    ext_service = ExtensionService()
    status = await ext_service.delete_file_records(channel_id=channel_id)
    buttons = get_back_button_to_settings(channel_id=channel_id)
    if status == Status.OK:
        await call.message.edit_text("✅ Все загруженные публикации удалены.", reply_markup=buttons)
    else:
        await call.message.edit_text("⚠️ Не удалось выполнить операцию.\n\nПопробуйте еще раз.", reply_markup=buttons)


@router.callback_query(LoadCb.filter(F.action == "load"))
@required_plan()
@save_work()
async def request_to_load_file(call: CallbackQuery, callback_data: LoadCb, state: FSMContext):
    channel_id = callback_data.channel_id
    buttons = get_back_button_to_settings(channel_id=channel_id)
    await call.message.edit_text(
        "📄 Загрузите файл с публикациями в формате Excel.\n\nИспользуйте шаблон ниже. После заполнения отправьте файл в этот чат.")
    await call.message.answer_document(document=FSInputFile(Path("botLogic") / "src" / "example.xlsx"))
    await call.message.answer("◀️ Вернуться в меню", reply_markup=buttons)
    await state.update_data(channel_id=channel_id)
    await state.set_state(LoadFileState.wait_file_loading)


@router.message(LoadFileState.wait_file_loading)
@required_plan()
@save_work()
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
                await msg.answer(f"✅ Файл успешно загружен.\n\nНайдено публикаций: <b>{len(records)}</b>",
                                 reply_markup=buttons)
            else:
                await msg.answer("⚠️ В файле не найдено ни одной публикации.", reply_markup=buttons)
        except:
            await msg.answer("⚠️ Не удалось обработать файл.\n\nУбедитесь, что он соответствует шаблону, и попробуйте снова.", reply_markup=buttons)
    else:
        await msg.answer("📄 Отправьте файл с публикациями.", reply_markup=buttons)
