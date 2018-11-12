"""Model training configuration.

The TrainerConfig class contains generic configuration setup for a Machine
Learning model. The class configures the training and testing datasets, and
obtains the feature and label names to be used by TensorFlow Estimators.
"""
import pandas as pd
import numpy as np

class Feature:
    def __init__(self, name, numeric, vocabulary_list=None):
        self.name = name
        self.numeric = numeric
        self.vocabulary_list = vocabulary_list

class TrainerConfig():
    """Creates feature columns to be given to a tf.Estimator.
    Args:
      classification: Boolean value. If false, it uses regression.
      csv_path: Path for the csv file with the data for the ML problem.
      label: String with the name of the column label
      features: List of lists where the first element is the feature name and
                the second element is numerical or categorical.
    """
    def __init__(self, classification, csv_path, label, features):
        data = pd.read_csv(csv_path)

        # Make 70/30 split.
        train_df, test_df = np.split(data.sample(frac=1), [int(.7*len(data))])

        # Determine label column.
        label_idx = data.columns.get_loc(label)

         # Split into features and labels.
        self.train_x = train_df.drop([train_df.columns[label_idx]], axis=1)
        self.train_y = train_df[train_df.columns[label_idx]]
        self.test_x = test_df.drop(test_df.columns[label_idx], axis=1)
        self.test_y = test_df[test_df.columns[label_idx]]

        if classification:
            self.label_names = sorted(list(self.train_y.unique()))
            self.classes = len(self.label_names)
            self.classification = True
        else:
            self.classification = False

        # Obtain feature names.
        self.features = self.create_features(features)

        # Evaluate the whole testing set.
        self.evaluation_steps = len(self.train_y.index)

    def create_features(self, features):
        """Create a list of feature objects to be used by column constructor.
        Args:
          features: List of lists where the first element is the feature name and
                the second element is numerical or categorical.
        Returns: A list of Feature objects.
        """
        feature_list = []
        for feature in features:
            name = feature[0]
            feature_type = feature[1]
            if feature_type == 'numeric':
                feature_list.append(Feature(name, True))
            else:
                # Get column index
                idx = self.train_x.columns.get_loc(name)

                # Get column as Pandas Series
                col = self.train_x[self.train_x.columns[idx]]

                # Get all possible values
                feature_list.append(Feature(name, False, list(col.unique())))
        return feature_list
