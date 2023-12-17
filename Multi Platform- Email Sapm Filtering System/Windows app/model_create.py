import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import pickle

data = pd.read_csv("emails.csv")
print(data.head())  
print(data.shape)
print(data['text'][0])
print(data['spam'].value_counts())
# sns.countplot(data['spam'])
# plt.show()
print("Duplicate Data :")
print(data.duplicated().sum())
#Removing the duplicates
data.drop_duplicates(inplace=True)
print("Duplicates after dropping:")
print(data.duplicated().sum())
print(data.isnull().sum())
#Shape of Data after removing the duplicate values
print(data.shape)
print(data['spam'].value_counts())

#Seperating X and Y values

X = data['text'].values
y = data['spam'].values

#Splitting the training and testing data from the main dataset
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2 , random_state= 0)
#NOTE : 20% of the actual data is take for training the ML model.
print(X_train.shape)
print(X_test.shape)
print(y_test.shape)

#Preprossing 

cv = CountVectorizer()

#Training the ML model 
nb = MultinomialNB()
pipe = make_pipeline(cv, nb)
pipe.fit(X_train,y_train)
y_pred = pipe.predict(X_test)   
accuracy_score(y_pred, y_test)
confusion = confusion_matrix(y_test, y_pred)

# Create a heatmap
sns.heatmap(confusion, annot=True, fmt='d', cmap='Blues')

# Customize the plot
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')

# Show the plot
plt.show()

#Generating a classification Report

report = classification_report(y_test, y_pred)

# Print the report
print("Classification Report:")
print(report)

email = ['Hey i am Elon Musk. Get a brand new car from Tesla']
print(pipe.predict(email))
# pickle.dump(pipe, open("Spam_detection.pkl",'wb'))