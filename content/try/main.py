# Импортируем нужные библиотеки
import wikipedia
import re

# Выбираем язык Википедии и интересующую нас страницу
wikipedia.set_lang("ru")
wiki = wikipedia.page('Гарри Поттер')

# Извлекаем текст из полученной страницы
text = wiki.content

# Очищаем текст с помощью регулярных выражений
text = re.sub(r'==.*?==+', '', text)  # удаляем лишние символы
text = text.replace('\n', '')  # удаляем знаки разделения на абзацы

# ------
# Импортируем библиотеку для визуализации
import matplotlib.pyplot as plt
%matplotlib inline


# Функция для визуализации облака слов
def plot_cloud(wordcloud):
    # Устанавливаем размер картинки
    plt.figure(figsize=(30, 20))
    # Показать изображение
    plt.imshow(wordcloud)
    # Без подписей на осях
    plt.axis("off")

# -------
    
# Импортируем инструменты для облака слов и списки стоп-слов
from wordcloud import WordCloud
from stop_words import get_stop_words


# Записываем в переменную стоп-слова русского языка
STOPWORDS_RU = get_stop_words('russian')

# Генерируем облако слов
wordcloud = WordCloud(width = 2000,
                      height = 1500,
                      random_state=1,
                      background_color='black',
                      margin=20,
                      colormap='Pastel1',
                      collocations=False,
                      stopwords = STOPWORDS_RU).generate(text)

# Рисуем картинку
plot_cloud(wordcloud)

# ------

# Сохраним получившуюся картинку в файл
wordcloud.to_file('hp_cloud_simple.png')


# -----

# Импортируем необходимое
import numpy as np
from PIL import Image


# Превращаем картинку в маску
mask = np.array(Image.open('/content/comment.png'))

# Генерируем облако слов
wordcloud = WordCloud(width = 2000,
                      height = 1500,
                      random_state=1,
                      background_color='white',
                      colormap='Set2',
                      collocations=False,
                      stopwords = STOPWORDS_RU,
                      mask=mask).generate(text)

# Выводим его на экран
plot_cloud(wordcloud)


# -------

wordcloud.to_file('hp_upvote.png')