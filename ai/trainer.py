"""Generic library that trains a TensorFlow model based on a csv file.

This functions reads CSV files and trains and evaluates a TensorFlow Estimator
based on them.
"""

import tensorflow as tf
import pandas as pd
import models

# Data downloaded from https://archive.ics.uci.edu/ml/machine-learning-databases/iris/
TRAIN_URL = "data/iris-training.csv"
TEST_URL = "data/iris-testing.csv"

def construct_feature_columns(feature_names):
    """Creates feature columns to be given to a tf.Estimator
    Args:
      feature_names: A list of strings with the names of the columns
    Returns: A list of tf.feature_columns.
    """
    feature_columns = []
    for name in feature_names:
        feature_columns.append(tf.feature_column.numeric_column(key=name))
    return feature_columns

def get_training_input_fn(features, labels, batch_size):
    """Creates a TensorFlow Estimator input_fn to be using in training.
    Args:
      features: A pandas DataFrame with the training features.
      labels: A pandas DataFrame with the training label.
      batch_size: Number of lements to be fed to the model in each iteration.
    Returns: A TensorFlow input_fn
    """
    def train_input_fn():
        """Input function to be called in each training step.
        Returns: A tuple containing tensors with the next batch of data.
        """
        # Create dataset from dataframe
        dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

        # Indefinitevely shuffle dataset and repeat data
        configured_dataset = dataset.shuffle(buffer_size=5).repeat(count=None).batch(batch_size)

        # Get next batch of tensors
        return configured_dataset.make_one_shot_iterator().get_next()
    return train_input_fn

def get_evaluation_input_fn(features, labels, batch_size):
    """Creates a TensorFlow Estimator input_fn to be used in evaluation
    Args:
      features: A pandas DataFrame with the training features.
      labels: A pandas DataFrame with the training label.
      batch_size: Number of lements to be fed to the model in each iteration.
    Returns: A TensorFlow input_fn
    """
    def eval_input_fn():
        """Input function to be called in each evaluation step.
        Returns: A tuple containing tensors with the next batch of data.
        """
        inputs = (dict(features), labels)
        dataset = tf.data.Dataset.from_tensor_slices(inputs).batch(batch_size)

        return dataset.make_one_shot_iterator().get_next()
    return eval_input_fn


def run_tf_model():
    """Implements and trains TensorFlow estimator and prints metrics.
    """
    train_df = pd.read_csv(TRAIN_URL)
    test_df = pd.read_csv(TEST_URL)

    # Split into features and labels
    train_x = train_df.drop([train_df.columns[4]], axis=1)
    train_y = train_df[train_df.columns[4]]
    test_x = test_df.drop(test_df.columns[4], axis=1)
    test_y = test_df[test_df.columns[4]]

    # Get label names and feature columns
    label_names = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
    feature_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    feature_columns = construct_feature_columns(feature_names)

    # Configure estimator
    estimator = models.get_dnn_classifier(feature_columns, label_names)

    # Training and evaluation specs
    train_spec = tf.estimator.TrainSpec(input_fn=get_training_input_fn(train_x, train_y, 100),
                                        max_steps=100)
    eval_spec = tf.estimator.EvalSpec(input_fn=get_evaluation_input_fn(test_x, test_y, 100))

    # TODO(osanseviero): Implement ExportStrategy
    metrics = tf.estimator.train_and_evaluate(estimator, train_spec, eval_spec)
    print(metrics)

def main():
    """Main function"""
    run_tf_model()


if __name__ == "__main__":
    main()
