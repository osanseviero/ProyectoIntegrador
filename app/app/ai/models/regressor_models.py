"""TensorFlow regressor models estimators.
"""

import tensorflow as tf

def get_baseline_regressor():
    """Creates a Baseline Regressor TensorFlow Estimator.
    Returns: A tf.Estimator
    """
    regressor = tf.estimator.BaselineRegressor()
    print('wut')
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
    
    It only has support for binary classification
    Args:
      feature_columns: A list of tf.feature_columns.
    Returns: A tf.Estimator
    """
    classifier = tf.estimator.LinearRegressor(
        feature_columns=feature_columns)
    return classifier