import json
import os
from datetime import datetime, timezone

import pytz
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from App import models
# Create your views here.
from django.shortcuts import redirect
import json
import random
import string
import nltk
import numpy as np
from keras.saving.save import load_model
from nltk import word_tokenize, PorterStemmer
from nltk.corpus import stopwords

with open('./Chatbot/intents.json', 'r') as file:
    data = json.load(file)

# 提取意图、模式和响应
intents = data['intents']

model = load_model('./Chatbot/TFmodel.h5')
import joblib

# 加载向量器和编码器
current_directory = os.getcwd()
vec_os=os.path.join(current_directory, "App/Chatbot/TF/tfidf_vectorizer.joblib")
vectorizer = joblib.load(vec_os)

enc_os = os.path.join(current_directory, "App/Chatbot/TF/label_encoder.joblib")
encoder = joblib.load(enc_os)


color_list=["blue","orange","yellow","green","white","black"]

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
def predict_intent(processed_text):
    # # 预处理输入文本
    # processed_text = preprocess_text(text)
    # 将处理后的文本转换为适合模型的格式
    input_text = " ".join(processed_text)
    #这个tm只能识别句子，坑，重新和成句子
    input_vector = vectorizer.transform([input_text]).toarray()
    # 使用模型进行预测
    prediction = model.predict(input_vector)
    print(prediction)
    # 获取最可能的类别
    predicted_class = np.argmax(prediction, axis=1)
    print(predicted_class)
    print(prediction[0][predicted_class])
    if prediction[0][predicted_class]<0.75:
        predicted_tag="noting"
    else:
        # 将数值标签转换回原始标签
        predicted_tag = encoder.inverse_transform(predicted_class)[0]
    return predicted_tag

@csrf_exempt
def Ask(request):
    if request.session.get('login')==False:
        return JsonResponse({'data': "", 'reply': "Sorry, you didn't login in, please input your username"})
    ask_text = request.POST.get('Ask')
    processed_text = preprocess_text(ask_text)
    predicted_tag = predict_intent(processed_text)
    print(predicted_tag)
    for i in intents:
        if i['tag']==predicted_tag:
            print(random.choice(i['responses']))
            print(predicted_tag)
            if i['tag']=="product_inquiry_SportsEquipment":
                data_list = models.Product.objects.filter(Kind="sport")
                data=[]
                for j in data_list:
                    d = {}
                    d['id']=j.id
                    d['name']=j.Name
                    d['color'] = j.Color
                    d['kind']=j.Kind
                    d['size']=j.Size
                    d['price']=j.Price
                    data.append(d)
                print(data)
                msg={
                    'data':data,
                    'reply':random.choice(i['responses'])
                }
                return JsonResponse(msg)
            elif i['tag']=="buy_SportsEquipment" or i['tag']=="buy_Stationery":
                tokens = nltk.word_tokenize(ask_text)
                tagged = nltk.pos_tag(tokens)
                colorBool = False
                sizeBool = False
                for (word, pos) in tagged:
                    if pos == "NN" or pos=="NNS":
                        properNouns = word

                    if word in color_list:
                        color = word
                        colorBool = True
                    if pos == "CD":
                        sizeBool = True
                        size = word
                print(properNouns)
                print(colorBool)
                print(sizeBool)

                if colorBool and sizeBool==False:
                    data_list = models.Product.objects.filter(Name__icontains=properNouns,Color=color)
                elif sizeBool and colorBool==False:
                    data_list = models.Product.objects.filter(Name__icontains=properNouns, Size=size)
                elif colorBool and sizeBool:
                    data_list = models.Product.objects.filter(Name__icontains=properNouns, Size=size,Color=color)
                else:
                    data_list = models.Product.objects.filter(Name__icontains=properNouns)
                data = []
                print(data_list)
                if len(data_list)==0:
                    msg = {
                        'data': data,
                        'reply': "sorry, we don't have this product"
                    }
                    return JsonResponse(msg)
                else:
                    for j in data_list:
                        d = {}
                        d['id']=j.id
                        d['name'] = j.Name
                        d['color'] = j.Color
                        d['kind'] = j.Kind
                        d['price'] = j.Price
                        d['size'] = j.Size
                        data.append(d)
                    print(data)
                    msg = {
                        'data': data,
                        'reply': random.choice(i['responses'])
                    }
                    return JsonResponse(msg)
            elif i['tag']=="product_inquiry_Stationery":
                data_list = models.Product.objects.filter(Kind="Stationery")
                data = []
                for j in data_list:
                    d = {}
                    d['id'] = j.id
                    d['name'] = j.Name
                    d['color'] = j.Color
                    d['kind'] = j.Kind
                    d['price'] = j.Price
                    data.append(d)
                print(data)
                msg = {
                    'data': data,
                    'reply': random.choice(i['responses'])
                }
                return JsonResponse(msg)
            elif i['tag'] == "order_status":
                data=[]
                msg = {
                    'data': data,
                    'reply': random.choice(i['responses']),
                    'select':True
                }
                return JsonResponse(msg)
            else:
                msg = {
                    'data': "",
                    'reply': random.choice(i['responses'])
                }
                print(random.choice(i['responses']))
                print(predicted_tag)
                return JsonResponse(msg)
    return JsonResponse({'data': [], 'reply': "Sorry, I didn't understand that."})

