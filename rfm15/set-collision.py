import matplotlib.pyplot as plt
import numpy as np
import math

def set_intersection(p, n):
    proba = 1
    for i in range(n):
        proba *= (p-n-i) / (p-i)
    return 1 - proba

universe = 2**16 # total number of ports
reserved = 2**10 # number of reserved ports (0-1024)

nmin=2**4
nmax=2**10
ns = range(nmin,nmax)
ps = [set_intersection(universe, n) for n in ns]

p50=0
p128=0
p256=0
p512=0
for i in range(len(ps)):
    if ps[i] > 0.5 and p50==0:
        p50=ns[i]
    if ns[i]==2**7:
        p128=ps[i]
    if ns[i]==2**8:
        p256=ps[i]
    if ns[i]==2**9:
        p512=ps[i]
plt.rc('font', size=28)

fig, ax = plt.subplots(figsize=(20,15), facecolor='white')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.ylim(0, 1)
plt.xlim(nmin, nmax)

plt.xlabel('Sets cardinality')
plt.ylabel('Set intersection probability')

plt.title('Set intersection probability against set cardinality')

plt.yticks([i/10 for i in range(11)])
plt.semilogx(base=2)
plt.plot(ns,ps)

def get_xmax(n):
    return (math.log(n,2)-math.log(nmin,2))/(math.log(nmax,2)-math.log(nmin,2))

plt.text(2**7.4, 0.05, '213', color='red')
plt.axhline(y=0.5, xmin=0, xmax=get_xmax(p50), color='red', ls='dotted')
plt.axvline(x=p50, ymin=0, ymax=0.5, color='red', ls='dotted')

plt.text(2**4.5, 0.18, '0.2216', color='red')
plt.axhline(y=p128, xmin=0, xmax=get_xmax(2**7), color='red', ls='dotted')
plt.axvline(x=2**7, ymin=0, ymax=p128, color='red', ls='dotted')

plt.text(2**4.5, 0.59, '0.6336', color='red')
plt.axhline(y=p256, xmin=0, xmax=get_xmax(2**8), color='red', ls='dotted')
plt.axvline(x=2**8, ymin=0, ymax=p256, color='red', ls='dotted')

plt.text(2**4.5, 0.94, '0.9823', color='red')
plt.axhline(y=p512, xmin=0, xmax=get_xmax(2**9), color='red', ls='dotted')
plt.axvline(x=2**9, ymin=0, ymax=p512, color='red', ls='dotted')

plt.savefig('fig.png')