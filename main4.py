import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from stop_words import get_stop_words
import numpy as np
from PIL import Image
import pandas as pd

# Чтение текста из Excel-файла
excel_file_path = './content/obrazec.xlsx'
df = pd.read_excel(excel_file_path)
text_column_name = 'Text'  # Замените на имя столбца с текстом в вашем файле

# Очистка текста
df[text_column_name] = df[text_column_name].apply(
    lambda x: re.sub(r'==.*?==+', '', str(x)).replace('\n', ''))

# Создание списка русских матерных слов (пример)
russian_profanity_list = ['хуй', 'пизда', 'бля', 'блять', 'епты', 'пиздец',
                          'ахуеть', 'ебать', 'еба', 'сука', 'сучка', 'пидор', 'блядина', 'нахуй']

russian_profanity_list = [' ']

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
wordcloud1 = generate_and_plot_wordcloud(3000, 2000, 'black', 'Pastel1')
wordcloud1.to_file('hp_cloud_simple.png')

# Генерируем и визуализируем облако слов с использованием маски
mask_path = './content/mgtu2.png'
mask = np.array(Image.open(mask_path))
wordcloud2 = generate_and_plot_wordcloud(3000, 2000, 'black', 'Set2', mask)
wordcloud2.to_file('hp_upvote.png')
