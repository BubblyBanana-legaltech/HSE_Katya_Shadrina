import os
import json
import requests
from bs4 import BeautifulSoup


class ParserCBRF:
    _URL = "https://www.cbr.ru/hd_base/KeyRate/"
    _OUTPUT_FILE = "key_rate.json"

    def __init__(self):
        self._data = {}

    def start(self) -> None:
        print("Запуск парсера через HTML (BeautifulSoup)")
        try:
            soup = self._get_cbr_soup()
            self._parse_cbr_table(soup)
            print(f"Найдено записей: {len(self._data)}")
            self._save_to_json()
            print(f"Файл сохранён: {os.path.join(os.path.dirname(__file__), self._OUTPUT_FILE)}")
        except Exception as e:
            print(f"Ошибка: {e}")
            raise

    def _get_cbr_soup(self) -> BeautifulSoup:
        print(f"Загрузка страницы: {self._URL}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(self._URL, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def _parse_cbr_table(self, soup: BeautifulSoup) -> None:
        # Ищем первую таблицу на странице
        table = soup.find('table')
        if not table:
            raise ValueError("Таблица не найдена на странице")

        rows = table.find_all('tr')
        if len(rows) < 2:
            raise ValueError("В таблице нет строк с данными")

        parsed = {}
        for row in rows[1:]:  # Пропускаем заголовок
            cells = row.find_all('td')
            if len(cells) >= 2:
                date_cell = cells[0].get_text(strip=True)
                rate_cell = cells[1].get_text(strip=True)
                try:
                    # Дата может быть в формате "13.09.2013" или "2025-04-26"
                    if '.' in date_cell:
                        # День.Месяц.Год → преобразуем в Год-Месяц-День
                        day, month, year = date_cell.split('.')
                        date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    else:
                        date_str = date_cell  # уже в нужном формате

                    rate_float = float(rate_cell.replace('%', '').replace(',', '.').strip())
                    parsed[date_str] = rate_float
                except Exception:
                    continue  # пропускаем некорректные строки

        self._data = parsed

    def _save_to_json(self) -> None:
        output_path = os.path.join(os.path.dirname(__file__), self._OUTPUT_FILE)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=4)

    def to_json(self) -> str:
        return json.dumps(self._data, ensure_ascii=False, indent=4)

    @classmethod
    def from_json(cls, path: str):
        inst = cls()
        with open(path, encoding="utf-8") as f:
            inst._data = json.load(f)
        return inst


if __name__ == "__main__":
    parser = ParserCBRF()
    parser.start()