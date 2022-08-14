import sys, re, os, shutil, socket, glob
from UserDict import UserDict

userinput = raw_input("\nAre you sure you want to delete content of input data and run directories? Y/N(default) ")

userinput = userinput.strip()
userinput = userinput.lower()

if userinput == "y" or userinput == "yes":

    initial_path = os.getcwd()
    input_data_path = initial_path + '/input_data' 

    ligand_randomconf_dir = 'gen_ligand_start_confs_rndm'

    if not os.path.exists(input_data_path):
        print '\nThe directory %s not foumd!' %input_data_path
        sys.exit()
    else:
        os.chdir(input_data_path)
        os.system('rm -rf *')
        os.chdir('../')

    if not os.path.exists(ligand_randomconf_dir):
        print '\nThe directory %s not foumd!' %ligand_randomconf_dir
        sys.exit()
    else:
        os.chdir(ligand_randomconf_dir)
        os.system('rm -rf *')
        os.chdir('../')
