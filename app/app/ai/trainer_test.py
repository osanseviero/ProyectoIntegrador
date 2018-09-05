import trainer 
import tensorflow as tf
import pandas as pd
import unittest

class TestTrainerCase(unittest.TestCase):

    def test_construct_feature_columns(self):
        feature_name = ['test']
        feature_columns = trainer.construct_feature_columns(feature_name)

        expected = [tf.feature_column.numeric_column(key='test')]
        self.assertEqual(expected, feature_columns)

    def test_get_input_fn(self):
        features = {'col_1': [1, 2, 3, 4]}
        label = {'col_2': [0] * 4}

        features_df = pd.DataFrame.from_dict(features)
        label_df = pd.DataFrame.from_dict(label)

        input_fn = trainer.get_input_fn(features_df, label_df, 2, shuffle=False)
        result = input_fn()
        feature_tensor = result[0]['col_1']
        label_tensor = result[1]

        with tf.Session() as sess:
            # Each call to the tensor should give a new batch of data
            self.assertCountEqual(sess.run(feature_tensor), [1, 2])
            self.assertCountEqual(sess.run(feature_tensor), [3, 4])

            # Data should repeat itself
            self.assertCountEqual(sess.run(feature_tensor), [1, 2])

if __name__ == '__main__':
    unittest.main()