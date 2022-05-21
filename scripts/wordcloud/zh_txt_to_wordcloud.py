import sys
import yaml
import jieba
import multidict as multidict
import numpy as np
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator


# 获取词频
def getFrequencyDictForText(sentence):
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}
 
    for text in sentence.split(" "):
        val = tmpDict.get(text, 0)
        tmpDict[text.lower()] = val + 1
    for key in tmpDict:
        fullTermsDict.add(key,tmpDict[key])
    return fullTermsDict


def get_params(yaml_path):
    """
    读取yaml配置
    """
    with open(yaml_path, 'r', encoding="utf-8") as f:
        file = f.read()
        params = yaml.load(file, Loader=yaml.FullLoader)
        # print(params)
    return params

def add_user_word_list(user_word_file_path):
    """
    从txt文件中读取用户自定义词语
    """
    with open(user_word_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    user_words_list = list(set([i.split('\n')[0] for i in lines if i != '\n']))
    
    for i in user_words_list:
        jieba.add_word(i)


def segmentation(txt_file):
    """
    jieba分词
    """
    with open(txt_file, 'r', encoding='utf-8') as f:
        text = f.read()
    # print(text)
    return jieba.lcut(text, cut_all=False)


def delete_stopword(text, stopwords_file_path):
    """
    删除停用词
    """
    with open(stopwords_file_path, 'r', encoding='utf-8') as f:
        sw = f.read()
    stopwords = sw.split('\n')
    stopwords = list(set(stopwords))
    # print(stopwords)

    words = []
    for word in text:
        if word.strip() in stopwords or word == '\n':
            # print(word)
            continue
        else:
            words.append(word.strip())

    return words


def text_to_wordcloud(text, save_file, params):
    """
    由txt文件生成词云
    """    
    if params['from_frequencies']:
        if params['mask']:
            wordcloud = WordCloud(
                width=params['width'], 
                height=params['height'], 
                margin=2,
                mask=np.array(Image.open(params['mask'])),
                contour_width=params['contour_width'],
                min_font_size=params['min_font_size'],
                max_font_size=params['max_font_size'],
                font_path=params['font_path'],
                prefer_horizontal=params['prefer_horizontal'],
                max_words=params['max_words'],
                relative_scaling=params['relative_scaling'],
                regexp=params['regexp'],
                collocations=params['collocations'],
                normalize_plurals=params['normalize_plurals'],
                include_numbers=params['include_numbers'],
                min_word_length=params['min_word_length'],
                background_color=params['background_color'],
                mode=params['mode'],
                colormap=params['colormap'],
                # color_func=params['color_func'],   
                color_func=ImageColorGenerator(np.array(Image.open(params['mask'])))     
            ).generate_from_frequencies(getFrequencyDictForText(text))
        else:
            wordcloud = WordCloud(
                width=params['width'], 
                height=params['height'], 
                margin=2,
                contour_width=params['contour_width'],
                min_font_size=params['min_font_size'],
                max_font_size=params['max_font_size'],
                font_path=params['font_path'],
                prefer_horizontal=params['prefer_horizontal'],
                max_words=params['max_words'],
                relative_scaling=params['relative_scaling'],
                regexp=params['regexp'],
                collocations=params['collocations'],
                normalize_plurals=params['normalize_plurals'],
                include_numbers=params['include_numbers'],
                min_word_length=params['min_word_length'],
                background_color=params['background_color'],
                mode=params['mode'],
                colormap=params['colormap'],
                color_func=params['color_func'],    
            ).generate_from_frequencies(getFrequencyDictForText(text))
    else:
        if params['mask']:
            wordcloud = WordCloud(
                width=params['width'], 
                height=params['height'], 
                margin=2,
                mask=np.array(Image.open(params['mask'])),
                contour_width=params['contour_width'],
                min_font_size=params['min_font_size'],
                max_font_size=params['max_font_size'],
                font_path=params['font_path'],
                prefer_horizontal=params['prefer_horizontal'],
                max_words=params['max_words'],
                relative_scaling=params['relative_scaling'],
                regexp=params['regexp'],
                collocations=params['collocations'],
                normalize_plurals=params['normalize_plurals'],
                include_numbers=params['include_numbers'],
                min_word_length=params['min_word_length'],
                background_color=params['background_color'],
                mode=params['mode'],
                colormap=params['colormap'],
                # color_func=params['color_func'],   
                color_func=ImageColorGenerator(np.array(Image.open(params['mask'])))     
            ).generate(text)
        else:
            wordcloud = WordCloud(
                width=params['width'], 
                height=params['height'], 
                margin=2,
                contour_width=params['contour_width'],
                min_font_size=params['min_font_size'],
                max_font_size=params['max_font_size'],
                font_path=params['font_path'],
                prefer_horizontal=params['prefer_horizontal'],
                max_words=params['max_words'],
                relative_scaling=params['relative_scaling'],
                regexp=params['regexp'],
                collocations=params['collocations'],
                normalize_plurals=params['normalize_plurals'],
                include_numbers=params['include_numbers'],
                min_word_length=params['min_word_length'],
                background_color=params['background_color'],
                mode=params['mode'],
                colormap=params['colormap'],
                color_func=params['color_func'],    
            ).generate(text)
    wordcloud.to_file(save_file)


if __name__ == '__main__':
    
    txt_file = sys.argv[1]    
    
    try: 
        save_file = sys.argv[2]
    except:
        save_file = txt_file.rsplit('.', 1)[0] + '.png'    
    
    params = get_params('./params_zh_wc.yml')
    
    print('loading: read file')
    words = segmentation(txt_file)

    if params['user_word_file_path']:
        print('loading: add user words')
        add_user_word_list(params['user_word_file_path'])
    else:
        print('loading: no user words')
    

    if params['stopwords_file_path']:
        print('loading: delete stopwords')
        words = delete_stopword(words, params['stopwords_file_path'])
    else:
        print('loading: no stopwords')

    words = ' '.join(words)
    print('loading: generate wordcloud')
    text_to_wordcloud(words, save_file, params)
    print('The wordcloud file has been saved as {}'.format(save_file))

