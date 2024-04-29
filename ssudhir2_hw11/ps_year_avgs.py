
from pyspark import SparkConf, SparkContext
import sys

# this script takes two arguements, an input file, and an output directory
if len(sys.argv) != 3:
    print('Usage: ' + sys.argv[0] + ' <in> <out>')
    sys.exit(1)
inputlocation = sys.argv[1]
outputlocation = sys.argv[2]

# Set up the configuration and job context
conf = SparkConf().setAppName('YearlyAverages')
sc = SparkContext(conf = conf)

# Read in the data from the input file
data = sc.textFile(inputlocation)
data_flat = data.flatMap(lambda line: line.split('\n'))
data_flat = data_flat.filter(lambda x: x != '') # remove empty lines
data_arr = data_flat.collect()

def clean_list(data_arr):
    
    '''
    helper function to clean the data_arr

    ------------ inputs ------------
    data_arr : list
               list of strings where each string is in the format 'YYYYMMDD,TMAX,TMIN' 
    
    ------------ outputs ------------
    cleaned_arr : list
                  list of tuples where each tuple is in the format (YYYY, tmax, tmin)
    '''

    cleaned_arr = []

    for line in data_arr:
        curr_row = line.split(',')         # 'YYYYMMDD,TMAX,TMIN' -> ['YYYYMMDD', 'TMAX', 'TMIN']

        # checking to see if every line of the file follows the format specified (and skip rows with empty values).
        if (len(curr_row[0]) == 8) and (len(curr_row[1]) > 0) and (len(curr_row[2]) > 0):
            year = int(curr_row[0][:4])    # 'YYYYMMDD' -> YYYY
            tmax = float(curr_row[1])      # 'TMAX' -> tmax
            tmin = float(curr_row[2])      # 'TMIN' -> tmin 
            cleaned_arr.append((year, tmax, tmin)) # ['YYYYMMDD,TMAX,TMIN'] -> (YYYY, tmin, tmax)

        else:
            continue

    return cleaned_arr

def calculate_averages(cleaned_arr):

    '''
    helper function to calculate the average tmax and tmin for each year

    ------------ inputs ------------
    cleaned_arr : list
                  list of tuples where each tuple is in the format (YYYY, tmax, tmin)

    ------------ outputs ------------
    averages : list
               list of tuples where each tuple is in the format (YYYY, avgmax, avgmin)
    '''

    sums = {}
    counts = {}
    for year, tmax, tmin in cleaned_arr:
        # if the year is not in the dictionary, add it
        if year not in sums:
            sums[year] = [tmax, tmin]
            counts[year] = 1

        else:
            sums[year][0] += tmax   # add tmax
            sums[year][1] += tmin   # add tmin
            counts[year] += 1       # add count

    averages = []
    for year in sums:
        avgmax = round(sums[year][0]/counts[year], 2)    # take average of tmax's
        avgmin = round(sums[year][1]/counts[year], 2)    # take average of tmin's
        averages.append( (year, avgmax, avgmin) )        # append to the list, the tuple (year, avgmax, avgmin)

    return averages

# Convert the list to an RDD
averages_rdd = sc.parallelize(calculate_averages(clean_list(data_arr)))
averages_rdd.saveAsTextFile(outputlocation)

# Let spark know the job is done, processes can be ended
sc.stop()
