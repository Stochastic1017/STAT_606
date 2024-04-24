
from mrjob.job import MRJob

class MRWordCount( MRJob ):

    '''
    MRWordCount class to count the number of words in a text file.

    -----------methods-----------
    MRJob: __init__, mapper, reducer 
    '''
    
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

        result = ""
        punctuations = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' # derived from running string.punctuations on a seperate cell
        for char in string:
            if char not in punctuations:
                result += char

        return result

    def mapper(self, _, line):
        
        '''
        Mapper function to count the number of words in a text file.

        -----------inputs-----------
        self: MRWordCount
              The MRWordCount object.

        _: str
           The key of the input file.
           (placeholder to indicate that the key is not used in the mapper function)

        line: str
              The line from the input file.

        -----------outputs----------
        self.remove_punctuations(word).lower(): str
                                                The word after removing punctuations and converting to lowercase. 
        '''

        # Split the line into list of words
        words = line.split()
        for word in words:
            # Yield the word after removing punctuations and converting to lowercase
            yield self.remove_punctuations(word).lower(), 1

    def reducer(self, word, counts):

        '''
        Reducer function to count the number of words in a text file.

        -----------inputs-----------
        self: MRWordCount
              The MRWordCount object.

        word: str
              The word from the input file.

        counts: list
                The list of counts of the word. 
        '''

        # Yield the word and the sum of the counts
        yield word, sum(counts)


if __name__ == '__main__':
    MRWordCount.run()

# Run the following command in the terminal to get the word counts
# Get-Content simple.txt | python mr_word_count.py | Out-File -FilePath simple_word_counts.txt