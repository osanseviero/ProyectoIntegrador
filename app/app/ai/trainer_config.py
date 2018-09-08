"""
"""
import pandas as pd
import numpy as np

class TrainerConfig():
    def __init__(self, categorical, csv_path, label_idx):
        df = pd.read_csv(csv_path)

        # Make 70/30 split
        train_df, test_df = np.split(df.sample(frac=1), [int(.7*len(df))])

         # Split into features and labels
        self.train_x = train_df.drop([train_df.columns[4]], axis=1)
        self.train_y = train_df[train_df.columns[4]]
        self.test_x = test_df.drop(test_df.columns[4], axis=1)
        self.test_y = test_df[test_df.columns[4]]

        # TODO(osanseviero): Implement support for regression
        if categorical:
            self.label_names = list(self.train_y.unique())

        # TODO(osanseviero): Implement support for categorical features
        self.feature_names = list(self.train_x.columns.values)

        # Feed 10% of the data in each iteration
        self.training_steps = len(self.train_x.index)
        print(self.training_steps)

        # Evaluate the whole testing set
        self.evaluation_steps = len(self.train_y.index)

