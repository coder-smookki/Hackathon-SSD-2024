def refactor_meeting(meeting: dict) -> str:
    return "|".join([str(meeting["id"]), meeting["name"], \
                     meeting["startedAt"], meeting["startedAt"]]) + "\n"


