import numpy as np
import pickle
import os
import matplotlib.pylab as plt
plt.close('all')

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

d = load_obj('./Tensile/infoSimu')
fileExt = r".txt"
fileDir = './Tensile/'
epsilonTarget = 0.01

L = [_ for _ in os.listdir(fileDir) if _.endswith(fileExt)]

nstep = np.loadtxt(fileDir+L[0]).shape[0]

arr = np.zeros((nstep, 3))

FReac = {} 
for i, file in enumerate(L):
    if 'ReactionForce' in file:
        arr += np.loadtxt(fileDir+file)[:, 1:4]
        FReac[file] = arr
    else:
        posDirichlet = np.loadtxt(fileDir+file)

posDirichlet = posDirichlet[:,1:4] # the first column stores the time
assert posDirichlet[0].shape == (3,)

t = np.loadtxt(fileDir+L[0])[:,0]
RFz = arr[:,2]

uDirichlet = posDirichlet - posDirichlet[0]

# length of the strand
h = d['lengthStrand']
# compute the strand axial strain
epsilon = uDirichlet[:,2] / h

assert 0.99 < epsilon[-1] / epsilonTarget < 1.01

filter = t <= 1

plt.figure()
plt.plot(t[filter], epsilon[filter])
ax = plt.gca()
ax.set_xlabel('time')
ax.set_ylabel(r'$\epsilon$ strand $\frac{l}{L}$')
plt.savefig(fileDir+ 'timeVSepsilon')

plt.figure()
plt.plot(epsilon[filter], RFz[filter], label='Sofa model with BFE')
# currve from Costello theory. Seen in the paper of Jiang, 1999  
# I just took 2 points on the curve of Fig. 5
slopeCostello = (150E3)/0.011
plt.plot(epsilon[filter], slopeCostello * epsilon[filter], label='Costello', linestyle='--')
ax = plt.gca()
ax.set_xlabel(r'$\epsilon$ strand $\frac{l}{L}$')
ax.set_ylabel(r'$F_{z}$')
ax.legend()
plt.savefig(fileDir+ 'epsilonVSAxialLoad')

plt.pause(0.1)