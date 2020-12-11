import pycrfsuite
import csv
import glob
import os
import ntpath
import sys
from collections import namedtuple

train_dir = sys.argv[1]
test_dir = sys.argv[2]
out_file = sys.argv[3]

def get_utterances_from_file(dialog_csv_file):
    """Returns a list of DialogUtterances from an open file."""
    reader = csv.DictReader(dialog_csv_file)
    #print(reader)
    return [_dict_to_dialog_utterance(du_dict) for du_dict in reader]

def get_utterances_from_filename(dialog_csv_filename):
    """Returns a list of DialogUtterances from an unopened filename."""
    with open(dialog_csv_filename, "r") as dialog_csv_file:
        return get_utterances_from_file(dialog_csv_file)

def get_data(data_dir):
    """Generates lists of utterances from each dialog file.
    To get a list of all dialogs call list(get_data(data_dir)).
    data_dir - a dir with csv files containing dialogs"""
    dialog_filenames = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    #print(dialog_filenames)
    for dialog_filename in dialog_filenames:
        yield get_utterances_from_filename(dialog_filename)
def get_data2(data_dir):
    """Generates lists of utterances from each dialog file.
    To get a list of all dialogs call list(get_data(data_dir)).
    data_dir - a dir with csv files containing dialogs"""
    dialog_filenames = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    for dialog_filename in dialog_filenames:
        yield dialog_filename, get_utterances_from_filename(dialog_filename)

DialogUtterance = namedtuple("DialogUtterance", ("act_tag", "speaker", "pos", "text"))

PosTag = namedtuple("PosTag", ("token", "pos"))

def _dict_to_dialog_utterance(du_dict):
    """Private method for converting a dict to a DialogUtterance."""

    # Remove anything with
    for k, v in du_dict.items():
        if len(v.strip()) == 0:
            du_dict[k] = None

    # Extract tokens and POS tags
    if du_dict["pos"]:
        du_dict["pos"] = [
            PosTag(*token_pos_pair.split("/"))
            for token_pos_pair in du_dict["pos"].split()]
    return DialogUtterance(**du_dict)

#training=list(get_data("C:/Users/sajal/Downloads/train"))
#testing=list(get_data2("C:/Users/sajal/Downloads/test"))
#out_file = "output.txt"

training=list(get_data(train_dir))
testing=list(get_data2(test_dir))


#print("Hello")
#print(DialogUtterance)


#features=[]
#labels=[]

training_labels=[]
testing_labels=[]
training_features=[]
testing_features=[]
filelist=[]
for val in training:
    spk1 = ''
    spk2 = ''
    i=0
    fe=[]
    lb=[]
    for item in val:
        fa=[]
        spk2=getattr(item, "speaker")
        if i==0:
            fa.append("F")
        if i>0:
            if spk1!=spk2:
                fa.append("SC")

        toks=getattr(item, "pos")

        if toks is not None:
            for x in toks:
                fa.append("TOKEN_"+getattr(x, "token"))
            for x in toks:
                fa.append("POS_"+getattr(x, "pos"))

        lb.append(getattr(item, "act_tag"))
        #print(fa)
        fe.append(fa)
        print(fe)
        i+=1
        spk1=spk2
    training_features.append(fe)
    training_labels.append(lb)

trainer=pycrfsuite.Trainer(verbose=False)


for x, y in zip(training_features, training_labels):

    trainer.append(x, y)
trainer.set_params({
    'c1': 1.0,   # coefficient for L1 penalty
    'c2': 1e-2,  # coefficient for L2 penalty
    'max_iterations': 100,  # stop earlier

    # include transitions that are possible, but not observed
    'feature.possible_transitions': True
})

trainer.train('baseline.crfsuite')

for val in testing:
    spk1 = ''
    spk2 = ''
    i=0
    fe=[]
    lb=[]

    for item in val[1]:
        fa=[]
        spk2=getattr(item, "speaker")
        if i==0:
            fa.append("F")
        if i>0:
            if spk1!=spk2:
                fa.append("SC")

        toks=getattr(item, "pos")

        if toks is not None:
            for x in toks:
                fa.append("TOKEN_"+getattr(x, "token"))
            for x in toks:
                fa.append("POS_"+getattr(x, "pos"))

        lb.append(getattr(item, "act_tag"))
        fe.append(fa)
        i+=1
        spk1=spk2
    testing_features.append(fe)
    testing_labels.append(lb)
    filelist.append(val[0])




tagger = pycrfsuite.Tagger()
tagger.open('baseline.crfsuite')


f = open(out_file, 'w')
for i in range(len(testing_features)):
    #f.write("Filename=" + ntpath.basename(filelist[i])+'\n')
    pred=tagger.tag(testing_features[i])
    for j in range(len(pred)):
        f.write(pred[j]+'\n')
    f.write('\n')
f.close()
