from mrjob.job import MRJob

class MRBigProduct(MRJob):

    def mapper(self, _, line):
        yield None,float(line.strip())

    def reducer(self, _, values):
        #yield None,sum(values)
        #yield max(values)
        yield None,reduce(lambda x,y: x*y, values, 1)

if __name__ == '__main__':
    MRBigProduct.run()

