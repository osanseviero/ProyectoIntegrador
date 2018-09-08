"""TensorFlow model implementations.

TODO(osanseviero): Change this to reusable hyperparameters
"""

import tensorflow as tf

def get_dnn_classifier(feature_columns, label_names, classes):
    """Creates a DNN Classifier TensorFlow Estimator.
    Args:
      feature_columns: A list of tf.feature_columns.
      label_names: A list with the label names.
    Returns: A tf.Estimator
    """
    classifier = tf.estimator.DNNClassifier(
        feature_columns=feature_columns,
        # Two hidden layers of 10 nodes each.
        hidden_units=[10, 10],
        n_classes=classes,
        label_vocabulary=label_names)
    return classifier

def get_baseline_classifier(label_names, classes):
    classifier = tf.estimator.BaselineClassifier(
        n_classes=classes,
        label_vocabulary=label_names)
    return classifier