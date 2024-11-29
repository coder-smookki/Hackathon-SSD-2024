from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.callbacks.profile import ProfileOpen
from bot.filters.role import EmailExistsFilter
from bot.handlers.profile.formulations import PROFILE_TEXT
from bot.keyboards.profile import profile_keyboard
from database.models import UserModel

profile_router = Router(name=__name__)


@profile_router.callback_query(
    ProfileOpen.filter(F.operation_prof == "profile"), EmailExistsFilter()
)
async def cmd_profile(callback: CallbackQuery, user: UserModel):

    await callback.message.edit_text(
        text=PROFILE_TEXT.format(
            first_name=user.first_name,
            last_name=user.last_name,
            midle_name=user.midle_name,
            login=user.login,
            email=user.email,
        ),
        reply_markup=profile_keyboard,
    )
