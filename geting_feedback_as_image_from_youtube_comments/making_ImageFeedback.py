from wordcloud import WordCloud
from PIL import Image

def wordcloud_Func(text, file_name):
    wc = WordCloud(width=800, height=400)
    wc.generate(text)

    wc.to_file('image\{}.png'.format(file_name))

def showFeedback(file_name):
    im = Image.open('image\{}.png'.format(file_name))
    im.show()
