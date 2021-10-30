from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pandas as pd
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

spark = SparkSession.builder.appName("PySpark SESSION NAME") \
    .config('spark.sql.shuffle.partitions', 300).config('spark.worker.cleanup.enabled', 'True').config("spark.some.config.option", "some-value") \
    .getOrCreate()

# reads the data in a spark dataframe
df = spark.read.options(header=True, inferSchema=True).csv("FILENAME.csv")
df.show(5)

# drops columns
df = df.drop('column1', 'column2')

# gets the name of the columns in the dataframe
print("The columns of the dataframe are:", df.columns)

# prints the types of each column
print("The types of each column are as follows:", df.dtypes)

# prints the number of records
print("The number of records is:", df.count())

# prints the number of distinct entries in column1
print("The number of distinct entries in column1 is:", df.select("column1").distinct().show())

# remove the rows with x in column1
df = df[df.column1 != 'x']

# add column with the timestamp format of data
df = df.withColumn("timestamp_date", F.to_timestamp("date"))

# counts the number of missing values per column
print("The number of missing values per column is:")
df.select([F.count(F.when(F.isnull(c), c)).alias(c) for c in df.columns]).show()

# counts values for column1
df.groupBy('column1').count().show()

# summarize the variables column1, column2, and column2
df.describe(['column1', 'column2', 'column3']).show()

# removes the rows who have values outside the predefidend boundaries
df = df.filter(df.column1 > lower_bound).filter(df.column1 < upper_bound)

# removes the rows with dates outside the range
upper_bound = datetime.datetime(year1, month1, day1)
lower_bound = datetime.datetime(year2, month2, day2)
df_bounded = df.filter(df.timestamp_date > lower_bound).filter(df.timestamp_date < upper_bound)

print("The earliest date is:", df_bounded.agg({"timestamp_date": "min"}).collect()[0][0])
print("The latest date is:", df_bounded.agg({"timestamp_date": "max"}).collect()[0][0])

# counts the number of records that remained
print("The number of remained records is:", df.count())

proportion = 0.5 # the proportion of the pyspark dataframe to be converted to pandas and then plotted
# the smaller the worst the picture, the larger the more memory and time consumed with the transition

b1 = df.select("column1_num", "column2_cat").sample(False, proportion).toPandas()
# plots the boxplot between numerical systolic and categorical successfulMeasurement
sns.boxplot(x=b1['column1_num'], y=b1['column2_cat']).set_title('Boxplot of column1_num based on the column2_cat')
plt.show()

# plots the distribution of systolic
plot1 = sns.displot(df.select("column1").sample(False, proportion).toPandas())
plt.title("Distribution of column1")

# selects data via SQL query
df.createOrReplaceTempView('table')
df1 = spark.sql('SELECT '
                'FROM table')

# executes function1 on column1 and adds the results in a new variable column2
spark.udf.register('udf1', function1)
df = df.withColumn('column2', F.expr("udf1(column1)"))