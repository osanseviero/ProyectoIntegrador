"""Example of the Hypertuner system.

This is just an example of what data is needed by the tuner. To create trials,
the HPTuner needs
	- The features and their types, specified in the frontend by the user.
	- The label name.
	- The search space, which is specified for now.
	- The metric to optimize. loss is suggested for regression and accuracy for
	classification.
	- To know if it should maximize or minimize the target metric.

For each generated trial, the HPTuner reports the metrics, the hyperparameters
and the trial id.
"""

from tuner import HPTuner


def main():
    # Project 1 - regression

    # Features obtained from the CSV
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
    space = {
        "batch_size": [10, 50, 100, 200],
        "train_steps": [100, 1000, 2000, 3000],
        "model_type": ['NN', 'Linear'],
    }

    tuner = HPTuner(False,
                    "data/test/housing.csv",
                    label,
                    features,
                    space,
                    'loss',
                    maximize=False)

    print(tuner.generate_trial())
    print(tuner.generate_trial())
    print(tuner.generate_trial())
    print(tuner.generate_trial())


    # Project 2 - classification
    features = [['sepal_length', 'numeric'],
                ['sepal_width', 'numeric'],
                ['petal_length', 'numeric'],
                ['petal_width', 'numeric']]
    label = 'species'
    space = {
        "batch_size": [10, 50, 100, 200],
        "train_steps": [100, 1000, 2000, 3000],
        "model_type": ['NN', 'Linear'],
    }

    tuner = HPTuner(True,
                    "data/test/iris.csv",
                    label,
                    features,
                    space,
                    'accuracy',
                    maximize=True)
    print(tuner.generate_trial())
    print(tuner.generate_trial())
    print(tuner.generate_trial())


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
    space = {
        "batch_size": [100, 500, 1000, 2000],
        "train_steps": [100, 1000, 2000, 3000],
        "model_type": ['NN', 'Linear'],
    }

    tuner = HPTuner(False,
                    "data/test/fifa_ranking.csv",
                    label,
                    features,
                    space,
                    'loss',
                    maximize=False)
    print(tuner.generate_trial())
    print(tuner.generate_trial())


if __name__ == "__main__":
    main()
