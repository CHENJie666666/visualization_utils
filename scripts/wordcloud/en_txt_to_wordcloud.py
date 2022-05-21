import sys
from wordcloud import WordCloud, ImageColorGenerator
import yaml
import numpy as np
from PIL import Image
import multidict as multidict
import re


def get_params(yaml_path):
    """
    读取yaml配置
    """
    with open(yaml_path, 'r', encoding="utf-8") as f:
        file = f.read()
        params = yaml.load(file, Loader=yaml.FullLoader)
        # print(params)
    return params

def txt_to_wordcloud(txt_file, save_file, params):
    """
    由txt文件生成词云
    """ 
    with open(txt_file, 'r', encoding='utf-8') as f:
        text = f.read()

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
                stopwords=params['stopwords'],
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
                stopwords=params['stopwords'],
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
                stopwords=params['stopwords'],
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
                stopwords=params['stopwords'],
                normalize_plurals=params['normalize_plurals'],
                include_numbers=params['include_numbers'],
                min_word_length=params['min_word_length'],
                background_color=params['background_color'],
                mode=params['mode'],
                colormap=params['colormap'],
                color_func=params['color_func'],    
            ).generate(text)
    
    wordcloud.to_file(save_file)

def getFrequencyDictForText(sentence):
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}
 
    # making dict for counting frequencies
    for text in sentence.split(" "):
        if re.match("a|the|an|the|to|in|for|of|or|by|with|is|on|that|be", text):
            continue
        val = tmpDict.get(text, 0)
        tmpDict[text.lower()] = val + 1
    for key in tmpDict:
        fullTermsDict.add(key,tmpDict[key])
    return fullTermsDict

if __name__ == '__main__':
    txt_file = sys.argv[1]    
    try: 
        save_file = sys.argv[2]
    except:
        save_file = txt_file.rsplit('.', 1)[0] + '.png'    
    # print(save_file)
    params = get_params('./params_en_wc.yml')
    txt_to_wordcloud(txt_file, save_file, params)
    print('The wordcloud file has been saved as {}'.format(save_file))




