'''
Created on Nov 20, 2016

@author: Adele
'''

import numpy as np
import Aras
import aras_sequentional
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC , LinearSVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from pip.commands.search import print_results


def test_diffrent_classifiers_on_aras(data_source):
    '''
    Parameters:
    if data_source = 1, it means load data from aras
    if data_source = 2, it means load data from sequential aras (first repeat of sensor is considered)
    if data_source = 3, it means load data from sequential aras (last repeat of sensor is considered)
    if data_source = 4, it means load data from sequential aras (just occurness of sensor events is considered)
    if data_source = 5, it means load data from sequential aras (number of occurness of sensor events is considered)


    '''
    names = ["1-Nearest Neighbors", 
             "2-Nearest Neighbors",
             "3-Nearest Neighbors",
             "4-Nearest Neighbors",
             "5-Nearest Neighbors",
             #"Linear SVM", 
             #"RBF SVM", 
             #"Poly SVM degree = 3",
             #"Poly SVM degree = 4",
             #"Poly SVM degree = 5",
             #"LinearSVC",
             #"Gaussian Process",
             "Decision Tree",
             "Random Forest", 
             "Neural Net", 
             "AdaBoost",
             "Naive Bayes", 
             "QDA"
             ]
    
    classifiers = [
        KNeighborsClassifier(1),
        KNeighborsClassifier(2),
        KNeighborsClassifier(3),
        KNeighborsClassifier(4),
        KNeighborsClassifier(5),
        #SVC(kernel="linear", C=1.0),
        #SVC(kernel='rbf', gamma=0.7, C=1.0),
        #SVC(kernel='poly', degree=3, C=1.0),
        #SVC(kernel='poly', degree=4, C=1.0),
        #SVC(kernel='poly', degree=5, C=1.0),
        #LinearSVC(C=1.0),
        #GaussianProcessClassifier(1.0 * RBF(1.0), warm_start=True),
        DecisionTreeClassifier(max_depth=5),
        RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
        MLPClassifier(alpha=1),
        AdaBoostClassifier(),
        GaussianNB(),
        QuadraticDiscriminantAnalysis()
        ]
    
    if data_source == 1:
        aras = Aras.load_aras(3 , isPerson=True)
    elif data_source == 2:
        aras = aras_sequentional.load_sequential_aras_first(isPerson=True)
    elif data_source == 3:
        aras = aras_sequentional.load_sequential_aras_last(isPerson=True)
    elif data_source == 4:
        aras = aras_sequentional.load_sequential_aras_occur(isPerson=True)
    elif data_source == 5:
        aras = aras_sequentional.load_sequential_aras_frequency_occur(isPerson=True)

        
    data = aras.data
    target = aras.target
    #print(len(target))
    #for i in range(len(target)):
    #   print(target[i])          
      
    # iterate over classifiers
    for name, clf in zip(names, classifiers):
        #for i in range (3 , 4):# i indicates number of days start from Day 1
        #print("\n\n***************************************************")
        #print("number of days: " + str(i))
        #print("***************************************************")
        scores = cross_val_score(clf, data, target, cv=10 , scoring='f1_macro') ####10-fold cross validation 
        print_results(name , 3 , scores.mean())
        #print("scores: " + str(scores))
        #print("mean score: " + str(scores.mean()))
        

def print_results(classifier_name, number_of_days, mean_score):
        print("Classifier: " + str(classifier_name))
        #print("number of days: " + str(number_of_days)
        print("10-fold Cross validation mean score: " + str(mean_score))
        
if __name__ == "__main__":
    test_diffrent_classifiers_on_aras(data_source=4)
    #cl = MLPClassifier(alpha=1)
#LinearSVC(C=1.0)#SVC(kernel="linear", C=1.0)
    #cl.fit()