import matplotlib.pyplot as plt
import math

fig, ax = plt.subplots()
plt.axis([0.5, 1, 0, 1])
T = range(0, 100000)
for n in range(6, 16, 2):
    sec = [1 - math.pow(1 - 1 / n, t) for t in T]
    ps = [64 / 1000 * t * n for t in T]
    vp = [t * n / math.pow(2, n) for t in T]
  
    ax.plot(sec, vp, label='n={}'.format(n))
    ax.set_xlabel('Security')
    ax.set_ylabel('Ratio of Verifier to Prover Work')
    ax.legend()
plt.show()
