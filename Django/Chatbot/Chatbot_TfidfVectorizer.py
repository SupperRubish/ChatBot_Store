# 假设你的JSON文件名为'intents.json'
import json
import random
import string
from pprint import pprint

import numpy as np
from keras.callbacks import EarlyStopping
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer #词袋
import nltk
from nltk import word_tokenize, PorterStemmer
from nltk.corpus import stopwords
# nltk.download('stopwords')

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from sklearn.metrics import f1_score

# 加载JSON文件
with open('intents.json', 'r') as file:
    data = json.load(file)

# 提取意图、模式和响应
intents = data['intents']

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



# print(preprocess_text("I live in Nottingham, and I am a master"))
#
patterns = []
tags = []
#
# # 遍历每个意图
for intent in intents:
    # 遍历每个模式
    for pattern in intent['patterns']:
        # 应用预处理函数
        words = preprocess_text(pattern)
        # 添加处理后的单词到模式列表
        patterns.append(words)
        # 添加对应的标签到标签列表
        tags.append(intent['tag'])
print(patterns)
print(tags)

# paired_list = list(zip(patterns, tags))
# random.shuffle(paired_list)
# patterns, tags = zip(*paired_list)
# patterns = list(patterns)
# tags = list(tags)
#
# print(patterns)
# print(tags)




from sklearn.feature_extraction.text import TfidfVectorizer

patterns = [" ".join(pattern) for pattern in patterns]
# 初始化TF-IDF向量器
vectorizer = TfidfVectorizer()

# 向量化文本数据
X = vectorizer.fit_transform(patterns).toarray()
print(X.shape)

from sklearn.preprocessing import LabelEncoder

# 初始化标签编码器
encoder = LabelEncoder()

# 编码标签
y = encoder.fit_transform(tags)



import joblib

# 保存TF-IDF向量器和标签编码器
joblib.dump(vectorizer, './TF/tfidf_vectorizer.joblib')
joblib.dump(vectorizer, '../App/Chatbot/TF/tfidf_vectorizer.joblib')

joblib.dump(encoder, './TF/label_encoder.joblib')
joblib.dump(encoder, '../App/Chatbot/TF/label_encoder.joblib')
# 定义模型
model = Sequential()
model.add(Dense(128, input_shape=(X.shape[1],), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(set(tags)), activation='softmax'))  # 输出层节点数为标签的数量



from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train)
print(y_train)
# 编译模型
model.compile(loss='sparse_categorical_crossentropy',
              optimizer=Adam(lr=0.0005),
              metrics=['accuracy'])

# 训练模型
history = model.fit(X_train, y_train, epochs=300, batch_size=5, validation_split=0.1)

plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(loc='upper left')
plt.show()

loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {accuracy}")

predictions = model.predict(X_test)
# 因为模型的输出是 softmax 概率，我们需要取最大概率的索引作为预测的类别
predicted_classes = np.argmax(predictions, axis=1)

# 计算 F1 分数
f1 = f1_score(y_test, predicted_classes, average='weighted')
print(f"F1 Score: {f1}")

model.save('TFmodel.h5')
model.save('../App/Chatbot/TFmodel.h5')

# import joblib
#
# # 加载向量器和编码器
# vectorizer = joblib.load('tfidf_vectorizer.joblib')
# encoder = joblib.load('label_encoder.joblib')
# def predict_intent(text):
#     # 预处理输入文本
#     processed_text = preprocess_text(text)
#     # 将处理后的文本转换为适合模型的格式
#     input_text = " ".join(processed_text)
#     # 向量化输入文本
#     input_vector = vectorizer.transform([input_text]).toarray()
#     # 使用模型进行预测
#     prediction = model.predict(input_vector)
#     # 获取最可能的类别
#     predicted_class = np.argmax(prediction, axis=1)
#     # 将数值标签转换回原始标签
#     predicted_tag = encoder.inverse_transform(predicted_class)[0]
#     return predicted_tag
#
# # 测试示例
# test_text = "Hello, how are you?"
# predicted_tag = predict_intent(test_text)
# print(f"Predicted intent: {predicted_tag}")

