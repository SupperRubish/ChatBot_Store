import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

data = pd.read_csv('/Users/chengmouren/Downloads/penguins_modfeats_CLEAN.csv')
# #
# labels_dict = {
#         'Adelie': 0,  # Assuming 'circle.xls' corresponds to the 'circle' gesture
#         'Chinstrap': 1,  # Assuming 'come.xls' corresponds to the 'come here' gesture
#         'Gentoo': 2,  # Assuming 'go.xls' corresponds to the 'go away' gesture
# }
# dataframes = []
# for i in range(len(test_file)):
#     if test_file.iloc[i,4]=="Adelie":
#         AF = test_file.iloc[i].copy()
#         AF['species']=0
#         dataframes.append(AF)
#     elif test_file.iloc[i,4]=="Chinstrap":
#         AF = test_file.iloc[i].copy()
#         AF['species']=1
#         dataframes.append(AF)
#     elif test_file.iloc[i,4]=="Gentoo":
#         AF = test_file.iloc[i].copy()
#         AF['species']=2
#         dataframes.append(AF)
# print(dataframes)
# combined_data = pd.concat(dataframes, ignore_index=True)
# print(combined_data)




# 选择输入变量和目标变量
features = data[['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']]
target = data['species']

# 划分训练集和测试集，比例为70%训练集，30%测试集，随机种子为42
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

# 初始化变量来存储准确率
accuracies = []

# 尝试不同的K值，这里假设我们尝试2到100
k_values = range(2, 101)

# 对每个K值进行迭代
for k in k_values:
    # 创建KNN模型实例
    knn = KNeighborsClassifier(n_neighbors=k)
    # 训练模型
    knn.fit(X_train, y_train)
    # 预测测试集
    y_pred = knn.predict(X_test)
    # 计算并存储准确率
    accuracies.append(accuracy_score(y_test, y_pred))

# 找到提供最高准确率的K值
optimal_k = k_values[accuracies.index(max(accuracies))]
print(f"最佳的K值为：{optimal_k}，准确率为：{max(accuracies)}")

# 绘制K值与准确率的关系图
plt.figure(figsize=(10, 6))
plt.plot(k_values, accuracies, marker='o')
plt.title('K值与测试集准确率的关系')
plt.xlabel('K值')
plt.ylabel('测试集准确率')
plt.show()