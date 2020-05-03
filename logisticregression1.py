# -*- coding: utf-8 -*-
"""ML_HW3_boranislamoglu.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hd43uBpwCyvIzTocUizmcSQCl1l9_6qi
"""

import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np
import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

"""# [25 pts] A Toy Example: Decision Boundary and Conditional Independence Assumption

### Gaussian Distributed Data fits better to Gaussian Naive Bayesian rather than Logistic Regression, unfortunately that is not the case most of the time.
Now, imagine we have two artificial dataset. Both are drawn from Gaussian distribution. One of the dataset is with standard deviation 1 and the other is 5. Each cluster is conditionally independent from each other.

make_blobs function samples data points from gaussian distribution.
"""

from sklearn.datasets import make_blobs
data1, label1 = make_blobs(n_samples=500, centers=2, n_features=2, cluster_std=1, random_state=1)
data2, label2 = make_blobs(n_samples=500, centers=2, n_features=2, cluster_std=5, random_state=1)

"""Let's split the datasets into train and test."""

X_train, X_test, y_train, y_test = train_test_split(data1, label1, test_size=0.2)
X_train2, X_test2, y_train2, y_test2 = train_test_split(data2, label2, test_size=0.2)

"""Plot the first dataset with standard deviation 1."""

plt.scatter(data1[:,0], data1[:,1], c=label1)
plt.title('Scatter plot data with standard deviation=1')
plt.xlabel('x')
plt.ylabel('y')
plt.show()

"""Plot the first dataset with standard deviation 4."""

plt.scatter(data2[:,0], data2[:,1], c=label2)
plt.title('Scatter plot data with standard deviation=5')
plt.xlabel('x')
plt.ylabel('y')
plt.show()

"""Train a Gaussian Naive Bayesian and Logistic Regression with the 1st dataset."""

from sklearn.naive_bayes import GaussianNB
GNB = GaussianNB()
GNB.fit(X_train, y_train)

from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(random_state=0)
clf.fit(X_train, y_train)

"""### Perfect Decision Boundary"""

# Predict
import seaborn as sn
print("Classification Report for Naive Bayesian:")
print(classification_report(GNB.predict(X_test),y_test))
cm = pd.DataFrame(confusion_matrix(y_test,GNB.predict(X_test)), range(2), range(2))
sn.set(font_scale=1.4)
sn.heatmap(cm, annot=True, annot_kws={"size": 16})

plt.ylabel('predictions')
plt.xlabel('actual values')
plt.title('Confusion Matrix')

plt.show()

# Predict
print("Classification Report for Logistic Regression:")
print(classification_report(clf.predict(X_test),y_test))
cm = pd.DataFrame(confusion_matrix(y_test,clf.predict(X_test)), range(2), range(2))
sn.set(font_scale=1.4)
sn.heatmap(cm, annot=True, annot_kws={"size": 16})

plt.ylabel('predictions')
plt.xlabel('actual values')
plt.title('Confusion Matrix')
plt.show()

"""### Both algorithm perfectly separate two data clusters for 1st dataset with standard deviation 1. The data points are linearly separable."""

from sklearn.naive_bayes import GaussianNB
GNB = GaussianNB()
GNB.fit(X_train2, y_train2)

from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(random_state=0)
clf.fit(X_train2, y_train2)

# Predict
print("Classification Report for Naive Bayesian:")
print(classification_report(GNB.predict(X_test2),y_test2))
cm = pd.DataFrame(confusion_matrix(y_test2,GNB.predict(X_test2)), range(2), range(2))
sn.set(font_scale=1.4)
sn.heatmap(cm, annot=True, annot_kws={"size": 16})

plt.ylabel('predictions')
plt.xlabel('actual values')
plt.title('Confusion Matrix')
plt.show()

# Predict
print("Classification Report for Logistic Regression:")
print(classification_report(clf.predict(X_test2),y_test2))
cm = pd.DataFrame(confusion_matrix(y_test2,clf.predict(X_test2)), range(2), range(2))
sn.set(font_scale=1.4)
sn.heatmap(cm, annot=True, annot_kws={"size": 16})

plt.ylabel('predictions')
plt.xlabel('actual values')
plt.title('Confusion Matrix')
plt.show()

