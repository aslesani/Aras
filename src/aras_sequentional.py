'''
Created on Nov 21, 2016

@author: Adele

==================================================
prepare and load aras as a sequence of sensor events (different implementation are provided)
==================================================

'''

from numpy import dtype
import numpy as np
from sklearn.datasets.base import Bunch
#from _ast import Str
#from asyncore import read
#import re
import csv
from os.path import join


print(__doc__)

def create_aras_sequentional_based_on_days_first():
    '''
    description: create sequential sensor events for each day separately
    the format of creating sequences is (sensorID_start, sensorID_stop)^ number of sensors , person, activity
    limitation:
     -it does not consider about consecutive days.
      sometimes an activity starts in one day but ends in another day.
     -it does not consider about maximum activity lengths
     -it does not consider about parallel activities. 
      if an activity occur after another, the application suppose the first activity is finished.
     -if a sensor event be repeated, just first one is logged
    '''
    #lines = f.readlin()
    module_path = r"E:\Lessons_tutorials\Behavioural user profile articles\Datasets\Aras\House A\CSV_Summery"
    with open("E:\Lessons_tutorials\Behavioural user profile articles\Datasets\Aras\House A\CSV_Summery\Sequential\Day\Whole_data.csv",'w+', newline='') as whole_data_file:
        for i in range(1,31):#31
            day_number = 'DAY_'+ str(i) + '.csv'
            with open(join(module_path, day_number) , "r") as in_file:
                with open(join(module_path, 'Sequential', 'Day', day_number), 'w+', newline='') as out_file:
                    in_txt = csv.reader(in_file, delimiter = ',' )
                    #out_csv = csv.writer(out_file)
                    
                    last_person_events = [
                        0,
                        ['-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1'],
                        ['-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1']
                        ]
    
                    
                    #create an empty list to store last activity of each person. 
                    #The index of list is the ID of person.e.g.last_person_activity[1] means person1's last activity
                    #the zero index is filled, but is not used
                    last_person_activity = ['-1','-1','-1']
                    
                    #create an empty list to store last sequence of each person that is not finished to be written in file. 
                    #The index of list is the ID of person.
                    last_person_sequence = [
                        0,
                        ['-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1', '-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1'],
                        ['-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1', '-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1']
                        ]
                    
                    #create an empty list to store last sequence number used for each person. i.e. It stores  
                    #The index of list is the ID of person.
                    last_person_used_sequence_index = [0, 0, 0]
                    #to skip from first line of file
                    next(in_txt)
                    #first_line_readed = False
                    for current_events in in_txt:
                        #print(current_events)
                        current_person = int(current_events[-2])
                        current_activity = current_events[-1]
                                            
                        #print(last_person_activity[current_person])
                        #print(current_activity)
                                                
                        if last_person_activity[current_person] == current_activity:
                            #print("yes")
                            last_person_used_sequence_index[current_person] += 1
                                                        
                        else:
                            last_person_used_sequence_index[current_person] = 1
                            #if current_person == 1:
                            #    print("no")
                            #   print("last_person_used_sequence_index[current_person]: " + str(last_person_used_sequence_index[current_person]))
    
                            if last_person_activity[current_person] != '-1':
                                #قبلی رو هم توی فایل بنویس
                                common_sensor_events = " ".join(x for x in last_person_sequence[current_person])
                                sequence_row = common_sensor_events.replace(' ' , ',') + "," + str(current_person) + "," + last_person_activity[current_person] + "\n"
                                #print(sequence_row)
                                out_file.write(sequence_row)
                                whole_data_file.write(sequence_row)
                        
                        
                        #if current_person == 1:    
                        modified_index = -1
                        for i in range(0,20):
                            if current_events[i] != last_person_events[current_person][i]:
                                if current_events[i] == '1':
                                    modified_index = i*2
                                else:
                                    modified_index = i*2 + 1
                                break
                        
                        if last_person_activity[current_person] != current_activity:
                            #همه توالی رو -1 کن
                            for i in range (0,40):
                                last_person_sequence[current_person][i] = '-1'      
    
                        #just the first time of changing sensor_start or stop is logged
                        if last_person_sequence[current_person][modified_index] == '-1':
                            last_person_sequence[current_person][modified_index] = str(last_person_used_sequence_index[current_person])     
                        else:
                            last_person_used_sequence_index[current_person] -= 1
                            
                        
                        last_person_events[current_person] = current_events
                        last_person_activity[current_person] = current_activity


