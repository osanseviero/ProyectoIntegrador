"""Generic library that trains a TensorFlow model based on a csv file.

This functions reads CSV files and trains and evaluates a TensorFlow Estimator
based on them.
"""

import tensorflow as tf
import models
from hparams import HParams
from trainer_config import TrainerConfig

# Data downloaded from https://archive.ics.uci.edu/ml/machine-learning-databases/iris/
CSV_PATH = "data/iris.csv"

def construct_feature_columns(feature_names):
    """Creates feature columns to be given to a tf.Estimator.
    Args:
      feature_names: A list of strings with the names of the columns
    Returns: A list of tf.feature_columns.
    """
    feature_columns = []
    for name in feature_names:
        feature_columns.append(tf.feature_column.numeric_column(key=name))
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

def run_tf_model(hparams):
    """Implements and trains TensorFlow estimator and prints metrics.
    """
    config = TrainerConfig(categorical=True, csv_path=CSV_PATH, label_idx=4)

    # TODO(osanseviero): Implement support for categorical features.
    feature_columns = construct_feature_columns(config.feature_names)

    # Configure estimator.
    estimator = models.get_dnn_classifier(feature_columns, config.label_names)

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

    # TODO(osanseviero): Implement ExportStrategy.
    metrics = tf.estimator.train_and_evaluate(estimator, train_spec, eval_spec)
    print(metrics)

def main():
    hparams = HParams(batch_size=1000, train_steps=100)
    run_tf_model(hparams)


if __name__ == "__main__":
    main()
