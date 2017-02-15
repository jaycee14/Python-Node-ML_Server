import pickle

#load a precomputed sci-kit learn model from a pickle file

modelFile = './models/knn_260714.pkl'

modelName ='knn_260714'


#load model
pkl_file = open(modelFile, 'rb')

model = pickle.load(pkl_file)

pkl_file.close()