
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
                  list of tuples where each tuple is in the format (YYYY, tmax, tmin)                                                                              '''

    cleaned_arr = []

    for line in data_arr:
        curr_row = line.split(',')         # 'YYYYMMDD,TMAX,TMIN' -> ['YYYYMMDD', 'TMAX', 'TMIN']

        # checking to see if every line of the file follows the format specified (and skip rows with empty values).
        if (len(curr_row[0]) == 8) and (len(curr_row[1]) > 0) and (len(curr_row[2]) > 0):
            year = int(curr_row[0][:4])    # 'YYYYMMDD' -> YYYY
            day = int(curr_row[0][4:6])    # 'YYYYMMDD' -> MM
            month = int(curr_row[0][6:8])  # 'YYYYMMDD' -> DD                                                                                                  
            tmax = float(curr_row[1])      # 'TMAX' -> tmax
            tmin = float(curr_row[2])      # 'TMIN' -> tmin                                                                    
            cleaned_arr.append((year, day, month, tmax, tmin)) # ['YYYYMMDD,TMAX,TMIN'] -> (YYYY, MM, DD, tmin, tmax)
            
        else:
            continue

    return cleaned_arr

def find_extremes(cleaned_arr):
    
    '''
    helper function to find the maximum tmax, and minimum tmin for each year

    ------------ inputs ------------
    cleaned_arr : list
                  list of tuples where each tuple is in the format (YYYY, tmax, tmin)

    ------------ outputs ------------
    extremes : list
               list of tuples where each tuple is in the format (YYYY, MM-DD, mm-dd) 
    '''

    maximum = {}
    minimum = {}
    for year, day, month, tmax, tmin in cleaned_arr:
        # if the year is not in the dictionary, add it
        if year not in maximum:
            maximum[year] = (tmax, f'{month}-{day}')
        # else, if current maximum is greater than maximum before, replace it
        else:
            if tmax > maximum[year][0]:
                # replace the value at key 'year' with tuple (current_maximum, MM-DD)
                maximum[year] = (tmax, f'{month}-{day}')

        # if the year is not in the dictionary, add it
        if year not in minimum:
            minimum[year] = (tmin, f'{month}-{day}')
        # else, if current minimum is lesser than minimum before, replace it
        else:
            if tmin < minimum[year][0]:
                # replace the value at key 'year' with tuple (current_minimum, mm-dd)
                minimum[year] = (tmin, f'{month}-{day}')

    # replace the value at key 'year' with tuple (MM-DD, mm-dd)
    extremes = [(year, maximum[year][1], minimum[year][1]) for year in maximum]

    return extremes

# Convert the list to an RDD                                                                                                                                   
extremes_rdd = sc.parallelize(find_extremes(clean_list(data_arr)))
extremes_rdd.saveAsTextFile(outputlocation)

# Let spark know the job is done, processes can be ended                                                                                                      
sc.stop()
