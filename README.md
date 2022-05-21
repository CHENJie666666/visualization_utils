# visualization_utils
Some useful utils for common visualization

## 1. 词云

### 1.1 英文文本转词云

支持含有英文内容的文本生成词云，可根据词频绘制

- 安装包

```shell
pip install wordcloud
pip install pyyaml
pip install numpy
pip install multidict
```

- 修改`params_en_wc.yml`文件
- 调用`wordcloud_generator_from_en.py`文件（第二个参数可不给）

```shell
python wordcloud_generator_from_en.py './temp.txt' './wordcloud.png'
```

### 1.2 中文文本转词云

支持含有中文内容的文本生成词云，可根据词频绘制

- 安装包

```shell
pip install wordcloud
pip install pyyaml
pip install numpy
pip install multidict
pip install jieba
```

- 修改`params_zh_wc.yml`文件（可添加自定义词及stopwords）
- 调用`wordcloud_generator_from_en.py`文件（第二个参数可不给）

```shell
python wordcloud_generator_from_zh.py './temp2.txt' './wordcloud2.png'
```

### 1.3 excel文件转词云

支持对excel文件生成词云，并可自定义颜色

- 安装包

```shell
pip install wordcloud
pip install pyyaml
pip install numpy
pip install pandas
pip install openpyxl
```

- 修改`params_excel_wc`.yml文件
- 调用`wordcloud_generator_from_excel.py`文件（第二个参数可不给）

```shell
python wordcloud_generator_from_excel.py './temp3.xlsx' './wordcloud3.png'
```


