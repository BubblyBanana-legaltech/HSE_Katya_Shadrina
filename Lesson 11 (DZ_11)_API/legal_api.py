import requests

class LegalAPI:
    BASE_URL = "https://legal-api.sirotinsky.com"
    TOKEN = "4123saedfasedfsadf4324234f223ddf23"

    def __init__(self):
        self.token = self.TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "User-Agent": "LegalAPI Client/1.0"
        }

    def _make_request(self, method: str, endpoint: str, params: dict = None, json_data: dict = None) -> dict:
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=json_data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка запроса к {url}: {e}")
        except ValueError:
            raise Exception(f"Некорректный JSON-ответ от {url}")

    def search_debtors(self, query: str, limit: int = 10, offset: int = 0) -> dict:
        params = {"query": query, "limit": limit, "offset": offset}
        return self._make_request("GET", "/api/v1/efrsb/debtors/search", params=params)

    def get_case_info(self, case_id: str) -> dict:
        return self._make_request("GET", f"/api/v1/efrsb/cases/{case_id}")

    def search_cases(self, debtor_name: str = None, region: str = None, status: str = None, limit: int = 10) -> dict:
        params = {k: v for k, v in {
            "debtor_name": debtor_name,
            "region": region,
            "status": status,
            "limit": limit
        }.items() if v is not None}
        return self._make_request("GET", "/api/v1/efrsb/cases/search", params=params)

    def search_messages(self, debtor_name: str = None, publish_date_from: str = None, publish_date_to: str = None) -> dict:
        params = {k: v for k, v in {
            "debtor_name": debtor_name,
            "publish_date_from": publish_date_from,
            "publish_date_to": publish_date_to
        }.items() if v is not None}
        return self._make_request("GET", "/api/v1/efrsb/messages/search", params=params)

    def get_message_by_id(self, message_id: str) -> dict:
        return self._make_request("GET", f"/api/v1/efrsb/messages/{message_id}")