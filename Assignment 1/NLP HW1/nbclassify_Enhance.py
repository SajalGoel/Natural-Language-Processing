import json
import sys
import math
import os
import string

#rootdir = sys.argv[1]
rootdir = "D:\\Sajal\\USC\\Semesters\\Spring 2020\\NLP\\Assignment 1\\dev"

classification = ""


with open("nbmodelEnhance2.txt", "r", encoding="latin1") as model:
    data = json.load(model)

spam_prior = float(data['spam_prior'])
ham_prior = float(data['ham_prior'])

spam_dict = data['spam_dict']
ham_dict = data['ham_dict']

vocab = list(set(list(spam_dict.keys()) + list(ham_dict.keys())))
vocab_len = len(vocab)
#print(vocab_len)

spam_count = sum(list(spam_dict.values()))
ham_count = sum(list(ham_dict.values()))

for directories, subdirs, files in os.walk(rootdir):
    for filename in files:
        fname = os.path.join(directories,filename)
        if(fname.endswith('.txt')):
            with open(fname, 'r', encoding="latin1") as fopen:
                content = fopen.read()
                content = content.lower()
                content = content.translate(str.maketrans('', '', string.punctuation))
                content = content.replace("\n"," ").split(" ")
                length=[]
                for word in content:
                    if word in spam_dict:
                        length.append(spam_dict[word])
                    elif word in ham_dict:
                        length.append(0)
                    else:
                        length.append(-1)

                length = [l for l in length if l != -1]
                log_prob = []
                for l in length:
                    log_prob.append(math.log((l+1)/(spam_count + vocab_len)))
                totalProb_spam = sum(log_prob) + math.log(spam_prior)

                length = []
                for word in content:
                    if word in ham_dict:
                        length.append(ham_dict[word])
                    elif word in spam_dict:
                        length.append(0)
                    else:
                        length.append(-1)

                length = [l for l in length if l != -1]
                log_prob = []
                for l in length:
                    log_prob.append(math.log((l+1)/(ham_count + vocab_len)))
                totalProb_ham = sum(log_prob) + math.log(ham_prior)


                if(totalProb_ham > totalProb_spam):
                    classification = classification + "ham" + "\t" + fname + "\n"
                else:
                    classification = classification + "spam" + "\t" + fname + "\n"

output = open("nboutput_Enhance.txt", "w")
output.write(classification)
output.close()          








                        
