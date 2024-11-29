CREATION_VKS = """
👥 Данные ВКС корректны?

📜 Название: {name}
🙎‍♂️ Количество участников: {participantsCount}
📆 Дата начала: {startedAt}
🕒 Продолжительность в минутах: {duration}
⚙️ Средство проведения: {backend}
🎤 Включен ли микрофон: {isMicrophoneOn}
📷 Включено ли видео: {isVideoOn}
🚪 Включено ли ожидание комнаты: {isWaitingRoomEnabled}
💿 Требуйте ли запись: {needVideoRecording}
""".strip()

END_CREATION_VKS = """
✅ Ваша ВКС создана:

📨 Ссылка для приглашения ВКС: {permalink}
📩 Участники: {participants}
""".strip()