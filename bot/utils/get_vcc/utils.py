from bot.handlers.get_vcc.formulations import SHOWING_VKS

def refactor_meetings(meetings: list) -> str:

    result_text = ''

    result = ["|".join([str(meeting["id"]), meeting["name"], \
                        meeting["startedAt"], meeting["startedAt"]]) + "\n" for meeting in meetings]

    # for meeting in meetings:

    #     result = "|".join([str(meeting["id"]), meeting["name"], \
    #                     meeting["startedAt"], meeting["startedAt"]]) + "\n"
    
    result_text = '\n\n'.join([SHOWING_VKS.format(vks_id=meeting.split('|')[0],
                                    name=meeting.split('|')[1],
                                    startedAt=meeting.split('|')[2]) for meeting in result])
    return result_text


def refactor_meeting(meeting: dict) -> str:
    return "|".join([str(meeting["id"]), meeting["name"], \
                     meeting["startedAt"], meeting["startedAt"]]) + "\n"
