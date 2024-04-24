
from mrjob.job import MRJob

class MRStatistics( MRJob ):

    def mapper(self, _, line):
        '''
        Mapper function that reads the input file and yields the key and value.

        -----------inputs-----------
        self: MRStatistics
              The MRStatistics object.

        _: str
           The key of the input file.
           (placeholder to indicate that the key is not used in the mapper function) 
        
        line: str
              The line from the input file.

        -----------outputs----------
        key: str
             The key from the input file.

        value: float
               The value from the input file.
        '''
        # file is always of the form
        # "key" "value"
        key = line.split()[0] # gets key (in str)
        value = float(line.split()[1]) # gets value (in float)
        yield key, value

    def reducer(self, key, values):
        
        '''
        Reducer function that reads the input file and yields the key, count, mean, and variance.

        -----------inputs-----------
        self: MRStatistics
              The MRStatistics object.

        key: str
             The key from the input file.

        values: list
                The list of values from the input file.

        -----------outputs----------
        key: str
             The key from the input file.

        (count, mu, var): tuple
                          The tuple containing the count, mean, and variance of the values. 
        '''
        # initialize variables
        values = list(values)
        sum_mu = 0.0
        sum_sd = 0.0
        count = 0

        # calculate mean
        # mu = sum(x) / n
        for value in values:
            sum_mu += value
            count += 1
        mu = sum_mu / count
        
        # calculate variance
        # var = sum((x - mu) ** 2) / (n - 1) ---> note: this is the unbiased estimator of sd
        for value in values:
            sum_sd += (value - mu)**2
        var = (sum_sd / (count - 1))

        yield key, (count, mu, var)

if __name__ == '__main__':
    MRStatistics.run()