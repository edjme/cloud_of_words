import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from stop_words import get_stop_words
import numpy as np
from PIL import Image
import pandas as pd

# Чтение текста из Excel-файла
excel_file_path = '/Users/stanislavparmut/Documents/progs/cloud_of_words/content/words.xlsx'
df = pd.read_excel(excel_file_path)
text_column_name = 'Text'  # Замените на имя столбца с текстом в вашем файле

# Очистка текста
df[text_column_name] = df[text_column_name].apply(
    lambda x: re.sub(r'==.*?==+', '', str(x)).replace('\n', ''))

# Создание списка русских матерных слов (пример)
russian_profanity_list = ['блять', 'ебать', 'мат1', '...']

# Объединяем текст в единый текст
text = ' '.join(df[text_column_name].astype(str))

# Продолжаем код для облака слов
STOPWORDS_RU = get_stop_words('russian')


def is_profane(word):
    for profane_word in russian_profanity_list:
        if distance(word, profane_word) <= len(profane_word) * 0.15:
            return True
    return False


def distance(a, b):
    "Вычисляет расстояние Левенштейна между строками a и b."
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + \
                1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


# Определение переменной mask
mask_path = '/Users/stanislavparmut/Documents/progs/cloud_of_words/content/mgtu2.png'
mask = np.array(Image.open(mask_path))

STOPWORDS_RU = get_stop_words('russian')


def generate_and_plot_wordcloud(width, height, background_color, colormap, mask=None):
    wordcloud = WordCloud(width=width,
                          height=height,
                          random_state=1,
                          background_color=background_color,
                          margin=20,
                          colormap=colormap,
                          collocations=False,
                          stopwords=STOPWORDS_RU,
                          mask=mask).generate(text)

    plt.figure(figsize=(30, 20))
    plt.imshow(wordcloud)
    plt.axis("off")

    return wordcloud


# Фраза, которую будем проверять.
phrase = ' '.join(df[text_column_name].astype(str)).lower().replace(" ", "")

# Флаг для отслеживания наличия матерных слов в тексте
profanity_found = False

# Проходимся по всем словам в тексте
for word in text.split():
    # Приводим слово к нижнему регистру и убираем пробелы
    cleaned_word = word.lower().replace(" ", "")

    # Проверяем, не является ли слово матерным
    if not is_profane(cleaned_word):
        # Если не матерное, добавляем в текст для облака слов
        phrase += " " + cleaned_word
    else:
        # Если матерное слово, устанавливаем флаг и не добавляем в текст для облака слов
        profanity_found = True

if not profanity_found:
    # Если матерных слов не найдено, генерируем и визуализируем облако слов
    generate_and_plot_wordcloud(
        2000, 1500, 'black', 'Pastel1').to_file('hp_cloud_simple.png')
    generate_and_plot_wordcloud(
        2000, 1500, 'white', 'Set2', mask).to_file('hp_upvote.png')
else:
    print("Матерные слова обнаружены, облако слов будет сгенерировано без них.")
