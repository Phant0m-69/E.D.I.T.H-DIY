import os
import shutil
import os.path
from tempfile import mkstemp
from shutil import move
from os import remove
import sys


#Note : This code will work only on python 3.8 +

print('Please install the requiremnts from the requiremnts folder')
#Function to replace a line with another in another line
def replace(source_file_path, pattern, substring):
    fh, target_file_path = mkstemp()
    with open(target_file_path, 'w') as target_file:
        with open(source_file_path, 'r') as source_file:
            for line in source_file:
                target_file.write(line.replace(pattern, substring))
    remove(source_file_path)
    move(target_file_path, source_file_path)

#function to execute a python file
def execfile(filename, globals=None, locals=None):
    if globals is None:
        globals = sys._getframe(1).f_globals
    if locals is None:
        locals = sys._getframe(1).f_locals
    with open(filename, "r") as fh:
        exec(fh.read()+"\n", globals, locals)

#This function is for finding path of files or folders
def path_(name_of_file_or_folder):
    name = name_of_file_or_folder #if the path just in current dir
    return(os.path.abspath(name))

print('Starting automated trainer ')
#copy paste all contents of input to the yolo input folder in data conversion
shutil.copytree(path_('input'), path_('Yolo-Training/data_converstion/main/input'), dirs_exist_ok=True)
print('Copy pasted all images into the engine folder')

#replace class_list.txt with the new class_list.txt
shutil.copyfile(path_('class_list.txt'),path_('Yolo-Training/data_converstion/main/class_list.txt'))
print('Edited the classes')

#now go to main.py in Yolo-Training/data_converstion/main/main.py and run it. Edit the images , and close main.py
os.system('python Yolo-Training/data_converstion/main/main.py')
print('Finished making boxes through GUI')

#copy paste input images and output text files into data folder
shutil.copytree(path_('input'), path_('data'), dirs_exist_ok=True)
shutil.copytree(path_('Yolo-Training/data_converstion/main/output/YOLO_darknet'),path_('data'),dirs_exist_ok=True)
print('Successfully made data folder with necessary files')

#after puuting the correct path, execute Yolo-Training/train_test_conversion/process.py , then replaces the file to its original state.
replace(path_('Yolo-Training/train_test_conversion/process.py'),"current_dir = '+++++'","current_dir = {}".format("'"+path_('data')+"'"))
os.system('python Yolo-Training/train_test_conversion/process.py')
replace(path_('Yolo-Training/train_test_conversion/process.py'),"current_dir = {}".format("'"+path_('data')+"'"),"current_dir = '+++++'")
print('Editing paths completed')
#put a correct path of file

replace(path_('Yolo-Training/anchors_calculation/anchors.py'),"default = ':::::::'","default = {}".format("'"+path_('Yolo-Training/anchors_calculation/anchors')+"'"))
replace(path_('Yolo-Training/anchors_calculation/anchors.py'),"default = '++++++'","default = {}".format("'"+path_('train.txt')+"'"))
os.system('python Yolo-Training/anchors_calculation/anchors.py')
replace(path_('Yolo-Training/anchors_calculation/anchors.py'),"default = {}".format("'"+path_('Yolo-Training/anchors_calculation/anchors')+"'"),"default = ':::::::'")
replace(path_('Yolo-Training/anchors_calculation/anchors.py'),"default = {}".format("'"+path_('train.txt')+"'"),"default = '++++++'")
print('Finished executing anchor calculator')


#copy anchor6.txt inside to the anchor6.txt outside
shutil.copyfile(path_('Yolo-Training/anchors_calculation/anchors/anchors6.txt'),path_('anchors6.txt'))
print('Saved the anchors')

#editing  the cfg file
print("Starting to edit ")
from user_input_gui import num
if num==1:
    num1=5
else:
    num1=num
num2=(num1+1)*3
with open('anchors6.txt') as f:
    first_line = f.readline()
print(first_line)

replace(path_('Yolo-Training/data_for_colab/yolov3-tiny-obj.cfg'),"anchors=?","anchors={}".format(first_line))
replace(path_('Yolo-Training/data_for_colab/yolov3-tiny-obj.cfg'),"classes=?","classes={}".format(str(num)))
replace(path_('Yolo-Training/data_for_colab/yolov3-tiny-obj.cfg'), "filters=?", "filters={}".format(str(num2)))
print('Finished changing filters , classes and anchors')
print('Completed making the cfg file ')
shutil.copyfile(path_('Yolo-Training/data_for_colab/yolov3-tiny-obj.cfg'),path_('output/yolov3-tiny-obj.cfg'))
print('Created the cfg file into output')

#copying test.txt and train.txt to data_for_colab folder
shutil.copyfile(path_('test.txt'),path_('Yolo-Training/data_for_colab/test.txt'))
shutil.copyfile(path_('train.txt'),path_('Yolo-Training/data_for_colab/train.txt'))

#Editing test.txt and train.txt in data_for_colab
replace(path_('Yolo-Training/data_for_colab/test.txt'),path_('data'),"/content/darknet/data_for_colab/data")
replace(path_('Yolo-Training/data_for_colab/train.txt'),path_('data'),"/content/darknet/data_for_colab/data")
#editing obj.names
shutil.copyfile(path_('class_list.txt'),path_('Yolo-Training/data_for_colab/obj.names'))
#editing obj.data
replace(path_('Yolo-Training/data_for_colab/obj.data'),'classes = ?','classes = {}'.format(num))
#copy paste data folder
shutil.copytree(path_('data'),path_('Yolo-Training/data_for_colab/data'),dirs_exist_ok=True)
#making zip file
shutil.make_archive(path_('output/data_for_colab'), 'zip',path_('Yolo-Training/data_for_colab') )

print("Process sucessfully finised")
print('Deleting changes')
#BAsically , this deletes all things done and makes everything look fresh as before
open("train.txt", "w").close()
open("test.txt", "w").close()
open('class_list.txt', "w").close()
open("anchors6.txt", "w").close()
shutil.rmtree('data');os.makedirs('data')
shutil.rmtree('input');os.makedirs('input')
shutil.rmtree('Yolo-Training')
shutil.unpack_archive(path_('Yolo-Training.zip'), path_(''))
print("Finished Everything. Go to output folder , unzip the file into your google drive")