#def create_aras_sequentional_based_on_people():
    #pass


def load_sequential_aras_first(isPerson):

    """Load and return the Aras Sequential dataset (classification).

    Parameters
    ----------
    isPerson : if is true, the Person column is the target,
               if is false, the activity col is the target 

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
    
    with open("E:\Lessons_tutorials\Behavioural user profile articles\Datasets\Aras\House A\CSV_Summery\Sequential\Day\Whole_data.csv") as csv_file:
        
        data_file = csv.reader(csv_file)
        #target_names = np.array(temp[2:])   # the name of labels   
        n_samples = 2068#sum(1 for row in data_file) 
        n_features = 41
        data = np.empty((n_samples, n_features))
        target = np.empty((n_samples,), dtype=np.int)
        temp_data = np.empty(n_features+1)# copy whole data to it, then select all col except 20
           
        idx_IN_columns = []                           
        for i, ir in enumerate(data_file):
            #print(i)
            temp_data = np.asarray(ir[:42], dtype=np.int)
            #print(temp_data)
            if isPerson == True:
                n_features = 40
                data = np.empty((n_samples, n_features))
                
                # in version 2 the activity col is removed too because it is not important, sensor data are required.
                idx_IN_columns = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]#all of features except feature 40 (Person_ID
                target[i] = np.asarray(ir[40], dtype=np.int)# Person ID is the class
            else:
                idx_IN_columns = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]#all of features except feature 41 (Activity_ID
                target[i] = np.asarray(ir[41], dtype=np.int)# Activity ID is the class
                
    
            extractedData = temp_data[idx_IN_columns]
            #print(extractedData)
            data[i] = np.asarray(extractedData , dtype=np.int)
            #print(target[i])
        
   
        #print(data)
        #print(target)
        return Bunch(data=data, target=target)
    #            target_names=target_names)
                #feature_names=['sepal length (cm)', 'sepal width (cm)',
                #              'petal length (cm)', 'petal width (cm)'])


def create_aras_sequentional_based_on_days_last():
    '''
    description: create sequential sensor events for each day separately
    the format of creating sequences is (sensorID_start, sensorID_stop)^ number of sensors , person, activity
    limitation:
     -it does not consider about consecutive days.
      sometimes an activity starts in one day but ends in another day.
     -it does not consider about maximum activity lengths
     -it does not consider about parallel activities. 
      if an activity occur after another, the application suppose the first activity is finished.
     -if a sensor event be repeated, just last one is logged
    '''
    #lines = f.readlin()
    module_path = r"E:\Lessons_tutorials\Behavioural user profile articles\Datasets\Aras\House A\CSV_Summery"
    with open("E:\Lessons_tutorials\Behavioural user profile articles\Datasets\Aras\House A\CSV_Summery\Sequential\Day\last\Whole_data.csv",'w+', newline='') as whole_data_file:
        for i in range(1,31):#31
            day_number = 'DAY_'+ str(i) + '.csv'
            with open(join(module_path, day_number) , "r") as in_file:
                with open(join(module_path, 'Sequential', 'Day', 'last', day_number), 'w+', newline='') as out_file:
                    in_txt = csv.reader(in_file, delimiter = ',' )
                    #out_csv = csv.writer(out_file)
                    
                    last_person_events = [
                        0,
                        ['-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1'],
                        ['-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1']
                        ]
    
                    
                    #create an empty list to store last activity of each person. 
                    #The index of list is the ID of person.e.g.last_person_activity[1] means person1's last activity
                    #the zero index is filled, but is not used
                    last_person_activity = ['-1','-1','-1']
                    
                    #create an empty list to store last sequence of each person that is not finished to be written in file. 
                    #The index of list is the ID of person.
                    last_person_sequence = [
                        0,
                        ['-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1', '-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1'],
                        ['-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1', '-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1']
                        ]
                    
                    #create an empty list to store last sequence number used for each person. i.e. It stores  
                    #The index of list is the ID of person.
                    last_person_used_sequence_index = [0, 0, 0]
                    #to skip from first line of file
                    next(in_txt)
                    #first_line_readed = False
                    for current_events in in_txt:
                        #print(current_events)
                        current_person = int(current_events[-2])
                        current_activity = current_events[-1]
                                            
                        #print(last_person_activity[current_person])
                        #print(current_activity)
                                                
                        if last_person_activity[current_person] == current_activity:
                            #print("yes")
                            last_person_used_sequence_index[current_person] += 1
                                                        
                        else:
                            last_person_used_sequence_index[current_person] = 1
                            #if current_person == 1:
                            #    print("no")
                            #   print("last_person_used_sequence_index[current_person]: " + str(last_person_used_sequence_index[current_person]))
    
                            if last_person_activity[current_person] != '-1':
                                #قبلی رو هم توی فایل بنویس
                                common_sensor_events = " ".join(x for x in last_person_sequence[current_person])
                                sequence_row = common_sensor_events.replace(' ' , ',') + "," + str(current_person) + "," + last_person_activity[current_person] + "\n"
                                #print(sequence_row)
                                out_file.write(sequence_row)
                                whole_data_file.write(sequence_row)
                        
                        
                        #if current_person == 1:    
                        modified_index = -1
                        for i in range(0,20):
                            if current_events[i] != last_person_events[current_person][i]:
                                if current_events[i] == '1':
                                    modified_index = i*2
                                else:
                                    modified_index = i*2 + 1
                                break
                        
                        if last_person_activity[current_person] != current_activity:
                            #همه توالی رو -1 کن
                            for i in range (0,40):
                                last_person_sequence[current_person][i] = '-1'      
    
                        #just the first time of changing sensor_start or stop is logged
                        #if last_person_sequence[current_person][modified_index] == '-1':
                        last_person_sequence[current_person][modified_index] = str(last_person_used_sequence_index[current_person])     
                        #else:
                        #    last_person_used_sequence_index[current_person] -= 1
                            
                        
                        last_person_events[current_person] = current_events
                        last_person_activity[current_person] = current_activity

def load_sequential_aras_last(isPerson):

    """Load and return the Aras Sequential dataset (classification).

    Parameters
    ----------
    isPerson : if is true, the Person column is the target,
               if is false, the activity col is the target 


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
    
    with open("E:\Lessons_tutorials\Behavioural user profile articles\Datasets\Aras\House A\CSV_Summery\Sequential\Day\last\Whole_data.csv") as csv_file:
        
        data_file = csv.reader(csv_file)
        #target_names = np.array(temp[2:])   # the name of labels   
        n_samples = 2068#sum(1 for row in data_file) 
        n_features = 41
        data = np.empty((n_samples, n_features))
        target = np.empty((n_samples,), dtype=np.int)
        temp_data = np.empty(n_features+1)# copy whole data to it, then select all col except 20
                                      
        idx_IN_columns = []                           
        for i, ir in enumerate(data_file):
            #print(i)
            temp_data = np.asarray(ir[:42], dtype=np.int)
            #print(temp_data)
            if isPerson == True:
                n_features = 40
                data = np.empty((n_samples, n_features))
    
                # in version 2 the activity col is removed too because it is not important, sensor data are required.
                idx_IN_columns = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]#all of features except feature 40 (Person_ID
                target[i] = np.asarray(ir[40], dtype=np.int)# Person ID is the class
            else:
                idx_IN_columns = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]#all of features except feature 41 (Activity_ID
                target[i] = np.asarray(ir[41], dtype=np.int)# Activity ID is the class
                
    
            extractedData = temp_data[idx_IN_columns]
            #print(extractedData)
            data[i] = np.asarray(extractedData , dtype=np.int)
            #print(target[i])
   
   
        #print(data)
        #print(target)
        return Bunch(data=data, target=target)
    #            target_names=target_names)
                #feature_names=['sepal length (cm)', 'sepal width (cm)',
                #              'petal length (cm)', 'petal width (cm)'])

