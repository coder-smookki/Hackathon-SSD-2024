from bot.handlers.get_vcc.filters.cancel import filter_cancel_router
from bot.handlers.get_vcc.filters.department import filter_department_router
from bot.handlers.get_vcc.filters.name import filter_name_router
from bot.handlers.get_vcc.filters.priority import filter_priority_router
from bot.handlers.get_vcc.filters.state import filter_state_router
from bot.handlers.get_vcc.filters.user import filter_user_router


routers = (
    filter_cancel_router,
    filter_department_router,
    filter_name_router,
    filter_priority_router,
    filter_state_router,
    filter_user_router,
)