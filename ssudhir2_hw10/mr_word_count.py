#!/usr/bin/env python3

from mrjob.job import MRJob

class MRWordCount( MRJob ):
    
    # Helper function to remove punctuations from a string
    # Took this from ssudhir2_hw3.ipynb
    def remove_punctuations(self, string):
        
        '''
        Helper function to remove punctuations from a string.

        -----------inputs-----------

        string: str
                The string from which punctuations need to be removed.

        -----------outputs----------

        result: str
                The string after removing punctuations.
        '''
        
        if not isinstance(string, (str, )):
            raise TypeError(f'string = {string} should be of type str.')

        result = ""
        punctuations = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' # derived from running string.punctuations on a seperate cell
        for char in string:
            if char not in punctuations:
                result += char

        return result

    def mapper(self, _, line):
        words = line.split()
        for word in words:
            yield self.remove_punctuations(word).lower(), 1

    def reducer(self, word, counts):
        yield word, sum(counts)


if __name__ == '__main__':
    MRWordCount.run()