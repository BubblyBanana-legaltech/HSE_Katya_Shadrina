class CourtCase:
    def __init__(self, case_number):
        self.case_number = case_number  # обязательный параметр - номер дела
        self.case_participants = []     # список участников дела, пустой по умолчанию
        self.listening_datetimes = []   # список судебных заседаний, пустой по умолчанию
        self.is_finished = False        # по умолчанию дело не завершено
        self.verdict = ""               # решение по делу, пустая строка по умолчанию

    def set_a_listening_datetime(self, datetime_info):
        # Добавляет судебное заседание (можно передать любую структуру, например словарь)
        self.listening_datetimes.append(datetime_info)

    def add_participant(self, participant_id):
        # Добавляет участника, если его ещё нет
        if participant_id not in self.case_participants:
            self.case_participants.append(participant_id)

    def remove_participant(self, participant_id):
        # Убирает участника, если он есть
        if participant_id in self.case_participants:
            self.case_participants.remove(participant_id)

    def make_a_decision(self, verdict_text):
        # Вынести решение, изменить статус дела на завершённое
        self.verdict = verdict_text
        self.is_finished = True


# Пример использования:
case = CourtCase("А12345")
case.add_participant("1234567890")
case.set_a_listening_datetime({"date": "2025-09-15", "time": "10:00", "location": "Зал 1"})
case.remove_participant("1234567890")
case.make_a_decision("Дело закрыто по статьям 10 и 15.")

print(case.case_number)            # А12345
print(case.case_participants)      # []
print(case.listening_datetimes)    # [{'date': '2025-09-15', 'time': '10:00', 'location': 'Зал 1'}]
print(case.is_finished)             # True
print(case.verdict)                # Дело закрыто по статьям 10 и 15.