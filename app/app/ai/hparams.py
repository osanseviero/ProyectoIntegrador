"""Model Hyperparamers
"""
import pandas as pd
import numpy as np

class HParams():
    """Creates feature columns to be given to a tf.Estimator.
    Args:
      categorical: Boolean value. If false, it uses regression.
      csv_path: Path for the csv file with the data for the ML problem.
      label_idx: Column index that contains the label to be predicted.
    """
    def __init__(self, batch_size=None, train_steps=100):
        self.batch_size = batch_size
        self.train_steps = train_steps
