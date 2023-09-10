# Dataset_Shuffler_For_YOLO
Generates datasets for cross validation with less dependency and in a easy way.

# Dependencies 
- os
- random
- copy
- shutil
- sys
- argparse

# What is this script for?
- It provides to create k different datasets that have k different validation sets from base dataset.
- It is similiar to k-fold cross validation method. But this script creates k different dataset.

![dataset_shuffler_how_it_works](https://github.com/bahadiryildirimeem/Dataset_Shuffler_For_YOLO/assets/45585791/21cf9768-2783-46c2-b484-d25b23d8427b)

# How it works?
- Script reads all of the labels that in given in the label path. 
- It accepts the first labeled class in the label file as the class of the label file. And counts number of labels for each class.
- To get validation size of each class, divides number of each class value to k value.
- Script uses "random.randint" to create k different "randomize" validation sets. 
- Saves each generated dataset to "generatedCrossValDataSet" folder as set_x.

# How to use?
-  Script gets 4 parameters.
  > -img_path=your_image_files_directory
  > -lbl_path=your_label_files_directory
  > -nof_cls=number_of_class_of_your_dataset
  > -k=number_of_dataset_that_will_be_created

Here is an example for generating 5 different dataset from helper_data_v5_2_whole file that have 5 classes: 

```python dataset_shuffler_for_yolo.py -img_path=helper_data_v5_2_whole/images -lbl_path=helper_data_v5_2_whole/labels -nof_cls=5 -k=5```

