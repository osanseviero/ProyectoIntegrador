"""Model training configuration.

The TrainerConfig class contains generic configuration setup for a Machine
Learning model. The class configures the training and testing datasets, and
obtains the feature and label names to be used by TensorFlow Estimators.
"""
import pandas as pd
import numpy as np

class TrainerConfig():
    """Creates feature columns to be given to a tf.Estimator.
    Args:
      classification: Boolean value. If false, it uses regression.
      csv_path: Path for the csv file with the data for the ML problem.
      label_idx: Column index that contains the label to be predicted.
    """
    def __init__(self, classification, csv_path, label_idx):
        data = pd.read_csv(csv_path)
        # Make 70/30 split.
        train_df, test_df = np.split(data.sample(frac=1), [int(.7*len(data))])

         # Split into features and labels.
        self.train_x = train_df.drop([train_df.columns[label_idx]], axis=1)
        self.train_y = train_df[train_df.columns[label_idx]]
        self.test_x = test_df.drop(test_df.columns[label_idx], axis=1)
        self.test_y = test_df[test_df.columns[label_idx]]

        # TODO(osanseviero): Implement support for regression
        if classification:
            self.label_names = list(self.train_y.unique())
            self.classes = len(self.label_names)
            self.classification = True
        else:
            self.classification = False

        # Obtain feature names.
        self.feature_names = list(self.train_x.columns.values)

        # Evaluate the whole testing set.
        self.evaluation_steps = len(self.train_y.index)
