import argparse

def parse_my_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--verbose',type=int,default=0)
    parser.add_argument('-m','--movie',action='store_true')
    parser.add_argument('-t','--carnum',type=int)
    parser.add_argument('-n','--nsteps',default=100000,type=int)
    args = parser.parse_args()
    return args
