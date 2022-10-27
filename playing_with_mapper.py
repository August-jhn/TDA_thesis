import kmapper as km
import numpy as np

mapper = km.KeplerMapper(verbose = 2)

print(type(mapper))
print("KeplerMapper is a class")

print(type(mapper.fit_transform))
