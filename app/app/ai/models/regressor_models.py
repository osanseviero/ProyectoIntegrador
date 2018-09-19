"""TensorFlow regressor models estimators.

Implements TensorFlow estimators that are able to predict a variable
(regresion). The supported models are Baseline, Deep Neural Network and a
Linear Regressor.
"""

import tensorflow as tf

def get_baseline_regressor():
    """Creates a Baseline Regressor TensorFlow Estimator.

    The Baseline Regressor ignores the features and learns the probabilities
    from the label.

    Returns: A tf.Estimator
    """
    regressor = tf.estimator.BaselineRegressor()
    return regressor

def get_dnn_regressor(feature_columns):
    """Creates a DNN Regressor TensorFlow Estimator.
    Args:
      feature_columns: A list of tf.feature_columns.
    Returns: A tf.Estimator
    """
    regressor = tf.estimator.DNNRegressor(
        feature_columns=feature_columns,
        # Two hidden layers of 10 nodes each.
        hidden_units=[10, 10])
    return regressor

def get_linear_regressor(feature_columns):
    """Creates a Linear Regressor TensorFlow Estimator.
    Args:
      feature_columns: A list of tf.feature_columns.
    Returns: A tf.Estimator
    """
    classifier = tf.estimator.LinearRegressor(
        feature_columns=feature_columns)
    return classifier
