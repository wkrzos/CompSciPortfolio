import time
def Timer(f):
    def inner(*a,**k):
        t0=time.time()
        res=f(*a,**k)
        return res,(time.time()-t0)
    return inner
