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
      model_type: The type of TensorFlow estimator being used. Supports:
        - NN
        - baseline
        - BoostedTrees
        - Linear
    """
    #TODO(osanseviero): Add optimizer as hyperparameter.
    #TODO(osanseviero): Add support of conditional hparams.
    #TODO(osanseviero): Validate model type values.
    def __init__(self, batch_size=None, train_steps=100, model_type='NN'):
        self.batch_size = batch_size
        self.train_steps = train_steps
        self.model_type = model_type

#TODO(osanseviero): Implement HParam space class.
#TODO(osanseviero): Implement HParam space config with trainer_config.
#TODO(osanseviero): Implement HParam tuning with Grid and Random search.
