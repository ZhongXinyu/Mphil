import cv2
import numpy as np
import matplotlib as mpl
mpl.use('Agg',warn=False, force=True)
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import statistics
import scipy as sc
import scipy.signal
from scipy.fftpack import fft
from PIL import Image
import io
 
 
 
 
# ************************************************ Initilise stuff ************************************************
# set file names, open video and load first frame
filein = 'Data/Clean.mp4'
fileout = 'Data/test-out.mp4'

cap = cv2.VideoCapture(filein)
if not cap.isOpened():
    print("Could not open video")
    sys.exit()

#  Skip first few frames, hack for videos with bad starts
skip = 50

# get video data
numframes = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)
cap.set(cv2.CAP_PROP_POS_FRAMES,skip)

# read first frame
ok, frame = cap.read()
if not ok:
    print('Cannot read video file')
    sys.exit()
    
# get frame size
ymax = np.shape(frame)[0]
xmax = np.shape(frame)[1]

# reduce frame size by factor 2
xsize_sml = int(xmax/2)
ysize_sml = int(ymax/2)

# set smoothing scale for savgol_filter MUST BE EVEN
smooth = 6
 
# ************************************************ Find initial circle ************************************************
# Find initial circle
# Need additions to check circle moves during the video using template matching at different times
# Also need to make checks that circle is in the frame so template is whole
grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
circles = cv2.HoughCircles(grey,cv2.HOUGH_GRADIENT,1,100,param1=100,param2=40,minRadius=60,maxRadius=180)
x = circles[0,0,0]
y = circles[0,0,1]
r = circles[0,0,2]
radii = r 

hsv_old = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# Produce image for user to check circle found
cv2.circle(frame, (circles[0,0,0], circles[0,0,1]), circles[0,0,2], (0, 255, 0), 4)
frame2 = cv2.resize(frame,(xsize_sml,ysize_sml))
cv2.imshow('Frame Test',frame2)

# set first bar position
bar = [[x,y,r,1]]
minrad = int(r-5)
maxrad = int(r+5)

# Get colour limits for masking
template = frame[int(y-r):int(y+r),int(x-r):int(x+r)]      
blurred = cv2.GaussianBlur(template, (11, 11), 0)
hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

# get disk colour
size = np.shape(template)[0]
masktmp = np.zeros(template.shape[:2], dtype=np.uint8)

colour_flag = False

r1 = (0.8*r)**2
r2 = (0.1*r)**2
center = size/2.0
for i in range(0,size):
    for j in range(0,size):
        rpt = (i-center)**2 + (j-center)**2
        if (rpt>r2 and rpt<r1):
            masktmp[i][j] = 255
            
colour, stdev = cv2.meanStdDev(hsv,mask=masktmp)
h1 = colour[0]-2*stdev[0]
h2 = colour[0]+2*stdev[0]

s1 = max(colour[1]-2*stdev[1],0)
v1 = max(colour[2]-2*stdev[2],0)
s2 = min(colour[1]+2*stdev[1],255)
v2 = min(colour[2]+2*stdev[2],255)

if stdev[0]>=44.75:
    h1=0
    h2=179

# checks for hues that wrap around 0 or 180
if h1<0:
    colour_flag = True
    colour2_min = np.array([h1+179, s1, v1],np.uint8)
    colour2_max = np.array([179, s2, v2],np.uint8)
    h1 = 0
    
if h2<179:
    colour_flag = True
    colour2_min = np.array([0, s1, v1],np.uint8)
    colour2_max = np.array([h1-179, s2, v2],np.uint8)
    h2 = 179
    
#create colour limits for inRange command
colour_min = np.array([h1, s1, v1],np.uint8)
colour_max = np.array([h2, s2, v2],np.uint8)
if colour_min[0]>colour_max[0]:
    colour_min = np.array([h2, s1, v1],np.uint8)
    colour_max = np.array([h1, s2, v2],np.uint8)

# ************************************************ Loop over video to track bar position ************************************************
#count = 0
#colour2_min = np.array([0, , 0],np.uint8)
#colour2_max = np.array([179, , 255],np.uint8)

while True:
    # Read a new frame
    ok, frame = cap.read()
    if not ok:
        break
    
