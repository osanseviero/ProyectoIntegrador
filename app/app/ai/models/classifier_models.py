"""TensorFlow classifier models estimators.

Implements TensorFlow estimators that are able to classify a discrete variable
(regresion). The supported models are Baseline, Deep Neural Network and a
Linear Regressor.
"""

import tensorflow as tf

def get_baseline_classifier(model_dir, label_names, classes):
    """Creates a Baseline Classifier TensorFlow Estimator.

    The Baseline Classifier ignores the features and learns the probabilities
    from the label.

    Args:
      model_dir: Directory to save model parameters and graph.
      label_names: A list with the label names.
      classes: The number of classes.
    Returns: A tf.Estimator
    """
    classifier = tf.estimator.BaselineClassifier(
        n_classes=classes,
        label_vocabulary=label_names,
        model_dir=model_dir)
    return classifier

def get_dnn_classifier(model_dir, feature_columns, label_names, classes):
    """Creates a DNN Classifier TensorFlow Estimator.
    Args:
      model_dir: Directory to save model parameters and graph.
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
        label_vocabulary=label_names,
        model_dir=model_dir)
    return classifier

def get_linear_classifier(model_dir, feature_columns, label_names, classes):
    """Creates a Linear Classifier TensorFlow Estimator.
    Args:
      model_dir: Directory to save model parameters and graph.
      feature_columns: A list of tf.feature_columns.
      label_names: A list with the label names.
      classes: The number of classes.
    Returns: A tf.Estimator
    """
    classifier = tf.estimator.LinearClassifier(
        feature_columns=feature_columns,
        n_classes=classes,
        label_vocabulary=label_names,
        model_dir=model_dir)
    return classifier
