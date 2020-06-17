import numpy as np
import pickle
import os
import matplotlib.pylab as plt
import sys
plt.close('all')


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


files = sys.argv[1:]
ntests = len(files)
assert ntests > 0, "No tests were provided !"
fig1 = plt.figure()
ax = plt.gca()
ax.set_xlabel('time')
ax.set_ylabel(r'$\epsilon$ strand $\frac{l}{L}$')

fig2 = plt.figure()
ax.set_xlabel(r'$\epsilon$ strand $\frac{l}{L}$')
ax.set_ylabel(r'$F_{z}$')

for i in range(ntests):
    File = files[i]
    nameSim = File.split('.')[0]
    DirectoryResults = './' + nameSim + '/'

    d = load_obj(DirectoryResults + '/infoSimu')
    fileDir = d['DirectoryResults']
    fileExt = r".txt"

    L = [_ for _ in os.listdir(fileDir) if _.endswith(fileExt)]

    # reaction force
    file = 'ReactionForce_f.txt'
    arr = np.loadtxt(fileDir + file)
    t = arr[:, 0]
    arr = arr[:, 1:]
    nn = int(arr.shape[1] / 3)
    arr = arr.reshape(-1, nn, 3)
    assert arr.shape[0] == t.shape[0]
    arr = np.sum(arr, axis=1)
    RFx = arr[:, 0]
    RFy = arr[:, 1]
    RFz = arr[:, 2]

    file = 'ReactionForce2WoROI_f.txt'
    arr2 = np.loadtxt(fileDir + file)
    t = arr2[:, 0]
    arr2 = arr2[:, 1:]
    nn = int(arr2.shape[1] / 3)
    arr2 = arr2.reshape(-1, nn, 3)
    assert arr2.shape[0] == t.shape[0]
    arr2 = np.sum(arr2, axis=1)
    RFx2 = arr2[:, 0]
    RFy2 = arr2[:, 1]
    RFz2 = arr2[:, 2]

    # displacement of the nodes
    file = 'CentralBeamDisplacementEnd_x.txt'
    posDirichlet = np.loadtxt(fileDir + file)
    tp = posDirichlet[:, 0]
    assert np.allclose(t[:tp.shape[0]], tp)
    posDirichlet = posDirichlet[:, 1:4]
    uDirichlet = posDirichlet - posDirichlet[0]

    # length of the strand
    h = d['lengthWire']
    # compute the strand axial strain
    epsilon = uDirichlet[:, 2] / h

    filter = t <= 1

    plt.figure(fig1.number)
    plt.plot(t[filter], epsilon[filter], '+', label=nameSim)

    plt.figure(fig2.number)
    plt.plot(epsilon[filter], RFx[filter], '+', label=nameSim + ' RFx')
    plt.plot(epsilon[filter], RFy[filter], '+', label=nameSim + ' RFy')
    plt.plot(epsilon[filter], RFz[filter], '+', label=nameSim + ' RFz')

DirectoryResults = "./PostProcessing/"
if not os.path.exists(DirectoryResults):
    os.mkdir(DirectoryResults)
plt.figure(fig1.number)
ax = plt.gca()
ax.legend()
plt.savefig(DirectoryResults + 'timeVSepsilon')

plt.figure(fig2.number)
ax = plt.gca()
ax.legend()
plt.savefig(DirectoryResults + 'epsilonVSAxialLoad')
plt.pause(0.001)
