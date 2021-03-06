import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow import keras
from keras.utils import plot_model
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import roc_auc_score
from scipy.io import loadmat
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import StratifiedKFold
from scipy import optimize

STEP = 5000

def load_challenge_data(filename):
    x = loadmat(filename)
    data = np.asarray(x['val'], dtype=np.float64)
    new_file = filename.replace('.mat','.hea')
    input_header_file = os.path.join(new_file)
    with open(input_header_file,'r') as f:
        header_data=f.readlines()
    return data, header_data

def import_key_data(path):
    labels=[]
    ecg_filenames=[]
    for subdir, dirs, files in sorted(os.walk(path)):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".mat"):
                data, header_data = load_challenge_data(filepath)
                labels.append(header_data[15][5:-1])
                ecg_filenames.append(filepath)
    return labels, ecg_filenames

def load_ecg_data(path)



def random_mix_12lead(signal):
  """
  SSL Approach 1: Mixing the channels of ECG
  """
  order = np.arange(12)
  np.random.shuffle(order)
  return signal[:, order]

def split_join_12lead(signal, no_split=2):
  """
  SSL Approach 2: picking random channels, split it according to the number of 
  splits (no_split) and join them. 
  E.g. signal = [1,2,3,4,5,6], no_split = 2
      -> output = [4,5,6,1,2,3]
  """
  new_signal = np.copy(signal)
  order = np.arange(12)
  np.random.shuffle(order)
  # pick how many channels to split and join
  no_channels = np.random.randint(0, 12, size=1)[0] 
  for i in order[0:no_channels]:
    new_signal[:,i] = np.hstack(np.split(new_signal[:,i], no_split)[::-1])
  return new_signal

def SSL_batch_generator( signal, batch_size=3): 
    batch_signal = np.zeros((batch_size, STEP, 12))
    while True:
      for i in range(signal.shape[0]):
        batch_signal[0] = signal[i]
        batch_signal[1] = random_mix_12lead(signal[i])
        batch_signal[2] = split_join_12lead(signal[i], no_split=2)
      yield batch_signal





