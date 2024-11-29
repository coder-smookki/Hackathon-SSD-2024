from bot.handlers.get_vcc.formulations import SHOWING_VKS, AFTER_SHOWING_VKS, BEFORE_SHOWING_VKS, NOT_FOUND_VKS


def refactor_meetings(meetings: list) -> str:

    result_text = ''

    result = ["|".join([str(meeting["id"]), meeting["name"], \
                        meeting["startedAt"], meeting["startedAt"]]) + "\n" for meeting in meetings]

    result_text += BEFORE_SHOWING_VKS + '\n\n'

    result_text += '\n\n'.join([SHOWING_VKS.format(vks_id=meeting.split('|')[0],
                                    name=meeting.split('|')[1],
                                    startedAt=meeting.split('|')[2].split('T')[0].replace('-', '.'),
                                    timeStarted=meeting.split('|')[2].split('T')[1][:5] 
                                    if meeting.split('|')[2].split('T')[1][:5][0] != '0'
                                    else meeting.split('|')[2].split('T')[1][1:5]) for meeting in result]) if '\n\n'.join([SHOWING_VKS.format(vks_id=meeting.split('|')[0],
                                    name=meeting.split('|')[1],
                                    startedAt=meeting.split('|')[2].split('T')[0].replace('-', '.'),
                                    timeStarted=meeting.split('|')[2].split('T')[1][:5] 
                                    if meeting.split('|')[2].split('T')[1][:5][0] != '0'
                                    else meeting.split('|')[2].split('T')[1][1:5]) for meeting in result]) != '' else NOT_FOUND_VKS
    
    result_text += '\n\n' + AFTER_SHOWING_VKS

    return result_text


def refactor_meeting(meeting: dict) -> str:
    return "|".join([str(meeting["id"]), meeting["name"], \
                     meeting["startedAt"], meeting["startedAt"]]) + "\n"
