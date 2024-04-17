import re

import nltk


# tokens = nltk.word_tokenize("i want to buy a yellow basketball")
# print(tokens)
# tagged = nltk.pos_tag(tokens)
# print(tagged)
# properNouns = [ word for (word, pos) in tagged if pos=="JJ" ]
# print(properNouns[0])



pattern = r"'([^,]+)'"

# 使用 re.findall() 查找所有匹配项
matches = re.findall(pattern, "basketball,please")

print(matches)

from nltk.tokenize import word_tokenize
from nltk import pos_tag

sentence = "7 size and blue basketball,please"

# 分词
tokens = nltk.word_tokenize(sentence)
print(tokens)

# 词性标注
tagged = nltk.pos_tag(tokens)
print(tagged)

# 初始化颜色和商品变量
color = None
product = None

# 假设颜色紧跟在描述词"JJ"后面，商品是名词"NN"
for word, tag in tagged:
    if tag == 'JJ':  # 形容词，假设它是颜色
        color = word
    elif tag == 'NN' and color:  # 名词，且已经找到颜色，假设它是商品
        product = word
        break  # 找到商品后就退出循环

print(f"Color: {color}, Product: {product}")