def create_aras_sequentional_based_on_days_occurness():
    '''
    description: create sequential sensor events for each day separately
    the format of creating sequences is (sensorID_start, sensorID_stop)^ number of sensors , person, activity
    limitation:
     -it does not consider about consecutive days.
      sometimes an activity starts in one day but ends in another day.
     -it does not consider about maximum activity lengths
     -it does not consider about parallel activities. 
      if an activity occur after another, the application suppose the first activity is finished.
     -just presence or absence of a sensor event (sensor_start and sensor_stop) is logged
    '''
    #lines = f.readlin()
    module_path = r"E:\Lessons_tutorials\Behavioural user profile articles\Datasets\Aras\House A\CSV_Summery"
    with open("E:\Lessons_tutorials\Behavioural user profile articles\Datasets\Aras\House A\CSV_Summery\Sequential\Day\occur\Whole_data.csv",'w+', newline='') as whole_data_file:
        for i in range(1,31):#31
            day_number = 'DAY_'+ str(i) + '.csv'
            with open(join(module_path, day_number) , "r") as in_file:
                with open(join(module_path, 'Sequential', 'Day', 'occur', day_number), 'w+', newline='') as out_file:
                    in_txt = csv.reader(in_file, delimiter = ',' )
                    #out_csv = csv.writer(out_file)
                    
                    last_person_events = [
                        0,
                        ['-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1'],
                        ['-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1']
                        ]
    
                    
                    #create an empty list to store last activity of each person. 
                    #The index of list is the ID of person.e.g.last_person_activity[1] means person1's last activity
                    #the zero index is filled, but is not used
                    last_person_activity = ['-1','-1','-1']
                    
                    #create an empty list to store last sequence of each person that is not finished to be written in file. 
                    #The index of list is the ID of person.
                    last_person_sequence = [
                        0,
                        ['-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1', '-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1'],
                        ['-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1', '-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1']
                        ]
                    
                    
                    #to skip from first line of file
                    next(in_txt)
                    #first_line_readed = False
                    for current_events in in_txt:
                        #print(current_events)
                        current_person = int(current_events[-2])
                        current_activity = current_events[-1]
                                            
                        #print(last_person_activity[current_person])
                        #print(current_activity)
                                                
                        if last_person_activity[current_person] != current_activity:
    
                            if last_person_activity[current_person] != '-1':
                                #قبلی رو هم توی فایل بنویس
                                common_sensor_events = " ".join(x for x in last_person_sequence[current_person])
                                sequence_row = common_sensor_events.replace(' ' , ',') + "," + str(current_person) + "," + last_person_activity[current_person] + "\n"
                                #print(sequence_row)
                                out_file.write(sequence_row)
                                whole_data_file.write(sequence_row)
                        
                        
                        #if current_person == 1:    
                        modified_index = -1
                        for i in range(0,20):
                            if current_events[i] != last_person_events[current_person][i]:
                                if current_events[i] == '1':
                                    modified_index = i*2
                                else:
                                    modified_index = i*2 + 1
                                break
                        
                        if last_person_activity[current_person] != current_activity:
                            #همه توالی رو -1 کن
                            for i in range (0,40):
                                last_person_sequence[current_person][i] = '-1'      
    
                        last_person_sequence[current_person][modified_index] = '1'     
                            
                        last_person_events[current_person] = current_events
                        last_person_activity[current_person] = current_activity


