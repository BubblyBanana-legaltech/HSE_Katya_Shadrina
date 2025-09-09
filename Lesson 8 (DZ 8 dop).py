class RightObligation:
    def __init__(self, right_holder, obligation_holder, description, deadline):
        """
        right_holder - сторона, обладающая правом (например, истец)
        obligation_holder - сторона, несущая обязательство (например, ответчик)
        description - описание права и обязательства
        deadline - срок исполнения обязательства (строка или объект даты)
        """
        self.right_holder = right_holder
        self.obligation_holder = obligation_holder
        self.description = description
        self.deadline = deadline
        self.is_fulfilled = False  # выполнено ли обязательство

    def fulfill_obligation(self):
        """Отметить обязательство как выполненное."""
        self.is_fulfilled = True
        print(f"Обязательство выполнено: {self.description}")

    def extend_deadline(self, new_deadline):
        """Продлить срок исполнения обязательства."""
        self.deadline = new_deadline
        print(f"Срок исполнения продлен до: {self.deadline}")

    def info(self):
        """Вывести информацию о праве и обязательстве."""
        status = "выполнено" if self.is_fulfilled else "не выполнено"
        print(f"Право: {self.right_holder}")
        print(f"Обязательство: {self.obligation_holder}")
        print(f"Описание: {self.description}")
        print(f"Срок исполнения: {self.deadline}")
        print(f"Статус: {status}")


# Пример использования:
if __name__ == "__main__":
    case = RightObligation(
        right_holder="Истец Иванов И.И.",
        obligation_holder="Ответчик Петров П.П.",
        description="Оплата задолженности по договору",
        deadline="2025-10-01"
    )
    case.info()
    case.fulfill_obligation()
    case.extend_deadline("2025-12-01")
    case.info()