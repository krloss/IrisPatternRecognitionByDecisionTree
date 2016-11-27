import irisExtraction as ie

from matplotlib import pyplot
from scipy import ndimage
from sklearn import tree
from sklearn import metrics
from sklearn import cross_validation

def irisValidation(dataset,test_size=0.4):
	targets = map(lambda x: dataset['targets'][x], dataset['names'])
	return cross_validation.train_test_split(dataset['data'],targets,test_size=test_size,random_state=0)

def classifyIris(dataset):
	train,test,trainTarget,testTarget = irisValidation(dataset)
	classifier = tree.DecisionTreeClassifier()

	classifier.fit(train,trainTarget)
	prediction = classifier.predict(test)
	print metrics.accuracy_score(testTarget,prediction)
	print metrics.confusion_matrix(testTarget,prediction)

for i in range(1,225):
	for j in range(1,11):
		clazz = '%03d' % i
		fileName = 'img/' + clazz + '/%02d.bmp' % j
		#clazz += 'E' if j < 6 else 'D'
		print clazz,fileName
		source = ndimage.imread(fileName,flatten=True)
		ie.extractIris(clazz,fileName,source)

classifyIris(ie.irisDataset)
