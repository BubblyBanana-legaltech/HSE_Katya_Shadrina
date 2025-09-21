from legal_api import LegalAPI

api = LegalAPI()

try:
    result = api.search_debtors("Иванов", limit=1)
    print("✅ Ответ от API:")
    print(result)
except Exception as e:
    print("❌ Ошибка:")
    print(e)