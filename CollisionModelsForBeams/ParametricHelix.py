import numpy as np
from pyquaternion import Quaternion


def getCoordPointsAlongHellix(r, h, npt, tmax):
    x = np.zeros((npt,3), dtype = float)
    # field of tangent vectors
    xp = np.zeros((npt,3), dtype = float)
    t = np.linspace(0,tmax, npt)
    x[:,0] = r * np.cos(t)
    x[:,1] = r * np.sin(t)
    x[:,2] = h * t

    xp[:,0] = -r * np.sin(t)
    xp[:,1] = r * np.cos(t)
    xp[:,2] = h 

    # https://math.stackexchange.com/a/476311/392320
    q = np.zeros((npt,4), dtype = float)
    a = np.array([1,0,0])

    # from this link, it looks like we need to provide the unit tangent vectors to the curve
    for i in range(npt):
        #tangent to the curve at the node
        b = xp[i]/np.linalg.norm(xp[i])
        assert np.allclose(np.linalg.norm(b), 1.)
        v = np.cross(a,b)
        s = np.linalg.norm(v) 
        if not np.allclose(s, 0):
            c = np.dot(a,b)
            vskew = np.array([[0, -v[2], v[1]], [v[2], 0 , -v[0]], [-v[1], v[0], 0]  ])
            # rotation matrix rotating a into b
            R = np.eye(3) + vskew + np.dot(vskew, vskew) * ((1-c)/(s**2))
        else:
            R = np.eye(3)
        assert np.allclose(R.dot(a), b)
        # components are not in the right order 
        qi = Quaternion(matrix=R).elements
        q[i]= [qi[1], qi[2], qi[3], qi[0]]

    return x, q