@csrf_exempt
def login(request):
    username = request.POST.get('username')
    print(username)
    data_list = models.User.objects.filter(Name=username)
    if len(data_list)>0:
        request.session['login']=True
        request.session['username']=username
        print(request.session.get("id"))
        return JsonResponse({'data': [], 'reply': "login successful.",'login':True})
    else:
        request.session['login']=False
        return JsonResponse({'data': [], 'reply': "Fail.",'login':False})


@csrf_exempt
def buy(request):
    username = request.session.get("username")
    user = models.User.objects.filter(Name=username)
    pid = request.POST.get('pid')
    print(pid)
    print(user[0].id)
    current_time = datetime.now()
    models.Order.objects.create(Uid=user[0].id,Pid=pid,time=current_time)
    return JsonResponse({'data': [], 'reply': "buy successful."})

@csrf_exempt
def refund(request):
    OrderID = request.POST.get("orderid")
    print(OrderID)
    models.Order.objects.get(id=OrderID).delete()
    return JsonResponse({'data': [], 'reply': "Delete successful."})


@csrf_exempt
def order(request):
    select = request.POST.get("select")
    choose = request.POST.get("choose")
    print(choose)
    if choose=="1":
        order_data = models.Order.objects.filter(id=int(select))
        if len(order_data)==0:
            return JsonResponse({'data': [], 'reply': "Sorry, this order ID is incorrect",'orderdata':[]})
        order_data = order_data[0]
        user = models.User.objects.filter(id=order_data.Uid)
        Username = user[0].Name
        address = user[0].Address
        product = models.Product.objects.filter(id=order_data.Pid)
        productName = product[0].Name
        price = product[0].Price
        kind = product[0].Kind
        color = product[0].Color
        d={}
        d['OrderID'] = order_data.id
        d['Username'] = Username
        d['address'] = address
        d['productName'] = productName
        d['price'] = price
        d['kind'] = kind
        d['color'] = color
        d['date'] = order_data.time
        # order_time = datetime.strptime(d['date'], "%Y-%m-%d %H:%M:%S.%f%z")

        # 获取当前时间（同样是aware，即包含时区信息）
        current_time = datetime.now(timezone.utc)

        # 计算时间差
        time_diff = current_time - d['date']
        if abs(time_diff.days)>7:
            d['canRefund'] = False
        else:
            d['canRefund'] = True

        msg = {
            'data': [],
            'reply': "these information is selected by order id.",
            'orderdata': [d]
        }
        return JsonResponse(msg)
    elif choose=="2":
        user = models.User.objects.filter(Name=select)
        if len(user)==0:
            return JsonResponse({'data': [], 'reply': "Sorry,this Username is incorrect.",'orderdata':[]})
        user = user[0]
        data_list = models.Order.objects.filter(Uid=user.id)
        orderdata=[]
        for ord in data_list:
            d={}
            d['OrderID'] = ord.id
            d['Username'] = user.Name
            d['address'] = user.Address
            product = models.Product.objects.filter(id=ord.Pid)[0]
            d['productName'] = product.Name
            d['price'] = product.Price
            d['kind'] = product.Kind
            d['color'] = product.Color
            d['date'] = ord.time
            current_time = datetime.now(timezone.utc)

            # 计算时间差
            time_diff = current_time - d['date']
            if abs(time_diff.days) > 7:
                d['canRefund'] = False
            else:
                d['canRefund'] = True

            orderdata.append(d)
        msg = {
            'data': [],
            'reply': "these information is selected by Username.",
            'orderdata': orderdata
        }
        return JsonResponse(msg)
