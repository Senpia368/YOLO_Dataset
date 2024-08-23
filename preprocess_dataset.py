import os

class Dataset:

    def __init__ (self, dataset_path, images_folder_name, labels_folder_name):
        self.dataset_path = dataset_path
        self.images = os.path.join(dataset_path, images_folder_name)
        self.labels = os.path.join(dataset_path, labels_folder_name)
    
    def preprocess(self, object_id):
        '''
        '''
        for folder in os.listdir(self.labels):
            label_folder_path = os.path.join(self.labels,folder)
            image_folder_path = os.path.join(self.images,folder)

            for filename in os.listdir(label_folder_path):
                file_path = os.path.join(label_folder_path, filename)
                object_labels = self.object_labels(file_path, object_id)

                if object_labels:
                    with open(file_path, 'w') as file:
                        file.writelines(object_labels)
                else:
                    image_path = os.path.join(image_folder_path, self.get_filename(filename)+'.jpg')
                    try:
                        os.remove(image_path)
                        os.remove(file_path)
                    except Exception as e:
                        print(f'An error has occured while deleting file: {e}')
    
    def object_labels(self,file_path, object_id):
        '''
        returns list of lines in text file that do contain the object_id
        '''
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        lines_to_keep = [line for line in lines if line[0] == object_id]

        return lines_to_keep

    def get_filename(self, filename):
        '''
        returns filename without extension
        '''
        return filename.split('.')[0]
    

def main():
    dataset = Dataset('mobility','images','labels')
    object_id = '2'

    dataset.preprocess(object_id)

    

if __name__ == "__main__":
    main()

