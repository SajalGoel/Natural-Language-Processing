import os
import string
import json
import sys

rootdir = sys.argv[1]

spam_emails_count=0
ham_emails_count=0
spam_dict={}
ham_dict={}
spam_content=[]
ham_content=[]
spam_prob=0.0
ham_prob=0.0

for directories, subdirs, files in os.walk(rootdir):
    #print(directories, subdirs, len(files))
    for filename in files:
        fname = os.path.join(directories,filename)
        if "spam" in fname and "spam" in directories:
            if(fname.endswith('.txt')):
                with open(fname, 'r', encoding="latin1") as fopen:
                    spam_content = fopen.read()
                    spam_content = spam_content.lower()
                    spam_content = spam_content.translate(str.maketrans('', '', string.punctuation))
                    #table = str.maketrans("!?.-/:^*", 8*" ")
                    #content.translate(table)
                    spam_content = spam_content.replace("\n"," ").split(" ")
                    #print(content)
                    spam_emails_count = spam_emails_count + 1
                    for x in spam_content:
                        if x not in spam_dict:
                            spam_dict[x] = 1
                        else:
                            spam_dict[x] = spam_dict[x] + 1
        elif "ham" in fname and "ham" in directories:
            if(fname.endswith('.txt')):
                with open(fname, 'r', encoding="latin1") as fopen:
                    ham_content = fopen.read()
                    ham_content = ham_content.lower()
                    ham_content = ham_content.translate(str.maketrans('', '', string.punctuation))
                    #ham_content = ham_content.split(" ")
                    ham_content = ham_content.replace("\n", " ").split(" ")
                    ham_emails_count = ham_emails_count + 1
                    #print(ham_content)
                    for x in ham_content:
                        if x not in ham_dict:
                            ham_dict[x] = 1
                        else:
                            ham_dict[x] = ham_dict[x] + 1

#print("Ham emails count:",ham_emails_count)
#print("Spam emails count:",spam_emails_count)
#print(len(ham_dict))
#print(spam_dict['subject'])

spam_prob = (spam_emails_count / (spam_emails_count+ham_emails_count))
ham_prob = (ham_emails_count / (spam_emails_count+ham_emails_count))

model={
    "spam_dict":spam_dict,
    "ham_dict":ham_dict,
    "spam_prior":spam_prob,
    "ham_prior":ham_prob
    }

with open("nbmodel.txt",'w') as fopen:
    json.dump(model,fopen)

            
                            

                    

