import sys, re, os, shutil, socket, glob
from UserDict import UserDict

userinput = raw_input("\nAre you sure you want to delete contents of input data and run directories? Y/N(default) ")

userinput = userinput.strip()
userinput = userinput.lower()

if userinput == "y" or userinput == "yes":

    initial_path = os.getcwd()
    input_data_path = initial_path + '/input_data' 

    fast_vm2_rndm = 'fast_vm2_rndm'
    vm2_rndm = 'vm2_rndm'
    fast_vm2_single = 'fast_vm2_single'
    vm2_single = 'vm2_single'

    if not os.path.exists(input_data_path):
        print '\nThe directory %s not foumd!' %input_data_path
        sys.exit()
    else:
        os.chdir(input_data_path)
        if os.path.exists('ligands'):
            os.system('rm -rf ligands')
        if os.path.exists('hosts'):
            os.system('rm -rf hosts')
        if os.path.exists('ligand_rndm_confs'):
            os.system('rm -rf ligand_rndm_confs')
        os.chdir('../')

    if not os.path.exists(fast_vm2_rndm):
        print '\nThe directory %s not foumd!' %fast_vm2_rndm
        sys.exit()
    else:
        os.chdir(fast_vm2_rndm)
        if os.path.exists('complexes'):
            os.system('rm -rf complexes')
        if os.path.exists('ligands'):
            os.system('rm -rf ligands')
        if os.path.exists('hosts'):
            os.system('rm -rf hosts')
        os.chdir('../')

    if not os.path.exists(vm2_rndm):
        print '\nThe directory %s not foumd!' %vm2_rndm
        sys.exit()
    else:
        os.chdir(vm2_rndm)
        if os.path.exists('complexes'):
            os.system('rm -rf complexes')
        if os.path.exists('ligands'):
            os.system('rm -rf ligands')
        if os.path.exists('hosts'):
            os.system('rm -rf hosts')
        os.chdir('../')

    if not os.path.exists(fast_vm2_single):
        print '\nThe directory %s not foumd!' %fast_vm2_single
        sys.exit()
    else:
        os.chdir(fast_vm2_single)
        if os.path.exists('complexes'):
            os.system('rm -rf complexes')
        if os.path.exists('ligands'):
            os.system('rm -rf ligands')
        if os.path.exists('hosts'):
            os.system('rm -rf hosts')
        os.chdir('../')

    if not os.path.exists(vm2_single):
        print '\nThe directory %s not foumd!' %vm2_single
        sys.exit()
    else:
        os.chdir(vm2_single)
        if os.path.exists('complexes'):
            os.system('rm -rf complexes')
        if os.path.exists('ligands'):
            os.system('rm -rf ligands')
        if os.path.exists('hosts'):
            os.system('rm -rf hosts')
        os.chdir('../')
