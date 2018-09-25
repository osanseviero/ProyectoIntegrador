"""TensorFlow regressor models estimators.

Implements TensorFlow estimators that are able to predict a variable
(regresion). The supported models are Baseline, Deep Neural Network and a
Linear Regressor.
"""

import tensorflow as tf

def get_baseline_regressor(model_dir):
    """Creates a Baseline Regressor TensorFlow Estimator.

    The Baseline Regressor ignores the features and learns the probabilities
    from the label.

    Args:
      model_dir: Directory to save model parameters and graph.
    Returns: A tf.Estimator
    """
    regressor = tf.estimator.BaselineRegressor(
        model_dir=model_dir)
    return regressor

def get_dnn_regressor(model_dir, feature_columns):
    """Creates a DNN Regressor TensorFlow Estimator.
    Args:
      model_dir: Directory to save model parameters and graph.
      feature_columns: A list of tf.feature_columns.
    Returns: A tf.Estimator
    """
    regressor = tf.estimator.DNNRegressor(
        feature_columns=feature_columns,
        model_dir=model_dir,
        # Two hidden layers of 10 nodes each.
        hidden_units=[10, 10])
    return regressor

def get_linear_regressor(model_dir, feature_columns):
    """Creates a Linear Regressor TensorFlow Estimator.
    Args:
      model_dir: Directory to save model parameters and graph.
      feature_columns: A list of tf.feature_columns.
    Returns: A tf.Estimator
    """
    classifier = tf.estimator.LinearRegressor(
        feature_columns=feature_columns,
        model_dir=model_dir)
    return classifier
