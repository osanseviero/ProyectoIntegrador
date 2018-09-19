"""Module that tunes HParams for a specific project

The HPTuner tunes the model HParams given a classification or regression
problem. The tuner reports the metrics and the hyperparameters used to obtain
those metrics.
"""

from hparams import HParams
from trainer import run_tf_model

class HPTuner():
    """Creates HyperParameters tuner.
    Args:
      classification: False for regression.
      csv_path: String with the path of the CSV file for the project.
      label: Name of the label column.
      features: List of lists where the first element is the feature name and
                the second element is numerical or categorical.

    """
    def __init__(self, classification, csv_path, label, features):
        self.classification = classification
        self.path = csv_path
        self.label = label
        self.features = features

    def get_baseline(self):
        """Runs a baseline model for the data.

        The baseline model learns the probabilities just from the labels and
        ignores the feature values.

        Returns: A dictionary with the metrics and the hyperparameters.
        """
        hparams = HParams(batch_size=1, train_steps=1, model_type='baseline')
        metrics = run_tf_model(hparams, self.classification, self.path, self.label, self.features)

        result = {}
        result['metrics'] = metrics
        result['hparams'] = hparams.__dict__

        print(result)
        return result

    def get_linear(self):
        hparams = HParams(batch_size=100, train_steps=1000, model_type='Linear')
        metrics = run_tf_model(hparams, self.classification, self.path, self.label, self.features)

        result = {}
        result['metrics'] = metrics
        result['hparams'] = hparams.__dict__

        print(result)
        return result

    #TODO(osanseviero): Implement HParam space config with trainer_config.
    def tune(self, space):
        pass

#TODO(osanseviero): Implement HParam tuning with Grid and Random search.

def main():
    # Project 1 - regression
    features = [['CRIM', 'numeric'],
                ['ZN', 'numeric'],
                ['INDUS', 'numeric'],
                ['CHAS', 'numeric'],
                ['NOX', 'numeric'],
                ['RM', 'numeric'],
                ['AGE', 'numeric'],
                ['DIS', 'numeric'],
                ['RAD', 'numeric'],
                ['TAX', 'numeric'],
                ['PT', 'numeric'],
                ['B', 'numeric'],
                ['LSTAT', 'numeric']]
    label = 'MV'

    tuner = HPTuner(False,
                    "data/test/housing.csv",
                    label,
                    features)
    tuner.get_baseline()
    
    # Project 2 - classification
    features = [['sepal_length', 'numeric'],
                ['sepal_width', 'numeric'],
                ['petal_length', 'numeric'],
                ['petal_width', 'numeric']]
    label = 'species'
    tuner = HPTuner(True,
                    "data/test/iris.csv",
                    label,
                    features)
    tuner.get_baseline()

    # Project 3 - serious classification
    features = [['country_full', 'categorical'],
                ['country_abrv', 'categorical'],
                ['total_points', 'numeric'],
                ['previous_points', 'numeric'],
                ['rank_change', 'numeric'],
                ['cur_year_avg', 'numeric'],
                ['cur_year_avg_weighted', 'numeric'],
                ['last_year_avg', 'numeric'],
                ['last_year_avg_weighted', 'numeric'],
                ['two_year_ago_avg', 'numeric'],
                ['two_year_ago_weighted', 'numeric'],
                ['three_year_ago_avg', 'numeric'],
                ['three_year_ago_weighted', 'numeric'],
                ['confederation', 'categorical'],
                ['rank_date', 'categorical']]
    label = 'rank'
    tuner = HPTuner(False,
                    "data/test/fifa_ranking.csv",
                    label,
                    features)
    tuner.get_baseline()
    tuner.get_linear()
    

if __name__ == "__main__":
    main()
