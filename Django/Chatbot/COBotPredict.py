import string

import numpy as np
from keras.saving.save import load_model
from nltk import word_tokenize, PorterStemmer
from nltk.corpus import stopwords

from ChatTest.Chatbot_CountVectorizer import vectorizer, encoder

model = load_model('model.h5')
def preprocess_text(text):
    # 转换为小写
    text = text.lower()
    # 移除标点
    text = text.translate(str.maketrans('', '', string.punctuation))
    # 分词
    words = word_tokenize(text)
    # 可选：移除停用词
    words = [word for word in words if word not in stopwords.words('english')]
    # 可选：词干提取
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    return words
def predict_intent(text):
    # 预处理输入文本
    processed_text = preprocess_text(text)
    # 将处理后的文本转换为适合模型的格式
    input_text = " ".join(processed_text)
    #这个tm只能识别句子，坑，重新和成句子
    input_vector = vectorizer.transform([input_text]).toarray()
    # 使用模型进行预测
    prediction = model.predict(input_vector)
    # 获取最可能的类别
    predicted_class = np.argmax(prediction, axis=1)
    # 将数值标签转换回原始标签
    predicted_tag = encoder.inverse_transform(predicted_class)[0]
    return predicted_tag

status = True
while status:
    test_text = input("you:")
    # test_text = "can i use card to pay?"
    if test_text=="exit()":
        status=False
    predicted_tag = predict_intent(test_text)
    print(f"Predicted intent: {predicted_tag}")