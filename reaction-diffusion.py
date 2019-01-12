import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors

n = 256
X = np.random.randint(0,2,(n, n))
# Ask for parameter type
para_type = int(input("Enter index for animation type\n\
0: bacteria 1\n\
1: bacteria 2\n\
2: coral\n\
3: fingerprint\n\
4: spirals\n\
5: spirals dense\n\
6: spirals fast\n\
7: unstable\n\
8: worms 1\n\
9: worms 2\n\
10: zebrafish\n"))

# Ask to save video and if a video is saved,
# ask for desired file name
save_video = int(input("Save video?\n\
enter 0 for no and 1 for yes\n"))
if save_video == 0:
	save_video = False
else:
	save_video = True
if save_video:
	video_fname = str(input("Please enter desired file name\n"))+'.mp4'
	print('The video name will be', video_fname, type(video_fname))

params = []
params.append((0.16, 0.08, 0.035, 0.065)) # Bacteria 1
params.append((0.14, 0.06, 0.035, 0.065)) # Bacteria 2
params.append((0.16, 0.08, 0.060, 0.062)) # Coral
params.append((0.19, 0.05, 0.060, 0.062)) # Fingerprint
params.append((0.10, 0.10, 0.018, 0.050)) # Spirals
params.append((0.12, 0.08, 0.020, 0.050)) # Spirals Dense
params.append((0.10, 0.16, 0.020, 0.050)) # Spirals Fast
params.append((0.16, 0.08, 0.020, 0.055)) # Unstable
params.append((0.16, 0.08, 0.050, 0.065)) # Worms 1
params.append((0.16, 0.08, 0.054, 0.063)) # Worms 2
params.append((0.16, 0.08, 0.035, 0.060)) # Zebrafish
(Du, Dv, F, k) = params[para_type]
#k = np.zeros((n,n))
#for i in range(n):
#	k[i] = np.linspace(0.055, 0.065, n)
Z = np.zeros((n+2,n+2), [('U', np.double), ('V', np.double)])
U,V = Z['U'], Z['V']
u,v = U[1:-1,1:-1], V[1:-1,1:-1]

r = 20
u[...] = 1.0
U[n//2-r:n//2+r,n//2-r:n//2+r] = 0.50
V[n//2-r:n//2+r,n//2-r:n//2+r] = 0.25
u += 0.05*np.random.random((n,n))
v += 0.05*np.random.random((n,n))
X=u


def iterate(X):
    global u,v
    if not pause:
        X1 = np.random.randint(0,2,(n, n))
        for i in range(50):
            Lu = (U[0:-2,1:-1] +U[1:-1,0:-2] - 4*U[1:-1,1:-1] + U[1:-1,2:] + U[2:  ,1:-1] )
            Lv = (V[0:-2,1:-1] +V[1:-1,0:-2] - 4*V[1:-1,1:-1] + V[1:-1,2:] + V[2:  ,1:-1] )
            uvv = u*v*v
            u += (Du*Lu - uvv +  F   *(1-u))
            v += (Dv*Lv + uvv - (F+k)*v    )

        X1=u
        return X1


#
# do not change below
#
pause = False

def onClick(event):
    global pause
    pause ^= True



fig = plt.figure(figsize=(25/3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(X, cmap=plt.cm.jet)

# The animation function: called to produce a frame for each generation.
def animate(i):
    im.set_data(animate.X)
    animate.X = iterate(animate.X)
# Bind our grid to the identifier X in the animate function's namespace.
animate.X = X

# Interval between frames (ms).
interval = 100
fig.canvas.mpl_connect('button_press_event', onClick)
anim = animation.FuncAnimation(fig, animate, interval=interval)
plt.show()

if save_video:
	anim.save(video_fname, writer="ffmpeg")