def load_sequential_aras_occur(isPerson):

    """Load and return the Aras Sequential dataset (classification).

    Parameters
    ----------
    isPerson : if is true, the Person column is the target,
               if is false, the activity col is the target 


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
    
    with open("E:\Lessons_tutorials\Behavioural user profile articles\Datasets\Aras\House A\CSV_Summery\Sequential\Day\occur\Whole_data.csv") as csv_file:
        
        data_file = csv.reader(csv_file)
        #target_names = np.array(temp[2:])   # the name of labels   
        n_samples = 2068#sum(1 for row in data_file) 
        n_features = 41
        data = np.empty((n_samples, n_features))
        target = np.empty((n_samples,), dtype=np.int)
        temp_data = np.empty(n_features+1)# copy whole data to it, then select all col except 20
                                      
        idx_IN_columns = []                           
        for i, ir in enumerate(data_file):
            #print(i)
            temp_data = np.asarray(ir[:42], dtype=np.int)
            #print(temp_data)
            if isPerson == True:
                n_features = 40
                data = np.empty((n_samples, n_features))
    
                # in version 2 the activity col is removed too because it is not important, sensor data are required.
                idx_IN_columns = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]#all of features except feature 40 (Person_ID
                target[i] = np.asarray(ir[40], dtype=np.int)# Person ID is the class
            else:
                idx_IN_columns = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]#all of features except feature 41 (Activity_ID
                target[i] = np.asarray(ir[41], dtype=np.int)# Activity ID is the class
                
    
            extractedData = temp_data[idx_IN_columns]
            #print(extractedData)
            data[i] = np.asarray(extractedData , dtype=np.int)
            print(target[i])
       
        return Bunch(data=data, target=target)
    #            target_names=target_names)
                #feature_names=['sepal length (cm)', 'sepal width (cm)',
                #              'petal length (cm)', 'petal width (cm)'])


def create_aras_sequentional_based_on_days_frequency_occurness():
    '''
    description: create sequential sensor events for each day separately
    the format of creating sequences is (sensorID_start, sensorID_stop)^ number of sensors , person, activity
    limitation:
     -it does not consider about consecutive days.
      sometimes an activity starts in one day but ends in another day.
     -it does not consider about maximum activity lengths
     -it does not consider about parallel activities. 
      if an activity occur after another, the application suppose the first activity is finished.
     -number of presence or absence of a sensor event (sensor_start and sensor_stop) is logged
    '''
    #lines = f.readlin()
    module_path = r"E:\Lessons_tutorials\Behavioural user profile articles\Datasets\Aras\House A\CSV_Summery"
    with open(r"E:\Lessons_tutorials\Behavioural user profile articles\Datasets\Aras\House A\CSV_Summery\Sequential\Day\frequency_occur\Whole_data.csv",'w+', newline='') as whole_data_file:
        for i in range(1,31):#31
            day_number = 'DAY_'+ str(i) + '.csv'
            with open(join(module_path, day_number) , "r") as in_file:
                with open(join(module_path, 'Sequential', 'Day', 'frequency_occur', day_number), 'w+', newline='') as out_file:
                    in_txt = csv.reader(in_file, delimiter = ',' )
                    #out_csv = csv.writer(out_file)
                    
                    last_person_events = [
                        0,
                        ['-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1'],
                        ['-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1']
                        ]
    
                    
                    #create an empty list to store last activity of each person. 
                    #The index of list is the ID of person.e.g.last_person_activity[1] means person1's last activity
                    #the zero index is filled, but is not used
                    last_person_activity = ['-1','-1','-1']
                    
                    #create an empty list to store last sequence of each person that is not finished to be written in file. 
                    #The index of list is the ID of person.
                    last_person_sequence = [
                        0,
                        ['-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1', '-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1'],
                        ['-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1', '-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1']
                        ]
                    
                    
                    #to skip from first line of file
                    next(in_txt)
                    #first_line_readed = False
                    for current_events in in_txt:
                        #print(current_events)
                        current_person = int(current_events[-2])
                        current_activity = current_events[-1]
                                            
                        if last_person_activity[current_person] != current_activity:
    
                            if last_person_activity[current_person] != '-1':
                                #قبلی رو هم توی فایل بنویس
                                common_sensor_events = " ".join(x for x in last_person_sequence[current_person])
                                sequence_row = common_sensor_events.replace(' ' , ',') + "," + str(current_person) + "," + last_person_activity[current_person] + "\n"
                                #print(sequence_row)
                                out_file.write(sequence_row)
                                whole_data_file.write(sequence_row)
                        
                        
                        #if current_person == 1:    
                        modified_index = -1
                        for i in range(0,20):
                            if current_events[i] != last_person_events[current_person][i]:
                                if current_events[i] == '1':
                                    modified_index = i*2
                                else:
                                    modified_index = i*2 + 1
                                break
                        
                        if last_person_activity[current_person] != current_activity:
                            #همه توالی رو -1 کن
                            for i in range (0,40):
                                last_person_sequence[current_person][i] = '-1'      
    
                        if last_person_sequence[current_person][modified_index] == '-1':
                            last_person_sequence[current_person][modified_index] = '1'
                        else:
                            last_person_sequence[current_person][modified_index] = str( int(last_person_sequence[current_person][modified_index]) + 1)    
                            
                        last_person_events[current_person] = current_events
                        last_person_activity[current_person] = current_activity


def load_sequential_aras_frequency_occur(isPerson):

    """Load and return the Aras Sequential dataset (classification).

    Parameters
    ----------
    isPerson : if is true, the Person column is the target,
               if is false, the activity col is the target 



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
    
    with open(r"E:\Lessons_tutorials\Behavioural user profile articles\Datasets\Aras\House A\CSV_Summery\Sequential\Day\frequency_occur\Whole_data.csv") as csv_file:
        
        data_file = csv.reader(csv_file)
        #target_names = np.array(temp[2:])   # the name of labels   
        n_samples = 2068#sum(1 for row in data_file) 
        n_features = 41
        data = np.empty((n_samples, n_features))
        target = np.empty((n_samples,), dtype=np.int)
        temp_data = np.empty(n_features+1)# copy whole data to it, then select all col except 20
                                      
        idx_IN_columns = []                           
        for i, ir in enumerate(data_file):
            #print(i)
            temp_data = np.asarray(ir[:42], dtype=np.int)
            #print(temp_data)
            if isPerson == True:
                n_features = 40
                data = np.empty((n_samples, n_features))
        
                # in version 2 the activity col is removed too because it is not important, sensor data are required.
                idx_IN_columns = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]#all of features except feature 40 (Person_ID
                target[i] = np.asarray(ir[40], dtype=np.int)# Person ID is the class
            else:
                idx_IN_columns = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]#all of features except feature 41 (Activity_ID
                target[i] = np.asarray(ir[41], dtype=np.int)# Activity ID is the class
                
    
            extractedData = temp_data[idx_IN_columns]
            #print(extractedData)
            data[i] = np.asarray(extractedData , dtype=np.int)
            print(target[i])
       
        return Bunch(data=data, target=target)
    #            target_names=target_names)
                #feature_names=['sepal length (cm)', 'sepal width (cm)',
                #              'petal length (cm)', 'petal width (cm)'])


if __name__ == "__main__":
    #create_aras_sequentional_based_on_days_frequency_occurness()
    load_sequential_aras_frequency_occur(isPerson=False)