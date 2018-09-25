"""Module that tunes HParams for a specific project

The HPTuner tunes the model HParams given a classification or regression
problem. The tuner reports the metrics and the hyperparameters used to obtain
those metrics.
"""
import math
import random
from hparams import HParams
from trainer import run_tf_model


class HPTuner():
    """Creates HyperParameters tuner.
    Args:
      output_path: Directory to save model parameters and graph.
      classification: False for regression.
      csv_path: String with the path of the CSV file for the project.
      label: Name of the label column.
      features: List of lists where the first element is the feature name and
                the second element is numerical or categorical.
      space: Dictionary that maps hyperparameter to possible values.
      metric: Metric to optimize.
      maximize: True to maximize and False to minimize.

    """
    def __init__(self, output_path, classification, csv_path, label, features, space, metric, maximize):
        self.output_path = output_path
        self.classification = classification
        self.path = csv_path
        self.label = label
        self.features = features
        self.space = space
        self.metric = metric
        self.maximize = maximize

        # Keep track of current trial, best trial and best reported metric
        self.trial_id = 0
        self.best_trial = 0

        if self.maximize:
            self.best_reported_metric = 0
        else:
            self.best_reported_metric = math.inf

    def get_baseline(self):
        """Runs a baseline model for the data.

        The baseline model learns the probabilities just from the labels and
        ignores the feature values.

        Returns: A dictionary with the metrics and the hyperparameters.
        """
        hparams = HParams(batch_size=1, train_steps=1, model_type='baseline')
        metrics = run_tf_model(self.output_path+'/'+str(self.trial_id), hparams, self.classification,
                               self.path, self.label, self.features)

        result = {}
        result['metrics'] = metrics
        result['hparams'] = hparams.__dict__
        result['trial'] = self.trial_id

        self.trial_id = self.trial_id + 1
        return result

    #TODO(osanseviero): Implement GridSearch
    def generate_trial(self):
        """Creates a random trial and reports the results
        When called, a new trial is generated. For the first trial, a baseline
        model is used.

        Returns: A dictionary with the metrics and the hyperparameters of the trial.
        """
        # Try baseline classifier for first trial
        if self.trial_id == 0:
            return self.get_baseline()

        # Get random hparams
        random_hparams = {}
        for hparam in self.space:
            random_hparams[hparam] = random.choice(self.space[hparam])

        hparams = HParams(**random_hparams)
        metrics = run_tf_model(self.output_path+'/'+str(self.trial_id), hparams, self.classification,
                               self.path, self.label, self.features)
        result = {}
        result['metrics'] = metrics
        result['hparams'] = hparams.__dict__
        result['trial'] = self.trial_id

        #TODO(osanseviero): Delete this once it's handled in Flask
        metric = metrics[0][self.metric]
        if self.maximize:
            if metric > self.best_reported_metric:
                self.best_reported_metric = metric
                self.best_trial = self.trial_id
        else:
            if metric < self.best_reported_metric:
                self.best_reported_metric = metric
                self.best_trial = self.trial_id

        self.trial_id = self.trial_id + 1
        return result
