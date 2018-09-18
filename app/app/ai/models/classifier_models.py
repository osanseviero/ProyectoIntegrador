"""TensorFlow classifier models estimators.

Implements TensorFlow estimators that are able to classify a discrete variable
(regresion). The supported models are Baseline, Deep Neural Network and a
Linear Regressor.
"""

import tensorflow as tf

def get_baseline_classifier(label_names, classes):
    """Creates a Baseline Classifier TensorFlow Estimator.

    The Baseline Classifier ignores the features and learns the probabilities
    from the label.

    Args:
      label_names: A list with the label names.
      classes: The number of classes.
    Returns: A tf.Estimator
    """
    classifier = tf.estimator.BaselineClassifier(
        n_classes=classes,
        label_vocabulary=label_names)
    return classifier

def get_dnn_classifier(feature_columns, label_names, classes):
    """Creates a DNN Classifier TensorFlow Estimator.
    Args:
      feature_columns: A list of tf.feature_columns.
      label_names: A list with the label names.
      classes: The number of classes.
    Returns: A tf.Estimator
    """
    classifier = tf.estimator.DNNClassifier(
        feature_columns=feature_columns,
        # Two hidden layers of 10 nodes each.
        hidden_units=[10, 10],
        n_classes=classes,
        label_vocabulary=label_names)
    return classifier

def get_linear_classifier(feature_columns, label_names, classes):
    """Creates a Linear Classifier TensorFlow Estimator.
    Args:
      feature_columns: A list of tf.feature_columns.
      label_names: A list with the label names.
      classes: The number of classes.
    Returns: A tf.Estimator
    """
    classifier = tf.estimator.LinearClassifier(
        feature_columns=feature_columns,
        n_classes=classes,
        label_vocabulary=label_names)
    return classifier
