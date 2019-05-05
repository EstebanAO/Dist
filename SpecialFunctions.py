import sys
import statistics
import math 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def pow(value, power):
    return value**power

def sqrt(value, power):
    return value**(1.0/power)

def mode(list):
    return max(set(list), key = list.count)

def prob(list, value):
    return list.count(value)/len(list)

def moment(values, n):
	res = 0
	lst = list(set(values))
	for i, val in enumerate(lst): 
		p = prob(values, val)
		res = res + p * (val) ** n
	return res

def median(values):
	return statistics.median(values)

def var(values):
	return moment(values, 2) - moment(values, 1) ** 2

def exp_bernoulli(p):
    if p > 1 or p < 0:
        raise Exception("In exp_bernoulli, p must be a value between 1 and 0")
    return p

def var_bernoulli(p):
    if p > 1 or p < 0:
        raise Exception("In var_bernoulli, p must be a value between 1 and 0")
    return p * (1 - p)

def comb(n, k):
	return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))
	
def prob_binomial(p, n, k):
    if p > 1 or p < 0:
        raise Exception("In var_bernoulli, p must be a value between 1 and 0")
    if k > n or k < 0:
        raise Exception("In var_bernoulli, k must be a value between 0 and n")
    if n < 0:
        raise Exception("In var_bernoulli, n must be grater than 0")
    return comb(n, k) * (1 - p) ** (n - k) * p ** k

def prob_geometric(k, p):
	if k < 1:
		raise Exception("In prob_geometric, the k value must be greater or equal to 1")
	return (1 - p) ** (k - 1) * p

def exp_binomial(p, n):
	return n * p
	
def var_binomial(p, n):
	return n * p * (1 - p)

def prob_geometric(k, p):
    if k < 1:
	    raise Exception("In prob_geometric, the k value must be greater or equal to 1")
    if p > 1 or p < 0:
        raise Exception("In prob_geometric, p must be a value between 1 and 0")
    return ((1 - p) ** (k - 1)) * p

def exp_geometric(p):
    return 1.0 / p

def var_geometric(p):
    return (1.0 - p) / (p**2)

def plot_histogram(list):
    x = np.asarray(list)
    plt.hist(x, bins=20)
    plt.show()
    