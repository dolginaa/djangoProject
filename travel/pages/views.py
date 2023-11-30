from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import random
from datetime import date, timedelta
import re
import wikipediaapi


def index(request):
    if request.method == 'POST':
        city_name = request.POST.get('city', '')
        return weather(request, city_name)
    return render(request, "index.html")


def about(request, name="Пушкино"):
    str = "day+19"
    pos = str.find("+")
    new_str = str[pos:]
    return HttpResponse(f"О городе {new_str}")


def weather(request, name="Пушкино"):

    city = name

    url = f'https://time-in.ru/coordinates?search={city}'
    resp2 = requests.get(url)
    string = BeautifulSoup(resp2.text, "lxml")
    bs = string.find('table', class_="coordinates-table")
    if (not bs):
        return hangman_game(request)
    alltext = bs.text
    pos = alltext.find("В десятичном формате")+20
    shirota = alltext[pos:pos+7]
    dolgota = alltext[pos+9:pos+16]

    api_key = '54dba589-3248-4938-8b01-9027b13ceb1f'
    today_date = date.today()
    url_forecast = f'https://api.weather.yandex.ru/v2/informers?lat={shirota}&lon={dolgota}&limit=3'
    headers = {'X-Yandex-API-Key': api_key}

    response = requests.get(url_forecast, headers=headers)
    data = response.json()

    a = [None, None, None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None, None]
    i = 0
    for day_forecast in data["forecast"]:
        a[i] = day_forecast["date"]
        i += 1
        a[i] = day_forecast["parts"]["day"]["temp_avg"]
        i += 1
        a[i] = day_forecast["parts"]["night"]["temp_avg"]
        i += 1
        a[i] = day_forecast["parts"]["day"]["wind_speed"]
        i += 1
        a[i] = day_forecast["parts"]["day"]["humidity"]
        i += 1
        a[i] = day_forecast["parts"]["day"]["condition"]
        i += 1

    return render(request, "weather.html", context={"city": name, "forecast": a})


def hangman_game(request):
    words = ['python', 'django', 'javascript',
             'html', 'css', 'java', 'database']
    if 'secret_word' not in request.session:
        request.session['secret_word'] = random.choice(words).upper()
        request.session['guessed_letters'] = []
        request.session['remaining_attempts'] = 7

    secret_word = request.session['secret_word']
    # Преобразуем список обратно в множество
    guessed_letters = set(request.session['guessed_letters'])
    remaining_attempts = request.session['remaining_attempts']

    if request.method == 'POST':
        # Используем get() с пустым значением по умолчанию
        letter = request.POST.get('letter', '').upper()
        if letter and letter not in guessed_letters:  # Проверяем, что letter не пустой
            guessed_letters.add(letter)
            if letter not in secret_word:
                remaining_attempts -= 1

        # Преобразуем множество обратно в список
        request.session['guessed_letters'] = list(guessed_letters)
        request.session['remaining_attempts'] = remaining_attempts

    if all(letter in guessed_letters for letter in secret_word):
        message = "Поздравляю! Вы угадали слово!"
        request.session.pop('secret_word')
        request.session.pop('guessed_letters')
        request.session.pop('remaining_attempts')
    elif remaining_attempts == 0:
        message = f"Игра окончена. Загаданное слово было '{secret_word}'. Попробуйте еще раз!"
        request.session.pop('secret_word')
        request.session.pop('guessed_letters')
        request.session.pop('remaining_attempts')
    else:
        message = ""

    context = {
        'message': message,
        'secret_word': secret_word,
        'guessed_letters': guessed_letters,
        'remaining_attempts': remaining_attempts,
    }

    return render(request, 'exception.html', context)


def sights(request, name="Пушкино"):

    city = name

    url = f'https://ru.wikipedia.org/wiki/{city}'
    resp2 = requests.get(url)
    string = BeautifulSoup(resp2.text, "lxml")
    print(f'PRINTED {string.text} ')
    bs = string.find('div', class_="mw-parser-output")
    return HttpResponse(bs.text)
    return render(request, "about.html", context={"city": name, "forecast": bs.text})

    alltext = bs.text
    pos = alltext.find("В десятичном формате")+20
    shirota = alltext[pos:pos+7]
    dolgota = alltext[pos+9:pos+16]
    print(f'PRINTED {dolgota} ')

    api_key = '54dba589-3248-4938-8b01-9027b13ceb1f'
    today_date = date.today()
    url_today = f'https://api.weather.yandex.ru/v2/forecast?city={city}&date={today_date}'
    headers = {'X-Yandex-API-Key': api_key}

    def get_weather_info(url, a):
        response = requests.get(url, headers=headers)
        data = response.json()
        forecasts_today = data['forecasts'][0]
        # Извлекаем температуру утром и ночью
        a[0] = forecasts_today['parts']['morning']['temp_avg']
        a[1] = forecasts_today['parts']['night']['temp_avg']

        # Извлекаем скорость ветра
        a[2] = forecasts_today['parts']['day']['wind_speed']

        # Извлекаем влажность
        a[3] = forecasts_today['parts']['day']['humidity']

        # Извлекаем время заката и рассвета
        a[4] = forecasts_today['sunrise']
        a[5] = forecasts_today['sunset']
    # Получаем прогноз погоды на сегодня
    a1 = [None, None, None, None, None, None, None]
    get_weather_info(url_today, a1)
    a1[6] = today_date

    # Получаем прогноз погоды на следующий день
    a2 = [None, None, None, None, None, None, None]
    next_day_date = today_date + timedelta(days=1)
    url_next_day = f'https://api.weather.yandex.ru/v2/forecast?city={city}&date={next_day_date}'
    get_weather_info(url_next_day, a2)
    a2[6] = next_day_date

    # Получаем прогноз погоды на третий день
    a3 = [None, None, None, None, None, None, None]
    third_day_date = today_date + timedelta(days=2)
    url_third_day = f'https://api.weather.yandex.ru/v2/forecast?city={city}&date={third_day_date}'
    get_weather_info(url_third_day, a3)
    a3[6] = third_day_date

    return HttpResponse(f"Достопримечательности города {name}")


def get_wikipedia_page(request):
    # Замените 'en' на язык вашего выбора
    wiki_wiki = wikipediaapi.Wikipedia(
        user_agent='travel/1.0 (anuta.dolgina@gmail.com)', language='en')
    # Замените на название статьи, которую вы хотите получить
    page_name = 'Python (programming language)'

    page = wiki_wiki.page(page_name)
    if page.exists():
        content = page.text
    else:
        content = f"Страница '{page_name}' не найдена на Wikipedia."

    return render(request, "about.html", context={"city": page.summary})
