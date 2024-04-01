from pyspark import SparkConf, SparkContext
import sys

# This script takes two arguments, an input file and output directory.
if len(sys.argv) != 3:
    print('Usage: ' + sys.argv[0] + ' <in> <out>')
    sys.exit(1)
inputlocation = sys.argv[1]
outputlocation = sys.argv[2]

# Set up the configuration and job context
conf = SparkConf().setAppName('WordCount')
sc = SparkContext(conf=conf)

# Read in the dataset and immediately transform all the lines into arrays.
data = sc.textFile(inputlocation)
data_flat = data.flatMap(lambda line: line.split())
wordkeys = data_flat.map(lambda w: (w.lower(),1) )
wordcounts = wordkeys.reduceByKey(lambda x,y: x+y)

# Save the results in the specified output directory.
wordcounts.saveAsTextFile(outputlocation)
sc.stop() # Let Spark know that the job is done.
