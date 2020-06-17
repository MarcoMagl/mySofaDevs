from sympy import *

thetaS, m , thetaD0, rs, rd, alphaS = symbols('thetaS m thetaD0 rs rd alphaS')
thetaD = m * thetaS + thetaD0

xs = rs*cos(thetaS)
ys = rs*sin(thetaS)
zs = rs*tan(alphaS)*thetaS

xd = xs + rd * cos(thetaD) * cos(thetaS) - rd * sin(thetaD) * sin(thetaS) * sin(alphaS) 
yd = ys + rd * cos(thetaD) * sin(thetaS) + rd * sin(thetaD) * cos(thetaS) * sin(alphaS) 
zd = zs - rd * sin(thetaD) * cos(alphaS)

init_printing(use_unicode=False)

xdp = diff(xd, thetaS)
ydp = diff(yd, thetaS)
zdp = diff(zd, thetaS)

print('xdp =' + str(xdp) + '\n')
print('ydp =' + str(ydp) + '\n')
print('zdp =' + str(zdp) + '\n')