"""Generic library that trains a TensorFlow model based on a csv file.

This functions reads CSV files and trains and evaluates a TensorFlow Estimator
based on them.
"""

from models import classifier_models as cfm
from models import regressor_models as rgm
from hparams import HParams
from trainer_config import TrainerConfig
import tensorflow as tf


def construct_feature_columns(features):
    """Creates feature columns to be given to a tf.Estimator.
    Args:
      features: A list of Features objects
    Returns: A list of tf.feature_columns.
    """
    feature_columns = []
    for feature in features:
        if feature.numeric:
            feature_columns.append(tf.feature_column.numeric_column(
                key=feature.name
            ))
        else:
            feature_columns.append(tf.feature_column.indicator_column(
                tf.feature_column.categorical_column_with_vocabulary_list(
                    key=feature.name,
                    vocabulary_list=feature.vocabulary_list
                )
            ))
    return feature_columns


def get_input_fn(features, labels, batch_size, shuffle=True):
    """Creates a TensorFlow Estimator input_fn.
    Args:
      features: A pandas DataFrame with the features.
      labels: A pandas DataFrame with the label.
      batch_size: Number of lements to be fed to the model in each iteration.
      shuffle: Determines if data needs to be shuffled
    Returns: A TensorFlow input_fn
    """
    def input_fn():
        """Input function to be called in each step.
        Returns: A tuple containing tensors with the next batch of data.
        """
        # Create dataset from dataframe
        dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

        # Indefinitevely shuffle dataset and repeat data
        if shuffle:
            dataset = dataset.shuffle(buffer_size=5)

        dataset = dataset.repeat(count=None).batch(batch_size)

        # Get next batch of tensors
        return dataset.make_one_shot_iterator().get_next()
    return input_fn


def get_classifier_estimator(output_path, hparams, feature_columns, label_names, classes):
    """Creates a TF Estimator classifier based on the hyperparameters
    Args:
      output_path: Directory to save model parameters and graph.
      hparams: A HParams object with the model hyperparameters.
      feature_columns: TensorFlow feature columns.
      label_names: A list of strings with the label names.
      classes: The number of possible classification classes.
    """
    if hparams.model_type == 'baseline':
        return cfm.get_baseline_classifier(output_path, label_names, classes)
    elif hparams.model_type == 'NN':
        return cfm.get_dnn_classifier(output_path, feature_columns, label_names, classes)
    elif hparams.model_type == 'Linear':
        return cfm.get_dnn_classifier(output_path, feature_columns, label_names, classes)

def get_regressor_estimator(output_path, hparams, feature_columns):
    """Creates a TF Estimator regressor based on the hyperparameters
    Args:
      output_path: Directory to save model parameters and graph.
      hparams: A HParams object with the model hyperparameters.
      feature_columns: TensorFlow feature columns.
    """
    if hparams.model_type == 'baseline':
        return rgm.get_baseline_regressor(output_path)
    elif hparams.model_type == 'NN':
        return rgm.get_dnn_regressor(output_path, feature_columns)
    elif hparams.model_type == 'Linear':
        return rgm.get_linear_regressor(output_path, feature_columns)


def run_tf_model(output_path, hparams, classification, csv_path, label, features):
    """Implements and trains TensorFlow estimator.
    Args:
        output_path: Directory to save model parameters and graph.
        hparams: A HParams object with the model hyperparameters.
        classification: True for classification, False for regression.
        csv_path: String with the location of the CSV with the training data.
        label: Name of the column with the label.
        features: A list of Feature objects.
    Returns: Metrics obtained from evaluation.
    """
    config = TrainerConfig(classification, csv_path, label, features)
    feature_columns = construct_feature_columns(config.features)

    # Configure estimator.
    if config.classification:
        estimator = get_classifier_estimator(output_path, hparams, feature_columns, config.label_names,
                                             config.classes)
    else:
        estimator = get_regressor_estimator(output_path, hparams, feature_columns)

    # Training and evaluation specs.
    train_spec = tf.estimator.TrainSpec(input_fn=get_input_fn(config.train_x,
                                                              config.train_y,
                                                              batch_size=hparams.batch_size,
                                                              shuffle=False),
                                        max_steps=hparams.train_steps)

    eval_spec = tf.estimator.EvalSpec(input_fn=get_input_fn(config.test_x,
                                                            config.test_y,
                                                            1),
                                      steps=config.evaluation_steps)

    metrics = tf.estimator.train_and_evaluate(estimator, train_spec, eval_spec)
    return metrics
