import requests
import time
import pprint
from collections import Counter
import re
from json import dump as jdump
import matplotlib.pyplot as plt

DOMAIN = 'https://api.hh.ru/'
url = f'{DOMAIN}vacancies'

vacancies = 'Python developer'

where = input('Где искать вакансию?')
query_string = input('Строка запроса?')

params = {
    'text': query_string,
    'area': 1,
    'page': 0,
    'per_page': 10
}

response = requests.get(url, params=params).json()

count_pages = response['pages']
all_count = len(response['items'])
skillis = []

for page in range(count_pages):
    if page > 2:
        break
    else:
        print(f"Обрабатывается страница {page}")

    params = {
        'text': query_string,
        'area': '1',
        'page': page,
        'per_page': 100
    }

    result = requests.get(url=url, params=params).json()

    for res in result['items']:
        skills = set()
        res_full = requests.get(res['url']).json()

        if 'description' in res_full:
            pp = res_full['description']
            pp_re = re.findall(r'\s[A-Za-z-?]+', pp)
            its = set(x.strip(' -').lower() for x in pp_re)

            for sk in res_full['key_skills']:
                skillis.append(sk['name'].lower())
                skills.add(sk['name'].lower())

            for it in its:
                if not any(it in x for x in skills):
                    skillis.append(it)

    # if count_pages < page + 1:
    #     break

    time.sleep(1)  # Добавляем задержку в 1 секунду перед следующим запросом

# Формирование списка навыков
print(skillis)
sk2 = Counter(skillis)
add = []
for name, count in sk2.most_common(5):
    add.append({'name': name, 'count': count, 'percent': round((count / all_count) * 100, 2)})

result['requirements'] = add
pprint.pprint(result)

# Создание графика
labels = [item['name'] for item in add]
percentages = [item['percent'] for item in add]

plt.figure(figsize=(8, 6))
plt.pie(percentages, labels=labels, autopct='%1.1f%%')
plt.title("Топ-5 навыков")

# Сохранение графика в виде изображения
plt.savefig('result.png')

# Опционально: отображение графика
plt.show()