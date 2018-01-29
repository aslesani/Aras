'''
Created on Oct 29, 2016

@author: Adele

==================================================
Create summerized data files from Aras Data set (House A)  in folder
E:\Lessons_tutorials\Behavioural user profile articles\Datasets\Aras\House A\Summery 
==================================================

'''

from numpy import dtype
from _ast import Str
from asyncore import read
import re
print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets
from os.path import join


def remove_duplicate_lines():
    
    for index in range(1,31):#31
        day_number = "DAY_" + str(index) + ".txt"
        f = open( join(r"E:\Lessons_tutorials\Behavioural user profile articles\Datasets\Aras\House A" , day_number ),"r")
        #lines = f.readlin()
        with open( join(r"E:\Lessons_tutorials\Behavioural user profile articles\Datasets\Aras\House A\Summery" , day_number), 'w') as summery_file:
            
            counter = 0
            previous = ""
            first_line = False
            for line in f:
                if first_line == False:
                    first_line = True
                    number_of_columns = len(line.split())-1
                    #write number of rows and columns, write 00000 for rows and then update it
                    #it is important that the updated value should have 5 char width
                    summery_file.write("00000," + str(number_of_columns) + "\n" )

                #print(line)
                #counter +=1
                if line != previous :
                    #the current format stores both prrson1 and person2 activities in a one row.
                    #the next lines separate them and store each person's activity in diffrent lines
                    cells = line.split()
                    #print(cells)
                    person1_activity = cells[-2]
                    person2_activity = cells[-1]
                    #print(person1_activity)
                    #print(person2_activity)
                    common_sensor_events = " ".join(x for x in cells[0:-2])
                    person1_line = common_sensor_events + " " + "1" + " " + person1_activity + "\n"
                    person2_line = common_sensor_events + " " + "2" + " " + person2_activity + "\n"

                    summery_file.write(person1_line.replace(' ' , ','))
                    summery_file.write(person2_line.replace(' ' , ','))

                    counter += 1
                    #print("counter: " + str(counter))
                 
                previous = line    
            
            #update number of rows at first line of file 
            #2 is because of writing for each person a separate line
            counter_string = str(counter*2)
            counter_length = len (counter_string)
               
            updated_first_line = counter_string + "," + str(number_of_columns)
            for i in range (0 , 5-counter_length):
                updated_first_line += ' '
            updated_first_line += "\n"    
            summery_file.seek(0)
            summery_file.write(updated_first_line) 
            #end update number of rows at first line of file 
       
        
        f.close()


def no_sequence_knn():
    pass
    
if __name__ == "__main__":
    remove_duplicate_lines()
