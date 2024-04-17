# 假设你的JSON文件名为'intents.json'
import json
import string
from pprint import pprint

import numpy as np
from keras.callbacks import EarlyStopping
from sklearn.feature_extraction.text import CountVectorizer #词袋
import nltk
from nltk import word_tokenize, PorterStemmer
from nltk.corpus import stopwords
# nltk.download('stopwords')

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam



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
#
#
from sklearn.feature_extraction.text import CountVectorizer #词袋

# 将分词列表转换回句子
patterns = [" ".join(pattern) for pattern in patterns]
print(patterns)
# 初始化CountVectorizer来转换文本
vectorizer = CountVectorizer()

# 应用CountVectorizer,这个tm只能识别句子，坑
X = vectorizer.fit_transform(patterns).toarray()

pprint(X)

from sklearn.preprocessing import LabelEncoder

# 初始化LabelEncoder
encoder = LabelEncoder()

# 转换标签为数值
y = encoder.fit_transform(tags)
pprint(y)



# 定义模型
model = Sequential()
model.add(Dense(128, input_shape=(X.shape[1],), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(set(tags)), activation='softmax'))  # 输出层节点数为标签的数量


# 编译模型
model.compile(loss='sparse_categorical_crossentropy',
              optimizer=Adam(learning_rate=0.001),
              metrics=['accuracy'])


from sklearn.model_selection import train_test_split

# 划分数据集
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 然后划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# 训练模型
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)



history = model.fit(X_train, y_train, epochs=500, batch_size=5, verbose=1, validation_split=0.1)

from sklearn.metrics import accuracy_score, f1_score

# 进行预测
y_pred_probs = model.predict(X_test)
y_pred = np.argmax(y_pred_probs, axis=1)  # 获取预测类别的索引

# 计算准确率
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

# 计算F1分数，需要指定平均方法，例如'micro', 'macro', 或 'weighted'
f1 = f1_score(y_test, y_pred, average='weighted')
print(f'F1 Score: {f1}')
model.save('./model.h5')


# 评估模型
# loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
# print('Test accuracy:', accuracy)

# 使用模型进行预测
# y_pred = model.predict(X_test)

# print(y_pred)
# print(y_test)
# y_pred_classes = np.argmax(y_pred, axis=1)
# print(y_pred_classes)
# s = []
# for i in y_pred_classes:
#     s.append(tags[i])
# print(s)
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

# 测试示例
status = True
while status:
    test_text = input("you:")
    # test_text = "can i use card to pay?"
    if test_text=="exit()":
        status=False
    predicted_tag = predict_intent(test_text)
    print(f"Predicted intent: {predicted_tag}")
