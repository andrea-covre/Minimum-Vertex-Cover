import matplotlib.pyplot as plt
import numpy as np
import random

# vertex_count = 100

# INITIALIZATION_MODE = "poisson"

# if INITIALIZATION_MODE == "uniform":
#     get_number_of_nodes = lambda: random.randint(1, vertex_count)
            
# elif INITIALIZATION_MODE == "normal":
#     get_number_of_nodes = lambda: int(np.random.normal(vertex_count/2, vertex_count/4))
    
# elif INITIALIZATION_MODE == "exponential":
#     get_number_of_nodes = lambda: int(np.random.exponential(vertex_count/2))
    
# elif INITIALIZATION_MODE == "poisson":
#     get_number_of_nodes = lambda: int(np.random.poisson(vertex_count/2))

v = 198

class LOGNORMAL_PARAM:
    MU = 1
    SIGMA = 0.9
    DISTRIBUTION_RANGE = [0, 20]

def get_lognormal_vertexes_count():
    """ Returns a random number from a lognormal distribution """
    sample = np.random.lognormal(LOGNORMAL_PARAM.MU, LOGNORMAL_PARAM.SIGMA)
    
    src_lower_bound = LOGNORMAL_PARAM.DISTRIBUTION_RANGE[0]
    src_upper_bound = LOGNORMAL_PARAM.DISTRIBUTION_RANGE[1]
    
    dst_lower_bound = 0
    dst_upper_bound = v
    
    dst_span = dst_upper_bound - dst_lower_bound
    src_span = src_upper_bound - src_lower_bound
    
    valueScaled = float(sample - src_lower_bound) / float(src_span)
    mapped_sample = dst_lower_bound + (valueScaled * dst_span)
    
    random_vertex_count = int(v - mapped_sample)
    
    if random_vertex_count < 0: random_vertex_count = 0
    
    return random_vertex_count

x = []
for i in range(1000):
    x.append(get_lognormal_vertexes_count())
    
print(sum(x)/len(x))

exit()


vec_size = 100

mu = 1
sigma = 0.9
distribution_range = 20

s = np.random.lognormal(mu, sigma)
print(s)

def map_to_range(value, target_range):
    src_lower_bound = 0
    src_upper_bound = distribution_range
    
    dst_lower_bound = target_range[0]
    dst_upper_bound = target_range[1]
    
    dst_span = dst_upper_bound - dst_lower_bound
    src_span = src_upper_bound - src_lower_bound
    
    valueScaled = float(value - src_lower_bound) / float(src_span)
    
    return dst_lower_bound + (valueScaled * dst_span)
    
x = map_to_range(s, (0, vec_size))
print(x)

exit()
#s = s * vec_size
# s = vec_size - s

x = s / sum(s)
for i, j in zip(x, s):
    print(j, i)

count, bins, ignored = plt.hist(s, 1000, density=False)

x = np.linspace(min(bins), max(bins), 1000)
pdf = (np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2)) / (x * sigma * np.sqrt(2 * np.pi)))


plt.plot(x, pdf, linewidth=2, color='r')
plt.axis('tight')
plt.show()