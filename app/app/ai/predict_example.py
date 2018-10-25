from hparams import HParams
from trainer import predict_tf_model
import pandas as pd

def main():
    # Model configuration for regression
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
    model_dir = 'data/output/test/housing/3'
    csv_dir = 'data/test/housing.csv'
    hparams = HParams(batch_size=10, train_steps=3000, model_type='Linear')


    # Predicting data
    # House with MV 24 
    predict_data = {'CRIM': [0.00632],
                    'ZN': [18],
                    'INDUS': [2.309999943],
                    'CHAS': [0],
                    'NOX': [0.537999988],
                    'RM': [6.574999809],
                    'AGE': [65.19999695],
                    'DIS': [4.090000153],
                    'RAD': [1],
                    'TAX': [296],
                    'PT': [15.30000019],
                    'B': [396.8999939],
                    'LSTAT': [4.980000019]}
    predict_df = pd.DataFrame.from_dict(predict_data) 

    predictions = predict_tf_model(model_dir, hparams, False, csv_dir, label, features, predict_data)
    print(list(predictions))

    # Model configuration for classification
    features = [['sepal_length', 'numeric'],
                ['sepal_width', 'numeric'],
                ['petal_length', 'numeric'],
                ['petal_width', 'numeric']]

    label = 'species'
    model_dir = 'data/output/test/iris/2'
    csv_dir = 'data/test/iris.csv'
    hparams = HParams(batch_size=50, train_steps=100, model_type='Linear')


    # Predicting data
    # Iris-virginica
    predict_data = {'sepal_length': [5.7],
                    'sepal_width': [2.5],
                    'petal_length': [5.0],
                    'petal_width': [2.0]}
    predict_df = pd.DataFrame.from_dict(predict_data) # Iris virginica sample

    predictions = predict_tf_model(model_dir, hparams, True, csv_dir, label, features, predict_data)
    print(list(predictions))
    

if __name__ == "__main__":
    main()
