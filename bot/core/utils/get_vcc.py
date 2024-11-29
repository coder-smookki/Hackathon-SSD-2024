from bot.handlers.get_vcc.formulations import SHOWING_VKS

def refactor_meetings(meetings: list) -> str:
    if not meetings:
        return "Не найдено ни одного мероприятия"
    result_text = '\n\n'.join([SHOWING_VKS.format(
        vks_id=str(meeting["id"]),
        name=meeting["name"],
        startedAt=meeting["startedAt"]
    ) for meeting in meetings])

    return result_text
