"""TensorFlow models implementations.
"""

import tensorflow as tf

def get_baseline_classifier(label_names, classes):
    """Creates a Baseline Classifier TensorFlow Estimator.
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

def get_boosted_tree_classifier(feature_columns, label_names, classes):
    """Creates a Boosted Tree Classifier TensorFlow Estimator.
    
    It only has support for binary classification
    Args:
      feature_columns: A list of tf.feature_columns.
      label_names: A list with the label names.
      classes: The number of classes.
    Returns: A tf.Estimator
    """
    #TODO(osanseviero): Remove exception once 
    if classes != 2:
        raise ValueError("Boosted Tree Classifier only supports binary classification")
    classifier = tf.estimator.BoostedTreesClassifier(
        feature_columns=feature_columns,
        n_batches_per_layer=5,
        n_classes=classes,
        label_vocabulary=label_names)
    return classifier

def get_linear_classifier(feature_columns, label_names, classes):
    """Creates a Linear Classifier TensorFlow Estimator.
    
    It only has support for binary classification
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