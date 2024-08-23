import os

class Dataset:

    def __init__ (self, dataset_path, images_folder_name, labels_folder_name):
        self.dataset_path = dataset_path
        self.images = os.path.join(dataset_path, images_folder_name)
        self.labels = os.path.join(dataset_path, labels_folder_name)
    
    def preprocess(self):
        '''
        '''
        