#    Add code to remove stationary regions? This should help end issues with similar background colours. Need to build a template for the background to compare against
#    while (count<30):
#        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#        test = hsv-hsv_old
#
#        count = count+1


    # Set initial box for colour matching
    boxtmp_x1 = max(int(x-1.2*r),0)
    boxtmp_x2 = min(int(x+1.2*r),xmax)
    boxtmp_y1 = max(int(y-3*r),0)
    boxtmp_y2 = min(int(y+3*r),ymax)

    xmaxtmp = boxtmp_x2 - boxtmp_x1 
    ymaxtmp = boxtmp_y2 - boxtmp_y1
    
    # process partial image to obtain mask
    blurred = cv2.GaussianBlur(frame[boxtmp_y1:boxtmp_y2,boxtmp_x1:boxtmp_x2], (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, colour_min, colour_max)
    if(colour_flag):
        mask2 = cv2.inRange(hsv, colour2_min, colour2_max)
        mask = cv2.bitwise_or(mask, mask2)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)



    # Find largest contour in mask 
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[1]
    if len(cnts) > 0:
        # If contour exists then calculate smallest enclosing circle
        c = max(cnts, key=cv2.contourArea)
        ((x, y), r) = cv2.minEnclosingCircle(c)
        
        # quick check incase we only picked up part of it
        if r <radii:
            r = radii
            
        # set small box for circle finder
        box_x1 = max(int(x-1.1*r),0)
        box_x2 = min(int(x+1.1*r),xmaxtmp)
        box_y1 = max(int(y-1.1*r),0)
        box_y2 = min(int(y+1.1*r),ymaxtmp)

        # Find circle to get accurate centre and radius
        grey = cv2.cvtColor(blurred[box_y1:box_y2,box_x1:box_x2], cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(grey,cv2.HOUGH_GRADIENT,1,100,param1=100,param2=10,minRadius=minrad,maxRadius=maxrad)
        if circles is not None:
            # if found add to bar which tracks the bar position and flag as success
            x = circles[0,0,0]+box_x1+boxtmp_x1
            y = circles[0,0,1]+box_y1+boxtmp_y1
            r = circles[0,0,2]
            bar.append([x,y,r,1])
            
            # draw the circle for debugging
            cv2.circle(frame, (int(x), int(y)), int(r), (255,0,0), 4)
        else:
            # add position from contour and flag as failed 
            x = x+boxtmp_x1
            y = y+boxtmp_y1
            bar.append([x,y,r,0])
    else:
        # add previous position and flag as failed 
        bar.append([x,y,r,0])
    
    # resize and show to check what is going on
    frame = cv2.resize(frame,(xsize_sml,ysize_sml))
    cv2.imshow('frame',frame)
    
    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break
 
# ************************************************ remove glitches ************************************************
# Does moving average to remove frames where we pick up a one or two circles in a section with lots of failures
# These sections have a high number of glitches
test = []
for item in bar:
    test.append(item[3])  
test = np.convolve(test, np.ones((int(fps/2),))/(fps/2), mode='same')

for i in range(int(fps/2),np.shape(bar)[0]):
    if(test[i]<0.8):
        bar[i][3] = 0
        
# ************************************************ smooth data and find speed and acc ************************************************

# convert bar poition to meters
sizes = [bar[0][3]]
for item in bar:
    if item[3]==1:
        sizes.append(item[2])
radii = statistics.median(sizes)
print(radii)
vpos = []
hpos = []
time = []
barpos = []
count = 1
timecount = 0
for item in bar:
    #check if point was successful
    if item[3]==1:
        # this is a little loop to interpolate over sections where the bar was lost, from last known position to now
        if count>1:
            x1=(item[0]-x)/count
            y1=(item[1]-y)/count
            for n in range(1,count-1):
                barpos.append([x1*n+x,y+y1*n])
                hpos.append(0.225*(x1*n+x)/radii)
                vpos.append(0.225*(ymax-(y+y1*n))/radii)
                time.append(timecount/fps)
                timecount+=1
        x=item[0]
        y=item[1]
        barpos.append([x,y])
        hpos.append(0.225*(x)/radii)
        vpos.append(0.225*(ymax-y)/radii)
        time.append(timecount/fps)
        timecount+=1
        count=1
    else:
        count+=1

np.savetxt('Data1.txt',vpos)

# smooth position
barpos = sc.signal.savgol_filter(barpos, smooth+1, 3, axis=0)
barpos = barpos.astype(np.int32)
barpos = barpos.reshape((1,-1,2))
vpos2 = sc.signal.savgol_filter(vpos, 2*smooth+1, 3)
hpos2 = sc.signal.savgol_filter(hpos, 2*smooth+1, 3)

# calculate speed
vspeed = [0]
hspeed = [0]
for i in range(1,np.shape(vpos)[0]-1):
    vspeed.append(fps*(vpos2[i+1] - vpos2[i-1])/2)
    hspeed.append(fps*(hpos2[i+1] - hpos2[i-1])/2)
vspeed.append(0)
hspeed.append(0)

# smooth speed
vspeed2 = sc.signal.savgol_filter(vspeed, 2*smooth+1, 3)
hspeed2 = sc.signal.savgol_filter(hspeed, 2*smooth+1, 3)

# calculate acceleration
vacc = [0]
hacc = [0]
for i in range(1,np.shape(vspeed)[0]-1):
    vacc.append(fps*(vspeed2[i+1] - vspeed2[i-1])/2)
    hacc.append(fps*(hspeed2[i+1] - hspeed2[i-1])/2)
vacc.append(0)
hacc.append(0)

# smooth acceleration
vacc2 = sc.signal.savgol_filter(vacc, 2*smooth+1, 3)
hacc2 = sc.signal.savgol_filter(hacc, 2*smooth+1, 3)



# ************************************************ find max/min ************************************************

# remove sections where the bar doesn't move much
start=0
while (np.abs(vspeed2[start])<0.05):
    start+=1
end = np.shape(vspeed2)[0]-1
while (np.abs(vspeed2[end])<0.05):
    end = end-1

# do a Fourier analysis for find an approximate number of reps
vfreq = sc.fft(vpos2[start:end])
maxfreq = np.argmax(np.abs(vfreq[1:30]))+1
npts = np.shape(vpos2[start:end])[0]
# set length to search over for max an min, too large and we lose reps, too small and we get multiple false max and min
period = int(0.35*npts/maxfreq)

vmax = []
vmin = []
# add first point to both max and min
vmax.append([start,vpos2[start]])
vmin.append([start,vpos2[start]])

# search first section and add max and min
n1 = np.argmax(vpos2[start:start+2*period])
n2 = np.argmin(vpos2[start:start+2*period])
n3 = n1+start
n4 = n2+start
if (n1!=0 and n1!=2*period-1):
    vmax.append([n3,vpos2[n3]])
if (n2!=0 and n2!=2*period-1):
    vmin.append([n4,vpos2[n4]])
    
# loop over entire range to add max and min
for i in range(2*period+start,end-period,period):

    n1 = np.argmax(vpos2[i-period:i+period])
    n2 = np.argmin(vpos2[i-period:i+period])

    n3 = n1+i-period
    n4 = n2+i-period
    if (n1!=0 and n1!=2*period-1 and n3!= vmax[-1][0]):
        vmax.append([n3,vpos2[n3]])

    if (n2!=0 and n2!=2*period-1 and n4!= vmin[-1][0]):
        vmin.append([n4,vpos2[n4]])

# add max and min for last section
n1 = np.argmax(vpos2[end-2*period:end])
n2 = np.argmin(vpos2[end-2*period:end])
n3 = n1+end-2*period
n4 = n2+end-2*period
if (n1!=0 and n3!= vmax[-1][0]):
    vmax.append([n3,vpos2[n3]])

if (n2!=0 and n4!= vmin[-1][0]):
    vmin.append([n4,vpos2[n4]])

# add last point to both max and min
n3 = npts-1+start
n4 = n3
if (n1!=0 and n3!= vmax[-1][0]):
    vmax.append([n3,vpos2[n3]])

if (n2!=0 and n4!= vmin[-1][0]):
    vmin.append([n4,vpos2[n4]])



vmax = np.array(vmax)
vmin = np.array(vmin)

# check endpoints and remove either max or min
if(vmax[1][0]<vmin[1][0]):
    vmax = np.delete(vmax,0,0)
else:
    vmin = np.delete(vmin,0,0)
    
if(vmax[-2][0]>vmin[-2][0]):
    vmax = np.delete(vmax,-1,0)
else:
    vmin = np.delete(vmin,-1,0)

# remove doubles maxs or double mins
for i, imax in enumerate(vmax[:-1]):
    minlist = []
    for j, jmin in enumerate(vmin):
        if(jmin[0]>imax[0] and jmin[0]<vmax[i+1][0]):
            minlist.append([j,jmin[1]])
    minlist = np.array(minlist)
    if (np.shape(minlist)[0]>1):
        n = minlist[np.argmin(minlist[:,1])][0]
        for pt in minlist:
            if(pt[0]!=n):
                vmin = np.delete(vmin,int(pt[0]),0)
                
for i, imin in enumerate(vmin[:-1]):
    maxlist = []
    for j, jmax in enumerate(vmax):
        if(jmax[0]>imin[0] and jmax[0]<vmin[i+1][0]):
            maxlist.append([j,jmax[1]])
    maxlist = np.array(maxlist)
    if (np.shape(maxlist)[0]>1):
        n = maxlist[np.argmax(maxlist[:,1])][0]
        for pt in maxlist:
            if(pt[0]!=n):
                vmax = np.delete(vmax,int(pt[0]),0)

# find median max amd mins
medvmax = statistics.median(vmax[:,1])
medvmin = statistics.median(vmin[:,1])
print(medvmax,medvmin)

# remove fake max and mins by checking if they are closer to the average max or average min
dist = 0.5*(medvmax + medvmin)
i=0
while(i<np.shape(vmax)[1]):
    if(vmax[i][1]<dist):
        vmax = np.delete(vmax,i,0)
    else:
        i = i+1

i=0
while(i<np.shape(vmin)[1]):
    if(vmin[i][1]>dist):
        vmin = np.delete(vmin,i,0)
    else:
        i = i+1

# remove doubles again so the must alternate max-min-max-min...
for i, imax in enumerate(vmax[:-1]):
    minlist = []
    for j, jmin in enumerate(vmin):
        if(jmin[0]>imax[0] and jmin[0]<vmax[i+1][0]):
            minlist.append([j,jmin[1]])
    minlist = np.array(minlist)
    if (np.shape(minlist)[0]>1):
        n = minlist[np.argmin(minlist[:,1])][0]
        for pt in minlist:
            if(pt[0]!=n):
                vmin = np.delete(vmin,int(pt[0]),0)
                
for i, imin in enumerate(vmin[:-1]):
    maxlist = []
    for j, jmax in enumerate(vmax):
        if(jmax[0]>imin[0] and jmax[0]<vmin[i+1][0]):
            maxlist.append([j,jmax[1]])
    maxlist = np.array(maxlist)
    if (np.shape(maxlist)[0]>1):
        n = maxlist[np.argmax(maxlist[:,1])][0]
        for pt in maxlist:
            if(pt[0]!=n):
                vmax = np.delete(vmax,int(pt[0]),0)
                 
# ************************************************ find reps ************************************************
 
# # Grab reps
reps = []
# add reps as either: squat type, max-min-max; or deadlift type, min-max-min
if(vmax[0][0] < vmin[0][0]):
     SquatType = True
     for i, item in enumerate(vmax[:-1]):
         reps.append([vmax[i][0],vmin[i][0],vmax[i+1][0]])

else:
     SquatType = False
     for i, item in enumerate(vmin[:-1]):
         reps.append([vmin[i][0],vmax[i][0],vmin[i+1][0]])
             
# trim reps ends to remove space between reps
for place, item in enumerate(reps):
    i=int(item[0])
    while (np.abs(vspeed2[i])<0.1):
        i+=1
    j = int(item[2])
    while (np.abs(vspeed2[j])<0.1):
        j = j-1
    item[0] = i
    item[2] = j
    reps[place] = item

# create plot of full data with min and max plotted on this is mostly for debugging
w, h = plt.figaspect(ymax/xmax)
fig = plt.figure('Sequence',figsize=(w,h))
plt.subplot(311)
plt.plot(time[start:end],vpos2[start:end])
for i in vmax[:,0]:
    plt.axvline(x=time[int(i)],color='r')
for i in vmin[:,0]:
    plt.axvline(x=time[int(i)],color='g')
plt.minorticks_on()
plt.title('Height')
plt.grid(True)

plt.subplot(312)
plt.plot(time[start:end],vspeed2[start:end])
for i in vmax[:,0]:
    plt.axvline(x=time[int(i)],color='r')
for i in vmin[:,0]:
    plt.axvline(x=time[int(i)],color='g')
plt.minorticks_on()
plt.title('Speed')
plt.grid(True) 

plt.subplot(313)
plt.plot(time[start:end],vacc2[start:end])
for i in vmax[:,0]:
    plt.axvline(x=time[int(i)],color='r')
for i in vmin[:,0]:
    plt.axvline(x=time[int(i)],color='g')

plt.minorticks_on()
plt.title('Acceleration')
plt.grid(True) 
fig.tight_layout()  
# plt.show()

# take plot and convert to image
fig.canvas.draw()
buf = fig.canvas.tostring_rgb()
ncols, nrows = fig.canvas.get_width_height()
seq = np.frombuffer(buf, dtype=np.uint8).reshape(nrows, ncols, 3)
seq = cv2.cvtColor(seq, cv2.COLOR_RGB2BGR)
seq = cv2.resize(seq,(xmax,ymax))
# cv2.imshow("Sequence", seq)
plt.close()


# Now plot create plot with reps stacked on top of each other
fig = plt.figure(figsize=(w,h))
plt.subplot(311)
for place, item in enumerate(reps):
    linelabel = "Rep #{0}".format(place+1)
    plt.plot([x-time[int(item[1])] for x in time[int(item[0]):int(item[2])]], vpos2[int(item[0]):int(item[2])], label=linelabel)
plt.minorticks_on()
plt.legend()
plt.title('Height (m)')
plt.grid(True)

plt.subplot(312)
for place, item in enumerate(reps):
    plt.plot([x-time[int(item[1])] for x in time[int(item[0]):int(item[2])]], vspeed2[int(item[0]):int(item[2])])
plt.minorticks_on()
plt.title('Speed (m/s)')
plt.grid(True)

plt.subplot(313)
for place, item in enumerate(reps):
    plt.plot([x-time[int(item[1])] for x in time[int(item[0]):int(item[2])]], vacc2[int(item[0]):int(item[2])])
plt.minorticks_on()
plt.title('Acceleration (m/s/s)')
plt.grid(True)

fig.tight_layout()
# plt.show()

# Again take plot and convert to image
fig.canvas.draw()
buf = fig.canvas.tostring_rgb()
ncols, nrows = fig.canvas.get_width_height()
over = np.frombuffer(buf, dtype=np.uint8).reshape(nrows, ncols, 3)
over = cv2.cvtColor(over, cv2.COLOR_RGB2BGR)
over = cv2.resize(over,(xmax,ymax))
# cv2.imshow("Overlay", over)
plt.close()

#should add plot for stacked bar paths

# join plots together to make a single frame resized to half the video
seq = cv2.resize(seq,(xsize_sml,ysize_sml))
over = cv2.resize(over,(xsize_sml,ysize_sml))

final = np.concatenate((seq, over), axis=1)
# cv2.imshow("LastFrame", final)

# Reset counter for video to start of first rep *now replaced*
# framenum = int(reps[0][0])
# cap.set(cv2.CAP_PROP_POS_FRAMES,framenum+skip)
# rep = 0

# Initilise video writer to output video we create
size = final.shape[1], final.shape[0]
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(fileout,fourcc,fps,size)

# Create data objects for plots of individual reps
data_x = []
data_v = []
data_s = []
data_a = []
for item in reps:
    data_x.append(list(x-time[int(item[1])] for x in time[int(item[0]):int(item[2])]))
    data_v.append(vpos2[int(item[0]):int(item[2])])
    data_s.append(vspeed2[int(item[0]):int(item[2])])
    data_a.append(vacc2[int(item[0]):int(item[2])])

# create inital plot with lines in pale red (C3) and fake line we can update later
# fig = plt.figure(figsize=(w,h))
#
# plt.subplot(311)
# plt.plot(data_x[0],data_v[0],'C3', alpha=0.5)
# line_v, = plt.plot(data_x[0][0],data_v[0][0],'C3')
# plt.minorticks_on()
# plt.title('Height')
# plt.grid(True)
#
# plt.subplot(312)
# plt.plot(data_x[0],data_s[0],'C3', alpha=0.5)
# line_s, = plt.plot(data_x[0][0],data_s[0][0],'C3')
# plt.minorticks_on()
# plt.title('Speed')
# plt.grid(True)
#
# plt.subplot(313)
# plt.plot(data_x[0],data_a[0],'C3', alpha=0.5)
# line_a, = plt.plot(data_x[0][0],data_a[0][0],'C3')
# plt.minorticks_on()
# plt.title('Acceleration')
# plt.grid(True)
#
# fig.tight_layout()

# Calculate distance mover and ave and max speed and acceleration for each rep
distance = []
speedmax = []
speedave = []
accmax = []
accave = []
if SquatType:
    for item in reps:
        distance.append(vpos2[int(item[2])] - vpos2[int(item[1])])
        speedmax.append(np.amax(vspeed2[int(item[1]):int(item[2])]))
        speedave.append(np.mean(vspeed2[int(item[1]):int(item[2])]))
        accmax.append(np.amax(vacc2[int(item[1]):int(item[2])]))
        accave.append(np.mean(vacc2[int(item[1]):int(item[2])]))
else:
    for item in reps:
        distance.append(vpos2[int(item[1])] - vpos2[int(item[0])])
        speedmax.append(np.amax(vspeed2[int(item[0]):int(item[1])]))
        speedave.append(np.mean(vspeed2[int(item[0]):int(item[1])]))
        accmax.append(np.amax(vacc2[int(item[0]):int(item[1])]))
        accave.append(np.mean(vacc2[int(item[0]):int(item[1])]))

# loop over reps to create video of each one
for place, item in enumerate(reps):
    # set begining frame
    start = int(item[0])
    end = int(item[2])+1
    cap.set(cv2.CAP_PROP_POS_FRAMES,start+skip)

    #close existing figures
    plt.close(fig)
    
    # create inital plot with lines in pale red (C3) and fake line we can update later
    fig = plt.figure(figsize=(w,h))
    
    plt.subplot(311)
    plt.plot(data_x[place],data_v[place],'C3', alpha=0.5)
    line_v, = plt.plot(data_x[place][0],data_v[place][0],'C3')
    plt.minorticks_on()
    plt.title('Height (m)')
    plt.grid(True)

    plt.subplot(312)
    plt.plot(data_x[place],data_s[place],'C3', alpha=0.5)
    line_s, = plt.plot(data_x[place][0],data_s[place][0],'C3')
    plt.minorticks_on()
    plt.title('Speed (m/s)')
    plt.grid(True)

    plt.subplot(313)
    plt.plot(data_x[place],data_a[place],'C3', alpha=0.5)
    line_a, = plt.plot(data_x[place][0],data_a[place][0],'C3')
    plt.minorticks_on()
    plt.title('Acceleration (m/s/s)')
    plt.grid(True)

    fig.tight_layout()
    
    for i in range(start,end):
        # Load frame
        ok, frame = cap.read()
        if not ok:
            break

        # Plot Bar path
        cv2.polylines(frame,barpos[:,start:i],False,(0,0,255),thickness=5)
        # Display Rep number and rep summary data on frame
        cv2.putText(frame, 'Rep # {}'.format(place+1), (50,100), cv2.FONT_HERSHEY_SIMPLEX, 3.0, (0,0,255), 5);
        cv2.putText(frame, 'Distance:  {:.2f}'.format(distance[place]), (50,150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 2);
        cv2.putText(frame, 'Peak Speed: {:.2f}'.format(speedmax[place]), (50,200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 2);
        cv2.putText(frame, 'Ave Speed:  {:.2f}'.format(speedave[place]), (50,250), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 2);
        cv2.putText(frame, 'Peak Accl:  {:.2f}'.format(accmax[place]), (50,300), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 2);
        cv2.putText(frame, 'Ave Accl:   {:.2f}'.format(accave[place]), (50,350), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 2);

        # Update plots with bold red line up to where we are now
        n = int(i-start)
        line_v.set_xdata(data_x[place][0:n])
        line_v.set_ydata(data_v[place][0:n])
        line_s.set_xdata(data_x[place][0:n])
        line_s.set_ydata(data_s[place][0:n])
        line_a.set_xdata(data_x[place][0:n])
        line_a.set_ydata(data_a[place][0:n])
        
        # convert plot to image to append to video
        plt.draw()
        fig.canvas.draw()
        buf = fig.canvas.tostring_rgb()
        ncols, nrows = fig.canvas.get_width_height()
        plots = np.frombuffer(buf, dtype=np.uint8).reshape(nrows, ncols, 3)
        plots = cv2.cvtColor(plots, cv2.COLOR_RGB2BGR)
        
        # resize
        plots = cv2.resize(plots,(xsize_sml,ysize_sml))
        frame = cv2.resize(frame,(xsize_sml,ysize_sml))
        
        # append fram and plots
        frame2 = np.concatenate((plots, frame), axis=1)
        
        # show frame and write to file
        cv2.imshow("Output", frame2)
        video.write(frame2)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break

# close plots
plt.close(fig)
# release initial video
cv2.VideoCapture.release(cap)
# Add summary slide at end for 4 seconds
for i in range(0,int(4*fps)):
    video.write(final)
# cleanup then exit
cv2.destroyAllWindows()
video.release()
