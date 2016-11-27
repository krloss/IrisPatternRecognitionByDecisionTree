import numpy as np

from matplotlib import pyplot
from scipy import ndimage

# Intensidade e tamanho da pupila foram definidos empiricamente.
def findPupil(image,pupilIntensity=2,pupilSize=4200):
	binary = image < pupilIntensity
	labels,num = ndimage.label(binary)
	#print num
	#pyplot.matshow(labels)

	labels = ndimage.find_objects(labels)
	pupil = np.copy(binary)

	for i in range(0, num):
		if(pupil[labels[i]].size < pupilSize):
			pupil[labels[i]] = 0

	#pyplot.matshow(pupil)

	indices = np.argwhere(pupil)
	aMin = np.amin(indices,axis=0)
	aMed = np.median(indices,axis=0)
	aMax = np.amax(indices,axis=0)
	'''
	pupil = pupil * 1
	pupil[aMed[0],aMin[1]:aMax[1]+1] = 2
	pupil[aMin[0]:aMax[0]+1,aMed[1]] = 3
	pyplot.matshow(pupil,cmap='hot')
	'''
	return [aMin,aMed,aMax]

def getIrisLine(yCP,hBand,interval):
	hLine = np.mean(hBand[:,interval],axis=0)
	'''
	line = hBand[0,:] * 0 + yCP
	pyplot.plot(line + 0)
	line[interval] = hLine
	pyplot.plot(line)
	'''
	return hLine

def getIrisPoint(hLine,soft):
	hLine = zip(range(soft,hLine.size-soft),hLine[soft:-soft])
	point = reduce(lambda x,y: x if y[0][1]-y[1][1] < x[0][1]-x[1][1] else y, zip(hLine[1:],hLine[:-1]))
	return [point[1][0],point[0][0]] if point[1][0] < point[0][0] else [point[0][0],point[1][0]]

# Contraste e suavizacao foram definidos empiricamente
def findIris(image,pupil,contrast=1.15,soft=22):
	#print str(pupil) + '\t' + str(soft)
	yCP=pupil[1][0]; xLP=pupil[0][1]; xRP=pupil[2][1];
	hBand = image[yCP-soft:yCP+soft+1,:] * contrast
	leftLine = getIrisLine(yCP,hBand,slice(None,xLP))
	rightLine = getIrisLine(yCP,hBand,slice(xRP,None))
	leftPoint = getIrisPoint(leftLine,soft)
	rightPoint = getIrisPoint(rightLine,soft)
	rightPoint = map(lambda x: xRP + x,rightPoint)
	#print str(leftPoint) + '\t' + str(rightPoint)
	'''
	image[:,leftPoint[0]] = 255
	image[:,rightPoint[1]] = 255
	'''
	return [(leftLine,yCP,leftPoint[0]),(rightLine,yCP,rightPoint[1])]

def drawCircle(yC,xC,radius):
	y,x = np.ogrid[-radius:radius,-radius:radius]
	index = y**2 + x**2 <= radius**2
	return [slice(yC-radius,yC+radius),slice(xC-radius,xC+radius)],index

def getIrisRegion(pupil,iris,image):
	roi = np.zeros((image.shape))

	roi[pupil[0][0]:pupil[2][0],iris[0][2]:iris[1][2]] = 1
	interval,index = drawCircle(pupil[1][0],pupil[1][1],pupil[2][1]-pupil[1][1])
	roi[interval][index] = 2;
	#pyplot.matshow(roi)
	return roi

def findIrisSegmentation(image):
	try:
		pupil = findPupil(image)
		iris = findIris(image,pupil)
		return getIrisRegion(pupil,iris,image)
	except Exception as ex:
		print '\t%s' % ex
		return np.zeros((image.shape))
'''
for i in range(1,6):
	for j in range(1,11):
		fileName = "img/%(c)03d_%(f)02d.bmp" % {'c':i, 'f':j}
		print fileName
		source = ndimage.imread(fileName,flatten=True)
		pyplot.imshow(source,cmap='gray')
		roi = findIrisSegmentation(source)
		source[roi==1] = 255
		pyplot.show()
'''
