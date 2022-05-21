import sys
import yaml
import numpy as np
from PIL import Image
from wordcloud import WordCloud, get_single_color_func
import pandas as pd


def get_params(yaml_path):
    """
    读取yaml配置
    """
    with open(yaml_path, 'r', encoding="utf-8") as f:
        file = f.read()
        params = yaml.load(file, Loader=yaml.FullLoader)
        # print(params)
    return params


class GroupedColorFunc(object):
    """
    生成颜色函数
    """ 
    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]
 
        self.default_color_func = get_single_color_func(default_color)
 
    def get_color_func(self, word):
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func
 
        return color_func
 
    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)


def color_func_generator(data, params):
    """
    根据用户输入颜色设置生成颜色函数
    """
    new_data = data.dropna()

    color_to_words = {}
    for color in new_data['color'].unique().tolist():
        data_temp = data[data['color'] == color]
        color_to_words[color] = data_temp['string'].values.tolist()
    
    if color_to_words:
        default_txt_color = params['default_txt_color']
        return GroupedColorFunc(color_to_words, default_txt_color)
    else:
        return None


def excel_to_wordcloud(excel_path, save_file, params):
    """
    由excel文件生成词云
    """
    data = pd.read_excel(excel_path, sheet_name='词云')

    strings = data['string'].values.tolist()
    new_strings = [i.strip() for i in strings]
    weights = data['weight'].values.tolist()
    
    frequency_dict = dict(zip(new_strings, weights))

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
            repeat=True,
            collocations=False,
            background_color=params['background_color'],
            mode=params['mode'],
            color_func=color_func_generator(data, params),  
        ).generate_from_frequencies(frequency_dict)
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
            repeat=True,
            collocations=False,
            background_color=params['background_color'],
            mode=params['mode'],
            color_func=color_func_generator(data, params),    
        ).generate_from_frequencies(frequency_dict)
    
    wordcloud.to_file(save_file)


if __name__ == '__main__':
    
    excel_path = sys.argv[1]    
    
    try: 
        save_file = sys.argv[2]
    except:
        save_file = excel_path.rsplit('.', 1)[0] + '.png'    
    
    params = get_params('./params_excel_wc.yml')

    print('loading: generate wordcloud')
    excel_to_wordcloud(excel_path, save_file, params)
    print('The wordcloud file has been saved as {}'.format(save_file))

