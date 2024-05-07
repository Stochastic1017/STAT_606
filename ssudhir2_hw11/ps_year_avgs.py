
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

def change_date(line):

    '''                                                                                                                                                         
    helper function to extract relevant information from the input data                                                                                         
                                                                                                                                                                
    ------------ inputs ------------                                                                                                                            
    line :  str                                                                                                                                                 
            strings in the format 'YYYYMMDD,TMAX,TMIN'                                                                                                          
                                                                                                                                                                
    ------------ outputs ------------                                                                                                                           
    result :    tuple                                                                                                                                           
                tuples in the format (YYYY, tmax, tmin)                                                                                                         
    '''

    string_line= line.split(',')

    try:
        year = int(string_line[0][0:4])
        tmax = int(string_line[1])
        tmin = int(string_line[2])
    except:
        return None
    
    result = (year, tmax, tmin)
    return result

def get_avg(line):

    '''                                                                                                                                                         
    helper function to compute the average of the tmax and tmin for each year                                                                                   
                                                                                                                                                                
    ------------ inputs ------------                                                                                                                            
    line :  str                                                                                                                                                 
            strings in the format 'YYYYMMDD,TMAX,TMIN'                                                                                                          
                                                                                                                                                                
    ------------ outputs ------------                                                                                                                           
    result :    tuple                                                                                                                                           
                tuples in the format (YYYY, avgmax, avgmin)                                                                                                     
    '''

    year = line[0]
    values = list(line[1])
    avgmax = sum(x[1] for x in values) / len(values)
    avgmin = sum(x[2] for x in values) / len(values)
    result = (year, round(avgmax, 2), round(avgmin, 2))
    return result

# Read in the data from the input file                                                                                                                          
rdd = sc.textFile(inputlocation)              # Read data from input file                                                                                       
rdd = rdd.map(lambda line: change_date(line)) # 'YYYYMMDD,TMAX,TMIN' -> [YYYY, MM, DD, tmax, tmin]                                                              
rdd = rdd.filter(lambda x: x != None)         # Remove empty lines                                                                                              
rdd = rdd.groupBy(lambda x: x[0])             # Group by year                                                                                                   
rdd = rdd.map(lambda line: get_avg(line))     # Compute the average of the tmax and tmin for each year                                                          

# Let spark know the job is done, processes can be ended                                                                                                        
rdd.saveAsTextFile(outputlocation)
sc.stop()
