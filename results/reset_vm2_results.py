import sys, re, os, shutil, socket, glob
from UserDict import UserDict

userinput = raw_input("\nAre you sure you want to delete csv files containing run results and summaries? Y/N(default) ")

userinput = userinput.strip()
userinput = userinput.lower()

if userinput == "y" or userinput == "yes":

    filenames_to_delete = glob.glob('*vm2_rndm_*csv')

    if len(filenames_to_delete) > 0:
        print 'Deleting files %s' %filenames_to_delete

        for filename in filenames_to_delete:
            if os.path.exists(filename):
                os.remove(filename)

    filenames_to_delete = glob.glob('*vm2_single_*csv')

    if len(filenames_to_delete) > 0:
        print 'Deleting files %s' %filenames_to_delete

        for filename in filenames_to_delete:
            if os.path.exists(filename):
                os.remove(filename)

    filenames_to_delete = glob.glob('*vm2_snap_*csv')

    if len(filenames_to_delete) > 0:
        print 'Deleting files %s' %filenames_to_delete

        for filename in filenames_to_delete:
            if os.path.exists(filename):
                os.remove(filename)


userinput = raw_input("\nAre you sure you want to delete all conformer files e.g. sdf, mol2 etc.? Y/N(default) ")

userinput = userinput.strip()
userinput = userinput.lower()

if userinput == "y" or userinput == "yes":

    initial_path = os.getcwd()

    if os.path.exists('conformers'):

        os.chdir('conformers')

        if os.path.exists('fast_vm2_rndm'):
            os.system('rm -rf fast_vm2_rndm')

        if os.path.exists('fast_vm2_single'):
            os.system('rm -rf fast_vm2_single')

        if os.path.exists('fast_vm2_snap'):
            os.system('rm -rf fast_vm2_snap')

        if os.path.exists('vm2_rndm'):
            os.system('rm -rf vm2_rndm')

        if os.path.exists('vm2_single'):
            os.system('rm -rf vm2_single')

        if os.path.exists('vm2_snap'):
            os.system('rm -rf vm2_snap')
