import os
import sys
from random import randint
import numpy as np
import inspect
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from datareader import DataReader
import word2vec as wv
import util

file_path = os.path.join(parentdir, "data")
file_path = os.path.join(file_path, "Wiki.txt")
eval_path = os.path.join(parentdir, "evaluation")
eval_path = os.path.join(eval_path, "questions-words-ptbr.txt")

my_data = DataReader(file_path)
my_data.get_data()
word2index = my_data.word2index
index2word = my_data.index2word

BATCH_SIZE = np.array(range(1, 17)) * 10
number_of_exp = len(BATCH_SIZE)
results = []
info = []

for i, bs in enumerate(BATCH_SIZE):
    print("\n ({0} of {1})".format(i + 1, number_of_exp))
    config = wv.Config(batch_size=bs)
    attrs = vars(config)
    config_info = ["%s: %s" % item for item in attrs.items()]
    info.append(config_info)
    my_model = wv.SkipGramModel(config)
    embeddings = wv.run_training(my_model,
                                 my_data,
                                 verbose=False,
                                 visualization=False,
                                 debug=False)
    score, report = util.score(index2word,
                               word2index,
                               embeddings,
                               eval_path,
                               verbose=False,
                               raw=True)
    results.append(score)
    print("Score = {}".format(score))
    for result in report:
        print(result)

BATCH_SIZE = list(BATCH_SIZE)
best_result = max(list(zip(results, BATCH_SIZE, info)))
result_string = """In an experiment with {0} batch sizes
the best size is {1} with score = {2}.
\n INFO = {3}""".format(number_of_exp,
                        best_result[1],
                        best_result[0],
                        best_result[2])

file = open("batch_size.txt", "w")
file.write(result_string)
file.close()


plt.plot(BATCH_SIZE, results)
plt.xlabel("batch size")
plt.ylabel("score")
plt.savefig("batch_size.png")
