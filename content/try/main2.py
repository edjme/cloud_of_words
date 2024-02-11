# Импортируем нужные библиотеки
import wikipedia
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from stop_words import get_stop_words
import numpy as np
from PIL import Image

# Выбираем язык Википедии и интересующую нас страницу
wikipedia.set_lang("ru")
wiki = wikipedia.page('Гарри Поттер')

# Извлекаем и очищаем текст из полученной страницы
text = re.sub(r'==.*?==+', '', wiki.content).replace('\n', '')

# Импортируем инструменты для облака слов и списки стоп-слов
STOPWORDS_RU = get_stop_words('russian')

# Генерируем и визуализируем облако слов


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
mask = np.array(Image.open(
    '/Users/stanislavparmut/Documents/progs/cloud_of_words/content/mgtu2.png'))
wordcloud2 = generate_and_plot_wordcloud(2000, 1500, 'white', 'Set2', mask)
wordcloud2.to_file('hp_upvote.png')
