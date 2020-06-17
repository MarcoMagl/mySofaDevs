import numpy as np
import pickle
import os
import matplotlib.pylab as plt
import sys
plt.close('all')

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

files=sys.argv[1:]
ntests=len(files)
fig1=plt.figure()
ax = plt.gca()
ax.set_xlabel('time')
ax.set_ylabel(r'$\epsilon$ strand $\frac{l}{L}$')

fig2=plt.figure()
ax.set_xlabel(r'$\epsilon$ strand $\frac{l}{L}$')
ax.set_ylabel(r'$F_{z}$')

for i in range(ntests):
    File=files[i]
    nameSim = File.split('.')[0]
    DirectoryResults='./'+ nameSim + '/'

    d = load_obj(DirectoryResults + '/infoSimu')
    fileDir= d['DirectoryResults']
    fileExt = r".txt"

    # L = [_ for _ in os.listdir(fileDir) if _.endswith(fileExt)]

    # reaction force
    filesResults = ['MonitorBlockedNodes_f.txt']
    for i, f in enumerate(filesResults):
        arr = np.loadtxt(fileDir+f)
        t = arr[:,0]
        arr = arr[:, 1:]
        nn = int(arr.shape[1] / 3)
        arr = arr.reshape(-1, nn , 3)
        assert arr.shape[0] == t.shape[0]
        arr = np.sum(arr, axis = 1)
        if i == 0:
            RFz = arr[:,2]
        else:
            RFz += arr[:,2]
            
    # # displacement of the nodes
    f= 'MonitorMovingNodes_x.txt'
    posDirichlet = np.loadtxt(fileDir+f)
    tp = posDirichlet[:,0]
    assert np.allclose(t[:tp.shape[0]], tp)
    posDirichlet = posDirichlet[:, 1:4]
    
    # bothEndsPulled = 0
    # if bothEndsPulled:
    #     uDirichlet = 2 * posDirichlet - posDirichlet[0]
    # else:
    uDirichlet = posDirichlet - posDirichlet[0]
    #dispDirich = np.load("disp_moving_nodes").reshape(-1, )
    #nnodesBlocked = d["nnodesBlocked"]
    #dispDirich = dispDirich.reshape(-1, nnodesBlocked, 3)


    # length of the strand
    h = d['lengthStrand']
    # compute the strand axial strain
    epsilon = uDirichlet[:,2] / h

    filter = tp <= 1

    plt.figure(fig1.number)
    plt.plot(tp[filter], epsilon[filter], label=nameSim)

    plt.figure(fig2.number)
    plt.plot(epsilon[filter], RFz[filter], label=nameSim)

    if i ==0:
        # currve from Costello theory. Seen in the paper of Jiang, 1999  
        # I just took 2 points on the curve of Fig. 5
        slopeCostello = (150E3)/0.011
        plt.plot(epsilon[filter], slopeCostello * epsilon[filter], label='Costello', linestyle='--')


import os
DirectoryResults="./PostProcessing/"
if not os.path.exists(DirectoryResults):
    os.mkdir(DirectoryResults)
plt.figure(fig1.number)
ax = plt.gca()
ax.legend()
plt.savefig(DirectoryResults+ 'timeVSepsilon')

plt.figure(fig2.number)
ax = plt.gca()
ax.legend()
plt.savefig(DirectoryResults+ 'epsilonVSAxialLoad')
plt.pause(0.1)
