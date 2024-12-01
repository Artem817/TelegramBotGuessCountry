import requests
import json
import time

API_URL_TEMPLATE = 'https://restcountries.com/v3.1/region/{region}'
REGIONS = ['africa', 'americas', 'asia', 'europe', 'oceania']

def generate_countries_json():
    max_retries = 5
    countries = []
    for region in REGIONS:
        for attempt in range(max_retries):
            try:
                response = requests.get(API_URL_TEMPLATE.format(region=region), timeout=10)
                response.raise_for_status()
                data = response.json()
                for country in data:
                    name = country.get('name', {}).get('common')
                    capitals = country.get('capital', [])
                    if name and capitals:
                        countries.append({
                            'country': name,
                            'capital': capitals[0]
                        })
                print(f"Дані для регіону {region} успішно завантажено!")
                break
            except requests.exceptions.RequestException as e:
                print(f"Спроба {attempt + 1} із {max_retries} для регіону {region} не вдалася: {e}")
                time.sleep(2)  
        else:
            print(f"Помилка при завантаженні даних для регіону {region} після кількох спроб.")
    
    if countries:
        with open('countries.json', 'w', encoding='utf-8') as f:
            json.dump(countries, f, ensure_ascii=False, indent=4)
        print("Файл countries.json успішно створено!")
    else:
        print("Не вдалося створити файл countries.json, оскільки дані не були завантажені.")

if __name__ == '__main__':
    generate_countries_json()
