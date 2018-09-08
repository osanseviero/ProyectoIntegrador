"""Module that configures the project HyperParameters.

The HParams class allows to configure the model HyperParameters. The HParams
include how the model is going to learn (steps, batch, learning rate and
optimizer) and the model type and architecture.
"""
class HParams():
    """Creates HyperParameters configuration
    Args:
      batch_size: Number of data samples to give in each step.
      train_steps: Number of times to feed a batch of data to the model.
      model_type: The type of TensorFlow estimator being used. Currently,
      it supports NN (Neural Network) and Baseline.
    """
    def __init__(self, batch_size=None, train_steps=100):
        self.batch_size = batch_size
        self.train_steps = train_steps
        self.model_type = 'NN'
