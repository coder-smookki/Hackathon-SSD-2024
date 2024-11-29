from aiogram.filters.callback_data import CallbackData

class ViewVKS(CallbackData, prefix='view_vks'):

    operation_view_vks: str