"""### Use the scatter plot and draw the perfect decision boundary on two scatter plot. Discuss what is linear separability, decision boundary, which datapoints are harder to separate. Discuss the accuries and the why which model performs better.
 

### Please also read: [Equivalence of GNB and LR](https://appliedmachinelearning.blog/2019/09/30/equivalence-of-gaussian-naive-bayes-and-logistic-regression-an-explanation/)
"""



"""# [75pts] Logistic Regression and Naive Bayesian Comparison

### The dataset
We will use Kaggle dataset. This dataset contains around 200k news headlines from the year 2012 to 2018 obtained from HuffPost.

You can [download.](https://www.kaggle.com/rmisra/news-category-dataset)
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer

df=pd.read_json("/content/drive/My Drive/News_Category_Dataset_v2.json", lines = True)

"""## Select 4 categories: Politics, Wellness, Entertainment, Travel

use only 50K of data row
"""

df = df.sample(50000)

new_df = df[(df['category']== 'POLITICS') | (df['category']== 'WELLNESS') | (df['category']== 'ENTERTAINMENT') | (df['category']== 'TRAVEL')]

new_df['category'].value_counts()

"""Convert category names to digit labelling"""

y = (new_df['category'].to_numpy() == "WELLNESS")*1 + (new_df['category'].to_numpy() == "ENTERTAINMENT")*2 + (new_df['category'].to_numpy() == "TRAVEL")*3

"""Merge headlines with short descriptions"""

X = new_df['short_description'] + ' '+ new_df['headline']

"""### Create Tf-Idf model"""

from sklearn.feature_extraction.text import CountVectorizer

count_vect = CountVectorizer(lowercase=True, stop_words='english')
X_train_counts = count_vect.fit_transform(X)

from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer = TfidfTransformer()
X_train_tf = tfidf_transformer.fit_transform(X_train_counts)

"""Split train and test data"""

from sklearn.model_selection import train_test_split
train_data = X_train_tf[:4*(X_train_tf.shape[0]//5),:]
test_data = X_train_tf[4*(X_train_tf.shape[0]//5):,:]

train_label = y[:4*(X_train_tf.shape[0]//5)]
test_label = y[4*(X_train_tf.shape[0]//5):]

"""### Gaussian Naive Bayesian"""

from sklearn.naive_bayes import GaussianNB
NewGNB = GaussianNB()
NewGNB.fit(train_data.toarray(), train_label)

# Predict
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
print("Classification Report for Naive Bayesian:")
print(classification_report(NewGNB.predict(test_data.toarray()), test_label))
print(accuracy_score(NewGNB.predict(test_data.toarray()),test_label))
cm = pd.DataFrame(confusion_matrix(test_label,NewGNB.predict(test_data.toarray())), range(4), range(4))
sn.set(font_scale=1.4)
sn.heatmap(cm, annot=True, annot_kws={"size": 16})

plt.ylabel('predictions')
plt.xlabel('actual values')
plt.title('Confusion Matrix')
plt.show()

"""### 6) Logistic Regression"""

clf = LogisticRegression(random_state=0)
clf.fit(train_data, train_label)

# Predict
>>> from sklearn.metrics import accuracy_score
print("Classification Report for Logistic Regression:")
print(classification_report(clf.predict(test_data),test_label))
print(accuracy_score(clf.predict(test_data),test_label))
cm = pd.DataFrame(confusion_matrix(test_label,clf.predict(test_data)), range(4), range(4))
sn.set(font_scale=1.4)
sn.heatmap(cm, annot=True, annot_kws={"size": 16})

plt.ylabel('predictions')
plt.xlabel('actual values')
plt.title('Confusion Matrix')
plt.show()

"""### Observe Logistic Regression is much slower but more accurate. Discuss.

We observed that Logistic Regression worked much slower than Gaussian Naive Bayesian.

However, we have obtained much better accuracy, precision and recall scores with Logistic Regression than Gaussian Naive Bayesian.

We have obtained the best results with the Logistic Regression, giving an accuracy of 0.8924617817606747

We have obtained the second best results with the Gaussian Naive Bayesian, giving an accuracy of 0.7090142329994729
"""