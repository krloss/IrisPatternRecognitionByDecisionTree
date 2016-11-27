import irisSegmentation as ss
import numpy as np

from matplotlib import pyplot
from scipy import ndimage
from scipy import stats
from skimage import feature

irisDataset = {'targets':{}, 'names':[], 'data':[]}

def getIrisDescriptor(image,neighbour=8,radius=3,method='uniform'): ### LBP
	lbp = feature.local_binary_pattern(image,neighbour*radius,radius,method)
	histogram = stats.itemfreq(lbp.ravel())[:,1]
	return histogram / sum(histogram)

def getSVD(image):
	U,s,V = np.linalg.svd(image)
	return s

def extractIris(clazz,name,image):
	mask = ss.findIrisSegmentation(image)
	image[mask != 1] = 0
	irisDataset['data'].append(getSVD(image))#getIrisDescriptor(image))
	irisDataset['names'].append(name)
	irisDataset['targets'][name] = clazz
'''
for i in range(1,6):
	for j in range(1,11):
		clazz = '%03d' % i
		fileName = 'img/' + clazz + '_%02d.bmp' % j
		clazz += 'E' if j < 6 else 'D'
		print clazz,fileName
		source = ndimage.imread(fileName,flatten=True)
		extractIris(clazz,fileName,source)
		
		pyplot.plot(np.mean(source,axis=0))
		pyplot.plot(np.mean(source,axis=1))
		pyplot.imshow(source,cmap='gray')
		pyplot.show()

print irisDataset
'''