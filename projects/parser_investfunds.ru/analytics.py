import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

FILENAME_TO_ANALYSE = "investfunds.ru-PIFs" + ".csv"
FILE_COV = "Covariation matrix"
COVAR_THRESHOLD = 0.8


input_data = pd.read_csv(FILENAME_TO_ANALYSE, sep=';',encoding="cp1251").to_dict(orient='dict')
num_data = {key: input_data[key] for key in input_data
            if type(input_data[key][1]) is not str}  # индекс выясняется во время отладки (чтобы лишнего не зацепить)

# удаляем плохо коррелирующие с всеми столбцы
del num_data['Unnamed: 0']
df = pd.DataFrame(data=num_data)
corr = df.corr()
labels = df.columns
corr_ = corr.values.tolist()
for i in range(0, len(corr_)-1):
    for j in range(i+1, len(corr_)):
        corr_[i][j] = round(corr_[i][j], 3)
        if 0.9999999 > corr_[i][j] > COVAR_THRESHOLD or corr_[i][j] < -COVAR_THRESHOLD:
            print(labels[i], labels[j], corr_[i][j])

# другой вариант, более красивый, но более затратный и менее читаемый
for key in corr:
    i = 0
    for item in corr[key]:
        corr[key] = round(corr[key], 3)
        if 0.9999999 > item > COVAR_THRESHOLD or item < -COVAR_THRESHOLD:
            # print(key, labels[j], item)
            i += 1
    if i == 0:
       pass
       corr.drop(columns=key, inplace=True)
       corr.drop(labels=key, axis=0, inplace=True)

# visualization
sns.set(rc={"figure.figsize": (35, 14)})
g = sns.heatmap(corr, annot=True, fmt='g')
g.get_figure().savefig("heatmap.png")

