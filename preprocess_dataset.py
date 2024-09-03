import os
import shutil
from collections import defaultdict

class Dataset:

    def __init__ (self, dataset_path, images_folder_path=None, labels_folder_path=None, id_map=None):
        self.dataset_path = dataset_path
        self.images = images_folder_path
        self.labels = labels_folder_path
        if id_map:
            self.id_map = id_map
        else:
            self.id_map = {
                            '0':'2',
                            '1':'7',
                            '2':'5',
                            '3':'6',
                            '4':'0',
                            '5':'1',
                            '6':'3',
                            '7':'4'
                        }

    
    def preprocess(self, object_id):
        '''
        removes all labels and their corresponding image that do not include the object
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
    
    def yolo1_1ToYolo1(self, new_dataset_path, lastFileName=None):
        '''
        Converts Yolo 1.1 dataset format to the Yolo 1 format
        '''
        data_path = os.path.join(self.dataset_path, 'obj_train_data')
        
        train_images, train_labels = self.prepare_new_yolo_dataset(new_dataset_path)

        file_set = set()
        
        for filename in sorted(os.listdir(data_path)):
            if lastFileName == filename:
                print('Loop breaked')
                break

            file_set.add(self.get_filename(filename))

        for filename in file_set:
            for filetype in ['.jpg','.txt']:
                destination_folder = train_images if filetype == '.jpg' else train_labels
                destination_path = os.path.join(destination_folder, filename+filetype)
                file_path = os.path.join(data_path, filename+filetype)
                shutil.copy(file_path, destination_path)


    def prepare_new_yolo_dataset(self, path):
        '''
        creates folder and subfolders for a new yolo dataset
        returns paths for train directories
        '''
        os.makedirs(path, exist_ok=True)

        images_dir = os.path.join(path, 'images')
        os.makedirs(images_dir, exist_ok=True)
        self.images = images_dir

        train_images = os.path.join(images_dir, 'train')
        os.makedirs(train_images, exist_ok=True)

        labels_dir = os.path.join(path, 'labels')
        os.makedirs(labels_dir, exist_ok=True)
        self.labels = labels_dir

        train_labels = os.path.join(labels_dir, 'train')
        os.makedirs(train_labels, exist_ok=True)

        return (train_images, train_labels)
    
    def change_object_ids(self):
        '''
        changes object id values to the values they are mapped to in
        the input dictionary
        '''
        for folder in os.listdir(self.labels):
            folder_path = os.path.join(self.labels, folder)

            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)

                try:
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                except:
                    print('An error has occured while reading the file')
                for i, line in enumerate(lines):
                    new_object_id = self.id_map[line[0]]
                    lines[i] = new_object_id + line[1:]

                with open(file_path, 'w') as file:
                    file.writelines(lines)



            

    

def main():
    dataset = Dataset('task1_dataset', 'task1_dataset/images', 'task1_dataset/labels')

    
    dataset.change_object_ids()
        

if __name__ == "__main__":
    main()

