# - * - coding: utf - 8 -*-
"""
create wordcloud with chinese
=============================

Wordcloud is a very good tool, but if you want to create
Chinese wordcloud only wordcloud is not enough. The file
shows how to use wordcloud with Chinese. First, you need a
Chinese word segmentation library jieba, jieba is now the
most elegant the most popular Chinese word segmentation tool in python.
You can use 'PIP install jieba'. To install it. As you can see,
at the same time using wordcloud with jieba very convenient
"""
from os import path
import matplotlib.pyplot as plt     #数学绘图库
import jieba               #导入jieba库（分词库）
#from wordcloud import WordCloud   #词云库
from wordcloud import WordCloud, ImageColorGenerator
import numpy 
from imageio import imread
import PIL.Image as Image ##图像转换
import jieba.analyse   

#jieba.enable_parallel(4)
# Setting up parallel processes :4 ,but unable to run on Windows

# add userdict by load_userdict()
jieba.load_userdict("txt/userdict.txt") #加载用户字典。

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
#d = path.dirname(__file__)

stopwords_path = d + '\\txt\\CS.txt' # 设置stopword路径
back_coloring_path = d + '\\img\\background.jpg' # 设置背景图片椭圆路径

# Chinese fonts must be set
#font_path = d + '/fonts/SourceHanSerif/SourceHanSerifK-Light.otf'
font_path = 'C:\Windows\Fonts\simkai.ttf' # 为matplotlib设置中文字体路径
# the path to save worldcloud
imgname1 = d + '\\img\\background1.png'
imgname2 = d + '\\img\\backgroundblack.png'

# read the mask / color image taken from
back_coloring = imread(path.join(d, back_coloring_path))# 设置背景图片

# Read the whole text.
#text = open(path.join(d, d + 'txt/竺可桢日记史料札记.送出版社审阅11.22修正稿.txt')).read()
#text = open("txt/竺可桢全集_第06卷-11卷1936-1949.txt", encoding="utf-8").read() 
text = open("txt/竺可桢日记史料札记.送出版社审阅11.22修正稿.txt", encoding="utf-8").read() 

# if you want use wordCloud,you need it
# add userdict by add_word()
userdict_list = ['西迁之路', '求是', '校务会议']


# The function for processing text with Jieba
def jieba_processing_txt(text):
    for word in userdict_list:
        jieba.add_word(word)

    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr = "/ ".join(seg_list)

    with open(stopwords_path, encoding='utf-8') as f_stop:
        f_stop_text = f_stop.read()
        f_stop_seg_list = f_stop_text.splitlines()

    for myword in liststr.split('/'):
        if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
            mywordlist.append(myword)
    return ' '.join(mywordlist)


wc = WordCloud(font_path=font_path, background_color="white", max_words=100, mask=back_coloring,
               max_font_size=100, random_state=56, width=600, height=460, margin=2,mode='RGB',
               colormap='gist_gray',scale=25,#contour_width=2,contour_color='blue'
)


wc.generate(jieba_processing_txt(text))

# create coloring from image
image_colors_default = ImageColorGenerator(back_coloring)

plt.figure()
# recolor wordcloud and show
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()

# save wordcloud
wc.to_file(path.join(d, imgname1))

# create coloring from image
image_colors_byImg = ImageColorGenerator(back_coloring)

# show
# we could also give color_func=image_colors directly in the constructor
plt.title("Custom colors")
plt.imshow(wc.recolor(color_func=image_colors_byImg), cmap=plt.cm.gray, interpolation="bilinear")
plt.axis("off")
plt.figure()
plt.imshow(back_coloring, interpolation="bilinear")
plt.axis("off")
plt.show()

# save wordcloud
wc.to_file(path.join(d, imgname2))
