from hparams import HParams
from trainer import run_tf_model

class HPTuner():
    def __init__(self, classification=False, csv_path='', label='', features=[]):
        self.classification = classification
        self.path = csv_path
        self.label = label
        self.features = features

    def get_baseline(self):
        hparams = HParams(batch_size=1, train_steps=1, model_type='baseline')
        metrics = run_tf_model(hparams, self.classification, self.path, self.label, self.features)
        print(metrics)

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
    

if __name__ == "__main__":
    main()