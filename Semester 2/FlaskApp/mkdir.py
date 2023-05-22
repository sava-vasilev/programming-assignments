import os
import encryption as encr

# Create method to check if d
def check_dir(dir_name):

    # Set main directory
    path = 'C:/Users/user/Desktop'
    os.chdir(path)

    # Assign user's username for the main folder
    directory = dir_name
    
    # Create global which type is 'list'
    global folder_dic

    # Check if the user already has a folder
    if os.path.isdir(directory):
        os.chdir(directory)

    # Id not, create the certain folders
    else:

        os.mkdir(directory)
        os.chdir(directory)

        os.mkdir('data_folder')
        os.mkdir('sync_folder')

        os.chdir("data_folder")
        if os.path.isfile("key.key"):
            data_folder = os.getcwd()
        else:
            encr.write_key()
            data_folder = os.getcwd()

        os.chdir("..")
        os.chdir("sync_folder")
        sync_folder = os.getcwd()
  
        # Save the paths of the folders into a list
        folder_dic = [data_folder, sync_folder]
