# -*- coding: utf-8 -*-
"""walidacja.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1h8lGu7m6Pb3086u7BO7BI68tJ891JZHB
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import plotly.express as px
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from pandas_profiling import describe
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report, plot_confusion_matrix, ConfusionMatrixDisplay
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, ShuffleSplit, cross_val_score

#wykonanie walidacji prostej i krzyżowej na zbiorze 150 kosaćców należących do trzech gatunków

df = px.data.iris()# import danych
df.head()
print(df.describe()) # statystyka opisowa
print(df.info()) # opis danych

# Walidacja prosta z podziałem na zbiór treningowy i walidacyjny
X = df.values[:, 0:4]
y = df.values[:, 5]
le = LabelEncoder() # transformacja macierzy y
y = le.fit_transform(y) 
# Podział na zbiór treningowy i testowy (dotyczy X i y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.31, random_state=0) 
da = LinearDiscriminantAnalysis() # LDA
da.fit(X_train, y_train) # trenowanie klasyfikatora
y_pred = da.predict(X_test) # predykcja klas - zbiór testowy
print('\nAccuray (test):', accuracy_score(y_test, y_pred))
y_train_pred = da.predict(X_train) # predykcja klas - zbiór terningowy
print('Accuray (train):', accuracy_score(y_train, y_train_pred))
labels = np.unique(y)
print(classification_report(y_test, y_pred, labels=labels))
# macierz pomyłek dla zbioru testowego (tekst)
print('\nConfusion matrix')
labels = np.unique(y)
cm = confusion_matrix(y_test, y_pred)
print(pd.DataFrame(cm, index=labels, columns=labels))
# macierz pomyłek dla zbioru testowego (grafika)
print('\nConfusion matrix - plot')
pcm = plot_confusion_matrix(da, X_test, y_test, labels=labels)
ConfusionMatrixDisplay(pcm, display_labels=labels)
plt.show() 

# Walidacja krzyżowa z podziałem zbioru na 6 części 
cv = ShuffleSplit(n_splits=6, test_size=0.23, random_state=0)
scores = cross_val_score(da, X, y, cv=cv)
print('\nAccuracy: ',scores) 
print('Accuracy (mean): ',scores.mean())
print('Accuracy (std): ',scores.std())