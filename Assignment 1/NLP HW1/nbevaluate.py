import os
import string
import sys
import json
import math


rootdir = sys.argv[1]

predict = []

with open(rootdir) as fopen:
    for data in fopen:
        split_data = data.find(" ")
        predict_label = data[0:split_data]
        file_path = data[split_data+1:]
        file_name = file_path[file_path.rfind("/")+1:]
        if "spam" in file_name:
            actual_label = "spam"
        else:
            actual_label = "ham"

        predict = predict + [(predict_label, actual_label)]

Matrix = [[0,0],[0,0]]
for values in predict:
    if(values[0] == values[1] == "ham"):
        Matrix[0][0] = Matrix[0][0] + 1
    elif(values[0] == "ham" and values[1] == "spam"):
        Matrix[1][0] = Matrix[1][0] + 1
    elif(values[0] == values[1] == "spam"):
        Matrix[1][1] = Matrix[1][1] + 1
    else:
        Matrix[0][1] = Matrix[0][1] + 1

#print(Matrix)

spam_precision = Matrix[1][1]/(Matrix[1][1] + Matrix[0][1])
spam_recall = Matrix[1][1]/(Matrix[1][1] + Matrix[1][0])
spam_fscore = 2 * spam_precision * spam_recall / (spam_precision + spam_recall)
print("Spam Precision:{0}, Spam Recall:{1}, Spam FScore:{2}".format(spam_precision,spam_recall,spam_fscore))

ham_precision = Matrix[0][0] / (Matrix[0][0] + Matrix[1][0])
ham_recall = Matrix[0][0] / (Matrix[0][0] + Matrix[0][1])
ham_fscore = 2 * ham_precision * ham_recall / (ham_precision + ham_recall)
print("Ham Precision:{0}, Ham Recall:{1}, Ham FScore:{2}".format(ham_precision,ham_recall,ham_fscore))


        
