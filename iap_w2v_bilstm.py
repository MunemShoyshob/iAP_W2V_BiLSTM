# -*- coding: utf-8 -*-
"""iAP_W2V_BiLSTM

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FApHLkWrvn4-B6W8LMdvN6hYXMBmvhuM
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix, cohen_kappa_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import matthews_corrcoef
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense, Flatten, Conv1D, MaxPooling1D, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.initializers import HeNormal
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization, Bidirectional
from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.layers import SimpleRNN, Dropout, Dense
from sklearn.model_selection import StratifiedKFold

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix, cohen_kappa_score
from sklearn.metrics import matthews_corrcoef
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict

from keras.models import Sequential
from keras.layers import Dense, Conv1D, MaxPool1D, Flatten,LSTM

train = pd.read_csv('/content/word2vec_train_32.csv')
test = pd.read_csv('/content/word2vec_test_32.csv')

xtrain = train.drop(['Target'], axis = 1)
ytrain = train['Target']

xtest = test.drop(['Target'], axis = 1)
ytest = test['Target']

X = xtrain
Y = ytrain

X = X.to_numpy()
X = X.reshape(X.shape[0], X.shape[1], 1)

kf = KFold(n_splits=5, shuffle=True)
for train_index, val_index in kf.split(X):
    X_train, X_val = X[train_index], X[val_index]
    y_train, y_val = Y[train_index], Y[val_index]

# Build the Bi-LSTM model
model = Sequential()

# Add a Bi-directional LSTM layer
model.add(Bidirectional(LSTM(128, activation='tanh', return_sequences=True), input_shape=(X_train.shape[1], 1)))

# Add another Bi-directional LSTM layer
model.add(Bidirectional(LSTM(64, activation='tanh', return_sequences=False)))

# Add fully connected layers
model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation='sigmoid'))  # Binary classification output

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.0001), loss='binary_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, epochs = 40, batch_size= 64)

pred = model.predict(X_val)
y_pred_classes = np.round(pred).astype(int)

accuracy_score(y_val, y_pred_classes), recall_score(y_val, y_pred_classes), precision_score(y_val, y_pred_classes), f1_score(y_val, y_pred_classes), cohen_kappa_score(y_val, y_pred_classes), matthews_corrcoef(y_val, y_pred_classes)

cm1 = confusion_matrix(y_val, y_pred_classes)
specificity = cm1[0,0]/(cm1[0,0]+cm1[0,1])
specificity

"""Test"""

sample_size = xtrain.shape[0] # number of samples in train set
time_steps  = xtrain.shape[1] # number of features in train set
input_dimension = 1               # each feature is represented by 1 number

train_data_reshaped = xtrain.values.reshape(sample_size,time_steps,input_dimension)
n_timesteps = train_data_reshaped.shape[1]
n_features  = train_data_reshaped.shape[2]

# Build the Bi-LSTM model
model1 = Sequential()

# Add a Bi-directional LSTM layer
model1.add(Bidirectional(LSTM(128, activation='tanh', return_sequences=True), input_shape=(n_timesteps,n_features)))

# Add another Bi-directional LSTM layer
model1.add(Bidirectional(LSTM(64, activation='tanh', return_sequences=False)))

# Add fully connected layers
model1.add(Dense(64, activation='relu'))
model1.add(Dense(1, activation='sigmoid'))  # Binary classification output

# Compile the model
model1.compile(optimizer=Adam(learning_rate=0.0001), loss='binary_crossentropy', metrics=['accuracy'])

history = model1.fit(xtrain, ytrain, epochs = 40, batch_size= 64)

pred1 = model1.predict(xtest)
pred1 = (pred1 > 0.5)

accuracy_score(ytest, pred1), recall_score(ytest, pred1), precision_score(ytest, pred1), f1_score(ytest, pred1), cohen_kappa_score(ytest, pred1), matthews_corrcoef(ytest, pred1)

cm1 = confusion_matrix(ytest, pred1)
specificity = cm1[0,0]/(cm1[0,0]+cm1[0,1])
specificity