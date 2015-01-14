import os
import pickle

current_dir = os.path.dirname(os.path.abspath(__file__))
counter_path = os.path.join(current_dir, 'res', 'counter.ppo')

f = open(counter_path, 'rb')
occurencies = pickle.load(f)
f.close()

_sum = sum([v for v in occurencies.values()])

def frequency(item):
    result = occurencies[item] / _sum
    if result == 0.0:
        return 0.000000001
    else:
        return result
