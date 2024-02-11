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
russian_profanity_list = ['мат3', 'мат2', 'мат1', '...']

# Фильтрация матерных слов из текста
df[text_column_name] = df[text_column_name].apply(lambda x: ' '.join(
    [word for word in str(x).split() if word.lower() not in russian_profanity_list]))

# Объединяем текст в единый текст
text = ' '.join(df[text_column_name].astype(str))

# Продолжаем код для облака слов
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


# Генерируем и визуализируем облако слов на черном фоне
wordcloud1 = generate_and_plot_wordcloud(2000, 1500, 'black', 'Pastel1')
wordcloud1.to_file('hp_cloud_simple.png')

# Генерируем и визуализируем облако слов с использованием маски
mask_path = '/Users/stanislavparmut/Documents/progs/cloud_of_words/content/mgtu3.png'
mask = np.array(Image.open(mask_path))
wordcloud2 = generate_and_plot_wordcloud(2000, 1500, 'white', 'Set2', mask)
wordcloud2.to_file('hp_upvote.png')

# Фраза, которую будем проверять.
phrase = ' '.join(df[text_column_name].astype(str)).lower().replace(" ", "")


def distance(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n, m)) space
        a, b = b, a
        n, m = m, n

    # Keep current and previous row, not entire matrix
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


d = {'а': ['а', 'a', '@'],
     'б': ['б', '6', 'b'],
     'в': ['в', 'b', 'v'],
     'г': ['г', 'r', 'g'],
     'д': ['д', 'd'],
     'е': ['е', 'e'],
     'ё': ['ё', 'e'],
     'ж': ['ж', 'zh', '*'],
     'з': ['з', '3', 'z'],
     'и': ['и', 'u', 'i'],
     'й': ['й', 'u', 'i'],
     'к': ['к', 'k', 'i{', '|{'],
     'л': ['л', 'l', 'ji'],
     'м': ['м', 'm'],
     'н': ['н', 'h', 'n'],
     'о': ['о', 'o', '0'],
     'п': ['п', 'n', 'p'],
     'р': ['р', 'r', 'p'],
     'с': ['с', 'c', 's'],
     'т': ['т', 'm', 't'],
     'у': ['у', 'y', 'u'],
     'ф': ['ф', 'f'],
     'х': ['х', 'x', 'h', '}{'],
     'ц': ['ц', 'c', 'u,'],
     'ч': ['ч', 'ch'],
     'ш': ['ш', 'sh'],
     'щ': ['щ', 'sch'],
     'ь': ['ь', 'b'],
     'ы': ['ы', 'bi'],
     'ъ': ['ъ'],
     'э': ['э', 'e'],
     'ю': ['ю', 'io'],
     'я': ['я', 'ya']
     }

# Флаг для отслеживания наличия матерных слов в тексте
profanity_found = False

for key, value in d.items():
    # Проходимся по каждой букве в значении словаря. То есть по вот этим спискам ['а', 'a', '@'].
    for letter in value:
        # Проходимся по каждой букве в нашей фразе.
        for phr in phrase:
            # Если буква совпадает с буквой в нашем списке.
            if letter == phr:
                # Заменяем эту букву на ключ словаря.
                phrase = phrase.replace(phr, key)

# Проходимся по всем словам.
for word in russian_profanity_list:
    # Разбиваем слово на части, и проходимся по ним.
    for part in range(len(phrase)):
        # Вот сам наш фрагмент.
        fragment = phrase[part: part + len(word)]
        # Если отличие этого фрагмента меньше или равно 25% этого слова, то считаем, что они равны.
        if distance(fragment, word) <= len(word) * 0.15:
            # Если они равны, выводим надпись о их нахождении.
            print("Найдено", word, "\nПохоже на", fragment)
            profanity_found = True
            # Убираем найденное матерное слово из текста
            phrase = phrase.replace(fragment, '')
            # Можно использовать continue, чтобы продолжить проверку для других частей слова


if not profanity_found:
    # Если матерных слов не найдено, генерируем и визуализируем облако слов
    generate_and_plot_wordcloud(
        2000, 1500, 'black', 'Pastel1').to_file('hp_cloud_simple.png')
    generate_and_plot_wordcloud(
        2000, 1500, 'white', 'Set2', mask).to_file('hp_upvote.png')
