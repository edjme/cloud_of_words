import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from stop_words import get_stop_words
import numpy as np
from PIL import Image
import pandas as pd
from fuzzywuzzy import fuzz

# Чтение текста из Excel-файла
excel_file_path = '/Users/stanislavparmut/Documents/progs/cloud_of_words/content/words.xlsx'
df = pd.read_excel(excel_file_path)
text_column_name = 'Text'

# Очистка текста
df[text_column_name] = df[text_column_name].apply(
    lambda x: re.sub(r'==.*?==+', '', str(x)).replace('\n', ''))

# Создание списка русских матерных слов
russian_profanity_list = ['хуй', 'пидор', 'ебать', 'бля', 'блять', 'епты']

# Фильтрация матерных слов из текста
df[text_column_name] = df[text_column_name].apply(lambda x: ' '.join(
    [word for word in str(x).split() if word.lower() not in russian_profanity_list]))

# Объединяем текст в единый текст
text = ' '.join(df[text_column_name].astype(str))

# Продолжаем код для облака слов
STOPWORDS_RU = get_stop_words('russian')

# Замена символов на русские буквы
phrase = ' '.join(df[text_column_name].astype(str)).lower().replace(" ", "")
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

for key, value in d.items():
    for letter in value:
        phrase = phrase.replace(letter, key)

# Проверка на матерные слова и удаление их из текста
profanity_found = False
for word in russian_profanity_list:
    for part in range(len(phrase)):
        fragment = phrase[part: part + len(word)]
        if fuzz.partial_ratio(fragment, word) > 75:
            print("Найдено", word, "\nПохоже на", fragment)
            profanity_found = True
            phrase = phrase.replace(fragment, '')

# Генерация и визуализация облаков слов


def generate_and_plot_wordcloud(width, height, background_color, colormap, mask=None):
    wordcloud = WordCloud(width=width,
                          height=height,
                          max_words=750,
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


if profanity_found:
    # Генерируем и визуализируем облако слов после удаления матерных слов
    generate_and_plot_wordcloud(
        5000, 5000, 'black', 'Pastel1').to_file('hp_cloud_simple.png')
    generate_and_plot_wordcloud(
        3000, 2500, 'white', 'Set2', mask).to_file('hp_upvote.png')
else:
    # Генерируем и визуализируем облако слов без удаления матерных слов
    wordcloud1 = generate_and_plot_wordcloud(2000, 1500, 'black', 'Pastel1')
    wordcloud1.to_file('hp_cloud_simple.png')

    mask_path = '/Users/stanislavparmut/Documents/progs/cloud_of_words/content/mgtu2.png'
    mask = np.array(Image.open(mask_path))
    wordcloud2 = generate_and_plot_wordcloud(2000, 1500, 'white', 'Set2', mask)
    wordcloud2.to_file('hp_upvote.png')
