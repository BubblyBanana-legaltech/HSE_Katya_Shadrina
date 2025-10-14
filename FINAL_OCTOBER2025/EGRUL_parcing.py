# parse_egrul.py
# Скрипт для парсинга данных из ЕГРЮЛ по списку ОГРН и сохранения в Excel

import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import os


def parse_org_xml(xml_content):
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        print(f"Ошибка парсинга XML: {e}")
        return None

    sv_yul = root.find(".//СвЮЛ")
    if sv_yul is None:
        return None

    attrs = sv_yul.attrib
    ogrn = attrs.get("ОГРН", "")
    inn = attrs.get("ИНН", "")
    kpp = attrs.get("КПП", "")

    # Наименования
    name_full = ""
    name_short = ""
    sv_naim_yul = sv_yul.find("СвНаимЮЛ")
    if sv_naim_yul is not None:
        name_full = sv_naim_yul.attrib.get("НаимЮЛПолн", "").strip()
        sv_sokr = sv_naim_yul.find("СвНаимЮЛСокр")
        if sv_sokr is not None:
            name_short = sv_sokr.attrib.get("НаимСокр", "").strip()

    # === ФИО и ДОЛЖНОСТЬ РУКОВОДИТЕЛЯ ===
    fio_ruk = ""
    dolzhnost = ""

    sved_dolzhn_fl = sv_yul.find(".//СведДолжнФЛ")
    if sved_dolzhn_fl is not None:
        sv_dolzhn = sved_dolzhn_fl.find("СвДолжн")
        if sv_dolzhn is not None:
            dolzhnost = sv_dolzhn.attrib.get("НаимДолжн", "").strip()
        sv_fl = sved_dolzhn_fl.find("СвФЛ")
        if sv_fl is not None:
            fam = sv_fl.attrib.get("Фамилия", "")
            im = sv_fl.attrib.get("Имя", "")
            otch = sv_fl.attrib.get("Отчество", "")
            fio_ruk = " ".join([part for part in [fam, im, otch] if part])

    if not fio_ruk:
        sv_ruk = sv_yul.find(".//СвРук")
        if sv_ruk is not None:
            dolzhnost = sv_ruk.attrib.get("НаимДолжн", "").strip()
            fio_el = sv_ruk.find("ФИО")
            if fio_el is not None:
                fam = fio_el.attrib.get("Фамилия", "")
                im = fio_el.attrib.get("Имя", "")
                otch = fio_el.attrib.get("Отчество", "")
                fio_ruk = " ".join([part for part in [fam, im, otch] if part])

    if not fio_ruk:
        sv_dolzhn = sv_yul.find(".//СвДолжн")
        if sv_dolzhn is not None:
            dolzhnost = sv_dolzhn.attrib.get("НаимДолжн", "").strip()
            sv_fl = sv_yul.find(".//СвФЛ")
            if sv_fl is not None:
                fam = sv_fl.attrib.get("Фамилия", "")
                im = sv_fl.attrib.get("Имя", "")
                otch = sv_fl.attrib.get("Отчество", "")
                fio_ruk = " ".join([part for part in [fam, im, otch] if part])

    # Email
    email = ""
    sv_email = sv_yul.find("СвАдрЭлПочты")
    if sv_email is not None and "E-mail" in sv_email.attrib:
        email = sv_email.attrib["E-mail"]

    # ОКВЭД
    okved_osn = ""
    okved_dop_list = []
    sv_okved = sv_yul.find("СвОКВЭД")
    if sv_okved is not None:
        sv_okved_osn = sv_okved.find("СвОКВЭДОсн")
        if sv_okved_osn is not None and "КодОКВЭД" in sv_okved_osn.attrib:
            okved_osn = sv_okved_osn.attrib["КодОКВЭД"]
        sv_okved_dop_list = sv_okved.findall("СвОКВЭДДоп")
        for el in sv_okved_dop_list:
            if "КодОКВЭД" in el.attrib:
                okved_dop_list.append(el.attrib["КодОКВЭД"])
    okved_dop = ", ".join(okved_dop_list)

    # === ФОРМИРОВАНИЕ ПОЛНОГО АДРЕСА ИЗ СвАдрЮЛФИАС ===
    address_parts = []
    sv_adr_fias = sv_yul.find("СвАдресЮЛ/СвАдрЮЛФИАС")

    if sv_adr_fias is not None:
        # Индекс
        index = sv_adr_fias.attrib.get("Индекс", "").strip()
        if index:
            address_parts.append(index)

        # НаимРегион (текст внутри тега)
        naime_region_el = sv_adr_fias.find("НаимРегион")
        if naime_region_el is not None and naime_region_el.text:
            address_parts.append(naime_region_el.text.strip())

        # Муниципальный район
        mun_rayon_el = sv_adr_fias.find("МуниципРайон")
        if mun_rayon_el is not None and "Наим" in mun_rayon_el.attrib:
            address_parts.append(mun_rayon_el.attrib["Наим"].strip())

        # Населённый пункт
        nasel_punkt = sv_adr_fias.find("НаселенПункт")
        if nasel_punkt is not None and "Наим" in nasel_punkt.attrib:
            tip_np = nasel_punkt.attrib.get("Вид", "").strip()
            naime_np = nasel_punkt.attrib["Наим"].strip()
            if tip_np:
                address_parts.append(f"{tip_np} {naime_np}")
            else:
                address_parts.append(naime_np)

        # Улица / проезд
        ul_dor_el = sv_adr_fias.find("ЭлУлДорСети")
        if ul_dor_el is not None:
            tip = ul_dor_el.attrib.get("Тип", "").strip()
            naime = ul_dor_el.attrib.get("Наим", "").strip()
            if tip and naime:
                address_parts.append(f"{tip} {naime}")
            elif naime:
                address_parts.append(naime)

        # Здание
        zdanie = sv_adr_fias.find("Здание")
        if zdanie is not None and "Номер" in zdanie.attrib:
            tip = zdanie.attrib.get("Тип", "").strip()
            nomer = zdanie.attrib["Номер"].strip()
            if tip:
                address_parts.append(f"{tip} {nomer}")
            else:
                address_parts.append(nomer)

        # Помещение в здании
        pom_zd = sv_adr_fias.find("ПомещЗдания")
        if pom_zd is not None and "Номер" in pom_zd.attrib:
            tip = pom_zd.attrib.get("Тип", "").strip()
            nomer = pom_zd.attrib["Номер"].strip()
            if tip:
                address_parts.append(f"{tip} {nomer}")
            else:
                address_parts.append(nomer)

        # Рабочее место / квартира
        pom_kv = sv_adr_fias.find("ПомещКвартиры")
        if pom_kv is not None and "Номер" in pom_kv.attrib:
            tip = pom_kv.attrib.get("Тип", "").strip()
            nomer = pom_kv.attrib["Номер"].strip()
            if tip:
                address_parts.append(f"{tip} {nomer}")
            else:
                address_parts.append(nomer)

    else:
        # Резерв: старый способ через АдресРФ
        adres_rf = sv_yul.find("СвАдресЮЛ/АдресРФ")
        if adres_rf is not None:
            if "Индекс" in adres_rf.attrib:
                address_parts.append(adres_rf.attrib["Индекс"])
            reg = adres_rf.find("Регион")
            if reg is not None and "НаимРегион" in reg.attrib:
                address_parts.append(reg.attrib["НаимРегион"])
            street_el = adres_rf.find("Улица")
            if street_el is not None and "НаимУлица" in street_el.attrib:
                address_parts.append(street_el.attrib["НаимУлица"])
            if "Дом" in adres_rf.attrib:
                address_parts.append(adres_rf.attrib["Дом"])
            if "Корпус" in adres_rf.attrib:
                address_parts.append(adres_rf.attrib["Корпус"])
            if "Кварт" in adres_rf.attrib:
                address_parts.append(adres_rf.attrib["Кварт"])

    full_address = ", ".join([part for part in address_parts if part])

    return {
        "ОГРН": ogrn,
        "ИНН": inn,
        "КПП": kpp,
        "НаимСокр": name_short,
        "НаимПолн": name_full,
        "Адрес": full_address,
        "ФИО_Руководителя": fio_ruk,
        "Должность": dolzhnost,
        "Email": email,
        "ОКВЭД_Основной": okved_osn,
        "ОКВЭД_Доп": okved_dop,
        "ДатаВып": attrs.get("ДатаВып", ""),
        "ДатаЗагрузки": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def get_org_data(ogrn):
    url = f"https://egrul.itsoft.ru/{ogrn}.xml"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and response.content.strip():
            return parse_org_xml(response.content)
        else:
            print(f"Данные не найдены для ОГРН {ogrn} (статус: {response.status_code})")
            return None
    except Exception as e:
        print(f"Ошибка при загрузке ОГРН {ogrn}: {e}")
        return None


def save_to_excel(data_list, filename='egrul_multiple.xlsx'):
    if not data_list:
        print("Нет данных для сохранения")
        return

    df_new = pd.DataFrame(data_list)

    try:
        if os.path.exists(filename):
            existing_df = pd.read_excel(filename)
            combined_df = pd.concat([existing_df, df_new], ignore_index=True)
        else:
            combined_df = df_new

        combined_df.to_excel(filename, index=False)
        print(f"✅ Данные успешно сохранены в {filename}")
    except PermissionError:
        print(f"❌ Ошибка: файл '{filename}' открыт в Excel. Закройте его и повторите запуск.")
    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")


if __name__ == "__main__":
    # Укажите нужные ОГРН
    ogrn_list = ["1232300034670", "1227700086460", "1257700213847", "1197746757515","1217700337975","1197746136939","1232300034670", "1231600034676"]

    all_data = []
    for ogrn in ogrn_list:
        print(f"Загрузка данных для ОГРН: {ogrn}")
        data = get_org_data(ogrn)
        if data is not None:
            all_data.append(data)

    if all_data:
        save_to_excel(all_data)
    else:
        print("❌ Нет данных для обработки.")