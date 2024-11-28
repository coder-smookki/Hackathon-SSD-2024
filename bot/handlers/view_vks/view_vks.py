from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from aiogram.types import Message
from typing import Dict, Any
from bot.callbacks.view_vks import ViewVKS
from bot.filters.role import EmailExistsFilter


view_vks_router = Router(name=__name__)


@view_vks_router.callback_query(ViewVKS.filter(F.operation_view_vks == "view_vks"))
async def cmd_view_vks(callback: CallbackQuery):
    await callback.message.edit_text("Показ ВКС")
