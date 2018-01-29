'''
Created on Oct 8, 2016

@author: Adele
'''

import csv

from os.path import join
from sklearn.datasets.base import Bunch

import numpy as np

module_path = r"E:\Lessons_tutorials\Behavioural user profile articles\Datasets\Aras\House A\CSV_Summery"
    
def get_number_of_samples_and_features(number_of_days):
    """
    return number of samples and features for desired days
    """
    n_samples = 0
    n_features = 0
    days_samples = []
    
    #create an empty array
    for n in range(number_of_days + 1):
        days_samples.insert(n, 0) # because days start from 1
    
    for day_number in range(1, number_of_days + 1):
        with open(join(module_path,'DAY_'+ str(day_number) + '.csv')) as csv_file:
            data_file = csv.reader(csv_file)
            temp = next(data_file)
            new_samples = int(temp[0])
            new_features = int(temp[1])
            days_samples[day_number] = new_samples
            n_samples = n_samples + new_samples
            #if number of new features is greater than now
            if new_features > n_features:
                n_features = new_features
                
    print("n_samples: " + str(n_samples))
    #print("n_features: " + str(n_features))
    #print("days_samples: " + str(days_samples))
    
    return (n_samples , n_features , days_samples)
        
        
        
def load_aras(number_of_days,isPerson):

    """Load and return the Aras dataset (classification).

    Parameters
    ----------
    number_of_days : int
    isPerson : Boolean (True means person is the target , false means activity is the target)
    
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the classification labels,
        'target_names', the meaning of the labels, 'feature_names', the
        meaning of the features, and 'DESCR', the
        full description of the dataset.

    (data, target) : tuple if ``return_X_y`` is True

        .. versionadded:: 0.18
    """
    #by Adele
    #print ("module_path: " + module_path )
    #/by Adele
    
    n_samples , n_features , days_samples = get_number_of_samples_and_features(number_of_days)
    data = np.empty((n_samples, n_features))
    target = np.empty((n_samples,), dtype=np.int)
    temp_data = np.empty(n_features+1)# copy whole data to it, then select all col except 20
    
    prevoius_days = 0
   
    for d in range(1, number_of_days + 1):
        #calculate total previous days. it is used for index of arrays    
        if d!=1:
            prevoius_days += days_samples[d-1]
        #/   
        with open(join(module_path,'DAY_' + str(d) + '.csv')) as csv_file:
            data_file = csv.reader(csv_file)
            next(data_file)# to skip from first line of data (line of number of samples and features)
            
            #target_names = np.array(temp[2:])   # the name of labels 
                                            #i.e. 0= setosa, 1= versicolor and 2= virginica
            idx_IN_columns = []
            for i, ir in enumerate(data_file):
                #print("i: " + str(i))
                temp_data = np.asarray(ir[:22], dtype=np.int)
                if isPerson == True:
                    idx_IN_columns = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,21]#all of features except Person_ID(20)
                    target[prevoius_days + i] = np.asarray(ir[20], dtype=np.int)# Person ID is the class
                else:
                    idx_IN_columns = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
                    target[prevoius_days + i] = np.asarray(ir[21], dtype=np.int)
    
                extractedData = temp_data[idx_IN_columns]
                data[prevoius_days + i] = np.asarray(extractedData , dtype=np.int)
            
       
    
    #print(target)
    return Bunch(data=data, target=target)
        #            target_names=target_names)
                    #feature_names=['sepal length (cm)', 'sepal width (cm)',
                    #              'petal length (cm)', 'petal width (cm)'])

def convert_txt_to_csv():
    module_path = r"E:\Lessons_tutorials\Behavioural user profile articles\Datasets\Aras\House A"
    
    for i in range(1,31):#31
        day_number = 'DAY_'+ str(i)
        with open(join(module_path, 'Summery', day_number +'.txt') , "r") as txt_file:
                with open(join(module_path, 'CSV_Summery', day_number +'.csv'), 'w+', newline='') as csv_file:
                    in_txt = csv.reader(txt_file, delimiter = ',' )
                    #print(in_txt)
                    #print(type(in_txt))
                    out_csv = csv.writer(csv_file)
                    out_csv.writerows(in_txt)#.strip())#.rstrip('\n'))#ignore \n to avoid creating empty rows



    
    
if __name__ == "__main__":
    convert_txt_to_csv()   
    #get_number_of_samples_and_features(5)
    aras = load_aras(2) 
    #print(aras)
    #print(len(aras.data))    

        
