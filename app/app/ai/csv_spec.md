# CSV Spec

All of the data fed to the ML models is obtained from csv files given by users. Because there is no formal spec of a csv file, and there are different csv structures in different structures, we are proposing a required format that users have to comply to. 

Here is a simple example:

AGE, COUNTRY
21, CANADA
19, MEXICO

|AGE  | COUNTRY |
|--|--|
| 21 | CANADA  |
| 19 | MEXICO |

The spec is:

 - All values in the row are separated by a comma. 
 - Rows don't end with a comma.
 - The first row of the csv file contains the name of the columns. This names can also be a number, but strings are strongly suggested.
 - The values should never have quotes.

## Example
**sepal_length,sepal_width,petal_length,petal_width,species**
5.7,2.5,5.0,2.0,Iris-virginica
6.4,2.8,5.6,2.2,Iris-virginica
4.6,3.1,1.5,0.2,Iris-setosa
7.7,2.6,6.9,2.3,Iris-virginica