
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
                tuples in the format (YYYY, MM-DD, tmax, tmin)                                                                                                  
    '''

    string_line = line.split(',')

    try:
        year = int(string_line[0][0:4])
        month = int(string_line[0][4:6])
        day = int(string_line[0][6:])
        tmax = int(string_line[1])
        tmin = int(string_line[2])
    except:
        return None
    
    result = (year, f'{month}-{day}', tmax, tmin)
    return result

# Read in the data from the input file                                                                                                                          
rdd = sc.textFile(inputlocation)
rdd = rdd.map(lambda line: change_date(line)) # 'YYYYMMDD,TMAX,TMIN' -> [YYYY, MM, DD, tmax, tmin]                                                              
rdd = rdd.filter(lambda x: x != None)         # Remove empty lines                                                                                              
rdd = rdd.groupBy(lambda x: x[0])             # Group by year                                                                                                   
rdd = rdd.map(  lambda x: (x[0],                           # Year                                                                                               
                sorted(x[1], key = lambda y: -y[2])[0][1], # Date with max value in the third column                                                            
                sorted(x[1], key = lambda y: y[3])[0][1],  # Date with min value in the fourth column                                                           
            ))

# Let spark know the job is done, processes can be ended                                                                                                        
rdd.saveAsTextFile(outputlocation)
sc.stop()
