"""TensorFlow model implementations.

TODO(osanseviero): Change this to reusable hyperparameters
"""

import tensorflow as tf

def get_dnn_classifier(feature_columns, label_names):
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
        # The model must choose between 3 classes.
        n_classes=3,
        label_vocabulary=label_names)
    return classifier
