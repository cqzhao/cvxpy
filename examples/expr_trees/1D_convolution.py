"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

#!/usr/bin/env python

from cvxpy import *
import numpy as np
import random

from math import pi, sqrt, exp

def gauss(n=11,sigma=1):
    r = range(-int(n/2),int(n/2)+1)
    return [1 / (sigma * sqrt(2*pi)) * exp(-float(x)**2/(2*sigma**2)) for x in r]

np.random.seed(5)
random.seed(5)
DENSITY = 0.008
n = 1000
x = Variable(n)
# Create sparse signal.
signal = np.zeros(n)
nnz = 0
for i in range(n):
    if random.random() < DENSITY:
        signal[i] = random.uniform(0, 100)
        nnz += 1

# Gaussian kernel.
m = 1001
kernel = gauss(m, m/10)

# Noisy signal.
std = 1
noise = np.random.normal(scale=std, size=n+m-1)
noisy_signal = conv(kernel, signal) #+ noise

gamma = Parameter(nonneg=True)
fit = norm(conv(kernel, x) - noisy_signal, 2)
regularization = norm(x, 1)
constraints = [x >= 0]
gamma.value = 0.06
prob = Problem(Minimize(fit), constraints)
solver_options = {"NORMALIZE": True, "MAX_ITERS": 2500,
                  "EPS":1e-3}
result = prob.solve(solver=SCS,
                    verbose=True,
                    NORMALIZE=True,
                    MAX_ITERS=2500)
# Get problem matrix.
data, dims = prob.get_problem_data(solver=SCS)

# Plot result and fit.
import matplotlib.pyplot as plt
plt.plot(range(n), signal, label="true signal")
plt.plot(range(n), np.asarray(noisy_signal.value[:n, 0]), label="noisy convolution")
plt.plot(range(n), np.asarray(x.value[:,0]), label="recovered signal")
plt.legend(loc='upper right')
plt.show()
