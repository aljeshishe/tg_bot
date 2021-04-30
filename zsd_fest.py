import re

import requests


def check_place():
    with requests.session() as s:
        response1 = s.get('https://reg.place/events/zsd-fontanka-fest/registration')
        response1.raise_for_status()
        authenticity_token = re.search('name="authenticity_token" value="(.+?)"', response1.text).group(1)

        data = {
            "utf8": "✓",
            "authenticity_token": authenticity_token,
            "select_person_form[race_id]": "5834",
            "select_person_form[code]": "",
            "commit": "Заполнить+анкету"
        }
        response2 = s.post('https://reg.place/events/zsd-fontanka-fest/registration', data=data)
        response2.raise_for_status()

        fail_string = 'Ограничение дисциплины'
        if fail_string not in response1 and fail_string in response2:
            return 'Нет мест'
        if fail_string not in response1 and fail_string not in response2:
            return 'Есть места'
        raise Exception(f'Unexpected response:\n{response2.text}')


if __name__ == '__main__':
    print(check_place())
