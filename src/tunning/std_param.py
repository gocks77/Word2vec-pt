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
file_path = os.path.join(file_path, "pt96.txt")
eval_path = os.path.join(parentdir, "evaluation")
eval_path = os.path.join(eval_path, "questions-words-ptbr.txt")

my_data = DataReader(file_path)
my_data.get_data()
word2index = my_data.word2index
index2word = my_data.index2word


pa1 = np.random.random_sample([10])
pa2 = np.random.random_sample([10]) / 10
pa3 = np.random.random_sample([10]) / 100
STD_PARAM = np.concatenate((pa1, pa2, pa3))
number_of_exp = len(STD_PARAM)

STD_PARAM.sort()
results = []

for i, pa in enumerate(STD_PARAM):
    print("\n ({0} of {1})".format(i + 1, number_of_exp))
    config = wv.Config(std_param=pa)
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
                               verbose=False)
    results.append(score)
    print("Score = {}".format(score))
    for result in report:
        print(result)

STD_PARAM = list(STD_PARAM)
best_result = max(list(zip(results, STD_PARAM)))
result_string = """In an experiment with {0} std params
the best one is {1} with score = {2}.""".format(number_of_exp,
                                                best_result[1],
                                                best_result[0])

file = open("std_param.txt", "w")
file.write(result_string)
file.close()


plt.plot(STD_PARAM, results)
plt.xscale('log')
plt.xlabel("std param")
plt.ylabel("score")
plt.savefig("std_param.png")
