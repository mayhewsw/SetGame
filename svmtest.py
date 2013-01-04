# In this example a two-class support vector machine classifier is trained on a
# toy data set and the trained classifier is used to predict labels of test
# examples. As training algorithm LIBSVM is used with SVM regularization
# parameter C=1 and a Gaussian kernel of width 1.2 and 10MB of kernel cache and 
# the precision parameter epsilon=1e-5.
# 
# For more details on LIBSVM solver see http://www.csie.ntu.edu.tw/~cjlin/libsvm/ 

def libsvm ():
	print 'LibSVM'

	size_cache=10
	width=2.1
	C=1.2
	epsilon=1e-5
	use_bias=False

	from sg import sg
	sg('set_features', 'TRAIN', fm_train_real)
	sg('set_kernel', 'GAUSSIAN', 'REAL', size_cache, width)
	sg('set_labels', 'TRAIN', label_train_twoclass)
	sg('new_classifier', 'LIBSVM')
	sg('svm_epsilon', epsilon)
	sg('c', C)
	sg('svm_use_bias', use_bias)
	sg('train_classifier')

	sg('set_features', 'TEST', fm_test_real)
	result=sg('classify')

if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_real=lm.load_numbers('../data/fm_train_real.dat')
	fm_test_real=lm.load_numbers('../data/fm_test_real.dat')
	label_train_twoclass=lm.load_labels('../data/label_train_twoclass.dat')
	libsvm()
