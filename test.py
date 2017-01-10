
if __name__ == "__main__" :
    import sys
    sys.path.append('./py/')
    import doctest
    doctest.testfile('./tests/tests.txt', verbose = True)
