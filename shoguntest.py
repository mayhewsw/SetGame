# In this example a two-class support vector machine classifier is trained on a
# 2-dimensional randomly generated data set and the trained classifier is used to
# predict labels of test examples. As training algorithm the LIBSVM solver is used
# with SVM regularization parameter C=1 and a Gaussian kernel of width 2.1.
# 
# For more details on LIBSVM solver see http://www.csie.ntu.edu.tw/~cjlin/libsvm/

# In this example a multi-class support vector machine classifier is trained on a
# toy data set and the trained classifier is used to predict labels of test
# examples. As training algorithm the LIBSVM solver is used with SVM
# regularization parameter C=1 and a Gaussian kernel of width 2.1 and the
# precision parameter epsilon=1e-5. 
# 
# For more details on LIBSVM solver see http://www.csie.ntu.edu.tw/~cjlin/libsvm/
import processCards
import cv

def libsvm_multiclass ():
	print 'LibSVMMultiClass'

	from shogun.Features import RealFeatures, Labels
	from shogun.Kernel import GaussianKernel
	from shogun.Classifier import LibSVMMultiClass

	feats_train=RealFeatures(fm_train_real)
	feats_test=RealFeatures(fm_test_real)
	width=2.1
	kernel=GaussianKernel(feats_train, feats_train, width)

	C=1
	epsilon=1e-5
	labels=Labels(label_train_multiclass)

	svm=LibSVMMultiClass(C, kernel, labels)
	svm.set_epsilon(epsilon)
	svm.train()

	#kernel.init(feats_train, feats_test)
        # WE can pass classify the test features also
        # The get_labels function is for if we want to process
        # the data in Python
	out = svm.classify(feats_test).get_labels()
        print out

def getFeatureVectorFromImage(img):
    '''
    img is a filename for a set board image. This will extract cards, and generate features
    '''
    groups = processCards.extractCards(trainimg)

    # Let's just do color.
    #Hmm. How to get the correct feature matrix?
    # Look up the Sunset detector paper.
    


if __name__=='__main__':
	#from tools.load import LoadMatrix
	#lm=LoadMatrix()
	#fm_train_real=lm.load_numbers('/home/stephen/Documents/shogun-data-0.1/toy/fm_train_real.dat')
	#fm_test_real=lm.load_numbers('/home/stephen/Documents/shogun-data-0.1/toy/fm_test_real.dat')
        #print fm_train_real
	#label_train_multiclass=lm.load_labels('/home/stephen/Documents/shogun-data-0.1/toy/label_train_multiclass.dat')
	trainImg = cv.LoadImage('images/lamp1.jpg')
	testImg = cv.LoadImage('images/lamp1_rotate.jpg')
	
	trainv = getFeatureVectorFromImage(trainImg)
	testv = getFeatureVectorFromImage(testImg)
	libsvm_multiclass(trainv, testv)
