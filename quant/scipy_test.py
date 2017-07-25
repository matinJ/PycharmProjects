import numpy as np
import scipy.stats as stats
import scipy.optimize as opt

#random number created
rv_unif=stats.uniform.rvs(size=10)
print rv_unif

rv_beta = stats.beta.rvs(size=10,a=4,b=2)
print rv_beta

rv_norm = stats.norm.rvs(size = 10)
print rv_norm

np.random.seed(seed=2016)
print np.random.rand(2,3)

norm_dist = stats.norm(loc=0.5, scale=2)
n=200
dat = norm_dist.rvs(size=n)
print "mean of data is: " +str(np.mean(dat))
print "median of data is:" +str(np.median(dat))
print "standard deviation of data is: " + str(np.std(dat))