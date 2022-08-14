import sys, re, os, shutil, socket
import fpformat, stat, glob
import getopt
import subprocess

def writeVm2Input(template_input_file, vm2_input_file, conf_file_name, 
                  host_base_crd, host_base_top, host_base_mol,
                  live_real_set_name, ligand_base_crd, ligand_base_top,
                  ligand_base_mol, template_ligand, pairs_map1, pairs_map2,
                  tether_file_name):

    file = open(template_input_file, 'r')
    lines = file.readlines()
    file.close()

    file = open(vm2_input_file, 'w')

    for line in lines:
        cols = line.split()
        if cols[0] == '_READINCONFS_':
            file.write('%s\n' % conf_file_name)
        elif cols[0] == '_HOSTNAMECRD_':
            file.write('%s\n' % host_base_crd)
        elif cols[0] == '_HOSTNAMETOP_':
            file.write('%s\n' % host_base_top)
        elif cols[0] == '_HOSTNAMEMOL_':
            file.write('%s\n' % host_base_mol)
        elif cols[0] == '_LIVEREALSET_':
            file.write('%s\n' % live_real_set_name)
        elif cols[0] == '_LIGNAMECRD_':
            file.write('%s.crd\n' % ligand_base_crd)
        elif cols[0] == '_LIGNAMETOP_':
            file.write('%s.top\n' % ligand_base_top)
        elif cols[0] == '_LIGNAMEMOL_':
            file.write('%s.mol\n' % ligand_base_mol)
        elif cols[0] == '_TEMPLATENAME_':
            file.write('%s\n' % template_ligand)
        elif cols[0] == '_PAIRSMAP1_':
            file.write('%s\n' % pairs_map1)
        elif cols[0] == '_PAIRSMAP2_':
            file.write('%s\n' % pairs_map2)
        elif cols[0] == '_TETHERFILENAME_':
            file.write('%s\n' % tether_file_name)
        else:
            file.write(line)

    file.close()

def parsePairMap(pair_map_file, pairs_map_list):

    file = open(pair_map_file, 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        pairs_map_list.append(line.strip())

def parseLigandKey(ligand_key_file, ligand_key_list):

    file = open(ligand_key_file, 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        ligand_key_list.append(line.strip())

#------------------------------------------------------------------------------ 
# Start of script 
#------------------------------------------------------------------------------ 

print
print '-'*80
print "Build directories for generation of ligand start conformers"
print '-'*80

initial_path = os.getcwd()
input_data_path = initial_path + '/input_data' 

ligand_confgen_path = '../1_ligand_confgen'
ligand_randomconf_dir = 'gen_ligand_start_confs_rndm'

ligand_rndm_confs = input_data_path + '/ligand_rndm_confs'

fast_vm2_rndm_path = initial_path + '/fast_vm2_rndm'
vm2_rndm_path = initial_path + '/vm2_rndm'
vm2_single_path = initial_path + '/vm2_single'
fast_vm2_single_path = initial_path + '/fast_vm2_single'

run_dirs = {}
inp_files = {}
host_inp_files = {}
conf_dirs = {}

#------------------------------------------------------------------------------ 
# Set basic defaults
#------------------------------------------------------------------------------ 

data_source_argument = None
name_trim_argument = None
start_conf_type_argument = None
template_argument = None
clear_data_argument = None
vm2_type_argument = None
ligand_key_argument = None
host_key_argument = None

data_source = 'new'
name_trim = None
do_name_trim = True

start_conf_type = 'all'
start_conf_rndm = True
start_conf_single = True

filename_template = None 

clear_data = None

vm2_type = 'all'
vm2_fast = True
vm2_regular = True

ligand_key_file = None
ligand_key_list = []

host_key_file = None
host_key_list = []

pair_map_filename = 'scaffold_mapping.txt'

#------------------------------------------------------------------------------ 
# Get commandline arguments
#------------------------------------------------------------------------------ 

argv = sys.argv[1:]

try:                                
    opts, args = getopt.getopt(argv, "hd:n:s:t:c:v:k:r:",
                 ["help","data=","nametrim=","startconfs=","template=","clear=", \
                  "vm2type=", "keyfile=", "hostkeyfile="])
                 
except getopt.GetoptError as err:
    # print help information and exit:
    print str(err)
    #usage()
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        #usage()                     
        sys.exit()                  
    elif opt in ("-d", "--data"):
       data_source_argument = arg
    elif opt in ("-n", "--nametrim"):
       name_trim_argument = arg
    elif opt in ("-s", "--startconfs"):
       start_conf_type_argument = arg
    elif opt in ("-t", "--template"):
       template_argument = arg
    elif opt in ("-c", "--clear"):
       clear_data_argument = arg
    elif opt in ("-v", "--vm2type"):
       vm2_type_argument = arg
    elif opt in ("-k", "--keyfile"):
       ligand_key_argument = arg
    elif opt in ("-r", "--hostkeyfile"):
       host_key_argument = arg

#------------------------------------------------------------------------------ 
# Set basic control variables 
#------------------------------------------------------------------------------ 

if data_source_argument is not None:

    if data_source_argument == 'reference':
       data_source = 'reference'
    elif data_source_argument == 'new':
       data_source = 'new'
    elif data_source_argument == 'reuse':
       data_source = 'reuse'
    else:
        print '\nData source argument %s is not recognized!' %data_source_argument
        print 'Choose from: reference or new'
        sys.exit()

if name_trim_argument is not None:
    if name_trim_argument == 'off':
        do_name_trim = False
        name_trim = None
    else:
        name_trim = name_trim_argument

if start_conf_type_argument is not None:

    if start_conf_type_argument == 'all':
       start_conf_type = 'all'
       start_conf_rndm = True
       start_conf_single = True
    elif start_conf_type_argument == 'random':
       start_conf_type = 'random'
       start_conf_rndm = True
       start_conf_single = False
    elif start_conf_type_argument == 'single':
       start_conf_type = 'single'
       start_conf_single = True
       start_conf_rndm = False
    else:
        print '\nStart conf type argument %s is not recognized!' %start_conf_type_argument
        print 'Choose from: all, random, and single'
        sys.exit()

if template_argument is not None:
    filename_template = template_argument
    print 'Template coordinate file name: %s' %filename_template
#elif data_source != 'reuse': 
#    print '\nA template coordinate file name (e.g. co-xtal ligand .pdb) is required!'
#    sys.exit()

if clear_data_argument is not None:

    if clear_data_argument == 'all':
        clear_data = 'all'
        if data_source == 'reuse':
            print 'Request to clear input data and reuse it!'
            sys.exit()
    elif clear_data_argument == 'input':
        clear_data = 'input'
        if data_source == 'reuse':
            print 'Request to clear input data and reuse it!'
            sys.exit()
    elif clear_data_argument == 'rundirs':
        clear_data = 'rundirs'
    else:
        print '\nClear data argument %s is not recognized!' %clear_data_argument
        print 'Choose from: all, input, or rundirs'
        sys.exit()

if vm2_type_argument is not None:

    if vm2_type_argument == 'all':
       vm2_type = 'all'
       vm2_regular = True 
       vm2_fast = True 
    elif vm2_type_argument == 'regular':
       vm2_type = 'regular'
       vm2_regular = True 
       vm2_fast = False 
    elif vm2_type_argument == 'fast':
       vm2_type = 'fast'
       vm2_regular = False
       vm2_fast = True 
    else:
        print '\nVM2 type argument %s is not recognized!' %vm2_type_argument
        print 'Choose from: all, regular, or fast'
        sys.exit()

if ligand_key_argument is not None:
    ligand_key_file = ligand_key_argument
    print 'Ligand key file name: %s' %ligand_key_file

if host_key_argument is not None:
    host_key_file = host_key_argument
    print 'Host key file name: %s' %host_key_file

#------------------------------------------------------------------------------ 
# Clear directories as requested, but stick to relevant ones only 
#------------------------------------------------------------------------------ 

if clear_data == 'all' or clear_data == 'input':

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

if clear_data == 'all' or clear_data == 'rundirs':

    if (start_conf_rndm and vm2_fast):
        if not os.path.exists(fast_vm2_rndm_path):
            print '\nThe directory %s not foumd!' %fast_vm2_rndm_path
            sys.exit()
        else:
            os.chdir(fast_vm2_rndm_path)
            if os.path.exists('complexes'):
                os.system('rm -rf complexes')
            if os.path.exists('ligands'):
                os.system('rm -rf ligands')
            if os.path.exists('hosts'):
                os.system('rm -rf hosts')
            os.chdir('../')

    if (start_conf_rndm and vm2_regular):
        if not os.path.exists(vm2_rndm_path):
            print '\nThe directory %s not foumd!' %vm2_rndm_path
            sys.exit()
        else:
            os.chdir(vm2_rndm_path)
            if os.path.exists('complexes'):
                os.system('rm -rf complexes')
            if os.path.exists('ligands'):
                os.system('rm -rf ligands')
            if os.path.exists('hosts'):
                os.system('rm -rf hosts')
            os.chdir('../')

    if (start_conf_single and vm2_fast):
        if not os.path.exists(fast_vm2_single_path):
            print '\nThe directory %s not foumd!' %fast_vm2_single_path
            sys.exit()
        else:
            os.chdir(fast_vm2_single_path)
            if os.path.exists('complexes'):
                os.system('rm -rf complexes')
            if os.path.exists('ligands'):
                os.system('rm -rf ligands')
            if os.path.exists('hosts'):
                os.system('rm -rf hosts')
            os.chdir('../')

    if (start_conf_single and vm2_regular):
        if not os.path.exists(vm2_single_path):
            print '\nThe directory %s not foumd!' %vm2_single_path
            sys.exit()
        else:
            os.chdir(vm2_single_path)
            if os.path.exists('complexes'):
                os.system('rm -rf complexes')
            if os.path.exists('ligands'):
                os.system('rm -rf ligands')
            if os.path.exists('hosts'):
                os.system('rm -rf hosts')
            os.chdir('../')

#------------------------------------------------------------------------------ 
# Populate input data directory for ligands 
#------------------------------------------------------------------------------ 

if data_source_argument != 'reuse':

    ligand_prep_dir = None

    molecule_names = []
    molecule_names_trimmed = []

    if data_source == 'reference':
        ligand_prep_dir = '../../setup/ligands/prepareLigands/reference/'
    elif data_source == 'new':
        ligand_prep_dir = '../../setup/ligands/prepareLigands/'
    else:
        print '\nNo ligand data source directory defined!'
        sys.exit()

    os.chdir(ligand_prep_dir)

    mol_filenames = glob.glob('*.mol')

    if len(mol_filenames) == 0:
        print '\nNo data found in directory %s' %ligand_prep_dir
        sys.exit()

    mol_filenames.sort()

    for filename in mol_filenames:
        print filename
        molecule_names.append(filename.split('.')[0])

    if not os.path.exists(input_data_path):
        os.mkdir(input_data_path)

    os.chdir(input_data_path)
    if not os.path.exists('ligands'):
        os.mkdir('ligands')

    os.chdir('ligands')

    if os.path.exists('template'):
        os.system('rm -rf template')

    if filename_template is not None:
        if not os.path.exists('template'):
            os.mkdir('template')
        os.chdir('template')
        print 'cp ../../../%s%s %s' % (ligand_prep_dir, filename_template, filename_template)
        os.system('cp ../../../%s%s %s' % (ligand_prep_dir, filename_template, filename_template))
        os.chdir('../')

    for filename in molecule_names:

        filename_crd = filename + '.crd'
        filename_top = filename + '.top'
        filename_mol = filename + '.mol'

        filename_trimmed = filename

        if do_name_trim:

            if name_trim:
                n1 = filename.find(name_trim)
            else:
                n1 = -1
            n2 = filename.find('_vm2')
            n3 = filename.find('_vc')

            if n1 != -1:
                filename_trimmed = filename[:n1]
            elif n2 != -1:
                filename_trimmed = filename[:n2]
            elif n3 != -1:
                filename_trimmed = filename[:n3]

        print filename_trimmed
        molecule_names_trimmed.append(filename_trimmed)

        filename_trimmed_crd = filename_trimmed + '.crd'
        filename_trimmed_top = filename_trimmed + '.top'
        filename_trimmed_mol = filename_trimmed + '.mol'

        os.system('cp ../../%s%s %s' % (ligand_prep_dir, filename_crd, filename_trimmed_crd))
        os.system('cp ../../%s%s %s' % (ligand_prep_dir, filename_top, filename_trimmed_top))
        os.system('cp ../../%s%s %s' % (ligand_prep_dir, filename_mol, filename_trimmed_mol))

    os.chdir(initial_path)

#------------------------------------------------------------------------------ 
# Populate input data directory for hosts 
#------------------------------------------------------------------------------ 

if data_source_argument != 'reuse':

    hosts_prep_dir = None

    if data_source == 'reference':
        hosts_prep_dir = '../../setup/hosts/prepareHosts/reference/'
    elif data_source == 'new':
        hosts_prep_dir = '../../setup/hosts/prepareHosts/'
    else:
        print '\nNo hosts data source directory defined!'
        sys.exit()

    os.chdir(hosts_prep_dir)

    filenames_crd = glob.glob('*.crd')
    filenames_mol = glob.glob('*.mol')
    filenames_top = glob.glob('*.top')
    filenames_tether = glob.glob('*tethered_atoms*')

    if len(filenames_crd) == 0:
        print '\nNo crd data found in directory %s' %hosts_prep_dir
        sys.exit()

    if len(filenames_mol) == 0:
        print '\nNo mol data found in directory %s' %hosts_prep_dir
        sys.exit()

    if len(filenames_top) == 0:
        print '\nNo top data found in directory %s' %hosts_prep_dir
        sys.exit()

    os.chdir(input_data_path)
    if not os.path.exists('hosts'):
        os.mkdir('hosts')

    os.chdir('hosts')

    for filename in filenames_crd:

        filename_trimmed = filename[:-4]

        if do_name_trim:

            if name_trim:
                n1 = filename.find(name_trim)
            else:
                n1 = -1
            n2 = filename.find('_vm2')
            n3 = filename.find('_vc')

            if n1 != -1:
                filename_trimmed = filename[:n1]
            elif n2 != -1:
                filename_trimmed = filename[:n2]
            elif n3 != -1:
                filename_trimmed = filename[:n3]

        filename_trimmed_crd = filename_trimmed + '.crd'
        os.system('cp ../../%s%s %s' % (hosts_prep_dir, filename, filename_trimmed_crd))

    for filename in filenames_mol:

        filename_trimmed = filename[:-4]

        if do_name_trim:

            if name_trim:
                n1 = filename.find(name_trim)
            else:
                n1 = -1
            n2 = filename.find('_vm2')
            n3 = filename.find('_vc')

            if n1 != -1:
                filename_trimmed = filename[:n1]
            elif n2 != -1:
                filename_trimmed = filename[:n2]
            elif n3 != -1:
                filename_trimmed = filename[:n3]

        filename_trimmed_mol = filename_trimmed + '.mol'
        os.system('cp ../../%s%s %s' % (hosts_prep_dir, filename, filename_trimmed_mol))

    for filename in filenames_top:

        filename_trimmed = filename[:-4]

        if do_name_trim:

            if name_trim:
                n1 = filename.find(name_trim)
            else:
                n1 = -1
            n2 = filename.find('_vm2')
            n3 = filename.find('_vc')

            if n1 != -1:
                filename_trimmed = filename[:n1]
            elif n2 != -1:
                filename_trimmed = filename[:n2]
            elif n3 != -1:
                filename_trimmed = filename[:n3]

        filename_trimmed_top = filename_trimmed + '.top'
        os.system('cp ../../%s%s %s' % (hosts_prep_dir, filename, filename_trimmed_top))


    for filename in filenames_tether:
        os.system('cp ../../%s%s %s' % (hosts_prep_dir, filename, filename))

    os.chdir(initial_path)

#------------------------------------------------------------------------------ 
# Populate input data directory for ligand start conformers - random set 
#------------------------------------------------------------------------------ 

if start_conf_rndm and data_source_argument != 'reuse':

    # Make input data directory for random ligand conf storage

    if not os.path.exists(ligand_rndm_confs):
        os.mkdir(ligand_rndm_confs)
    else:
       print '\nDirectory for random ligand conformers already exists! Quiting.' 
       sys.exit()

    # Define where to get the data

    os.chdir(initial_path)

    ligand_conf_dir = None

    if data_source == 'reference':
        ligand_conf_dir = ligand_confgen_path + '/reference/' + ligand_randomconf_dir 
    elif data_source == 'new':
        ligand_conf_dir = ligand_confgen_path + '/' + ligand_randomconf_dir 
    else:
        print '\nNo ligand conformer generation directory defined!'
        sys.exit()

    # Change to the directory and get sub-directory names i.e. ligand names

    os.chdir(ligand_conf_dir)

    molecule_names = glob.glob('*')

    if len(molecule_names) == 0:
        print '\nNo data found in directory %s' %ligand_conf_dir
        sys.exit()

    molecule_names.sort()

    # Make directories with the same name in local input_data

    os.chdir(ligand_rndm_confs)

    for molecule_name in molecule_names:
        os.mkdir(molecule_name)

    # Go back to where data is to do copy

    os.chdir(initial_path)
    os.chdir(ligand_conf_dir)

    for molecule_name in molecule_names:
        os.chdir(molecule_name)

        file_names = glob.glob('*')

        for file_name in file_names:
            if file_name.endswith('xyz'):
               
                os.system('cp %s %s/%s/%s' % (file_name,  ligand_rndm_confs, molecule_name, file_name))

        os.chdir('../')
  
    os.chdir(initial_path)

#------------------------------------------------------------------------------ 
# Get ligand key list - tells which run directories to make 
#------------------------------------------------------------------------------ 

if ligand_key_file:
    parseLigandKey(ligand_key_file, ligand_key_list)

#------------------------------------------------------------------------------ 
# Store paths to required data and run directories 
#------------------------------------------------------------------------------ 

if (start_conf_rndm and vm2_fast):
    if not os.path.exists(fast_vm2_rndm_path):
        os.mkdir(fast_vm2_rndm_path)
    run_dirs['fast_vm2_rndm'] = fast_vm2_rndm_path
    inp_files['fast_vm2_rndm'] = '_HOSTNAME__LIGNAME__fast_vm2_rndm.inp'
    host_inp_files['fast_vm2_rndm'] = '_HOSTNAME__fast_vm2.inp'
    conf_dirs['fast_vm2_rndm'] = ligand_rndm_confs

if (start_conf_rndm and vm2_regular):
    if not os.path.exists(vm2_rndm_path):
        os.mkdir(vm2_rndm_path)
    run_dirs['vm2_rndm'] = vm2_rndm_path
    inp_files['vm2_rndm'] = '_HOSTNAME__LIGNAME__vm2_rndm.inp'
    host_inp_files['vm2_rndm'] = '_HOSTNAME__vm2.inp'
    conf_dirs['vm2_rndm'] = ligand_rndm_confs

if (start_conf_single and vm2_fast):
    if not os.path.exists(fast_vm2_single_path):
        os.mkdir(fast_vm2_single_path)
    run_dirs['fast_vm2_single'] = fast_vm2_single_path
    inp_files['fast_vm2_single'] = '_HOSTNAME__LIGNAME__fast_vm2_single.inp'
    host_inp_files['fast_vm2_single'] = '_HOSTNAME__fast_vm2.inp'
    conf_dirs['fast_vm2_single'] =  None

if (start_conf_single and vm2_regular):
    if not os.path.exists(vm2_single_path):
        os.mkdir(vm2_single_path)
    run_dirs['vm2_single'] = vm2_single_path
    inp_files['vm2_single'] = '_HOSTNAME__LIGNAME__vm2_single.inp'
    host_inp_files['vm2_single'] = '_HOSTNAME__vm2.inp'
    conf_dirs['vm2_single'] =  None

print run_dirs

#------------------------------------------------------------------------------ 
# Set up run directory for ligand vm2 calculations 
#------------------------------------------------------------------------------ 

inptemplate = "_LIGNAME__vm2.inp"

molecule_names = []

ligand_data_path = input_data_path + '/ligands'
os.chdir(ligand_data_path)

mol_filenames = glob.glob('*.mol')

if len(mol_filenames) == 0:
    print '\nNo data found in directory %s' %ligand_data_path
    sys.exit()

mol_filenames.sort()

for filename in mol_filenames:
    if ligand_key_list:
        for key in ligand_key_list:
            if key in filename: 
                molecule_names.append(filename.split('.')[0])
                break
    else:
        molecule_names.append(filename.split('.')[0])
            
os.chdir(initial_path)

for k, run_path in run_dirs.iteritems():

    os.chdir(run_path)

    if not os.path.exists('ligands'):
        os.mkdir('ligands')

    os.chdir('ligands')

    for name in molecule_names:
        if not os.path.exists(name):
            os.mkdir(name)
        else:
           print '\nDirectories for ligand VM2 calculations already exist! Quiting.' 
           sys.exit()

    os.chdir(initial_path)

    ligand_run_dir = run_path + '/ligands'

    for name in molecule_names:

        inp_file_name = inptemplate.replace("_LIGNAME_",name)  

        writeVm2Input(inptemplate, inp_file_name, None, None, None, None, None, name, name,
                      name, None, None, None, None)

        os.system('mv %s %s/%s/%s' % (inp_file_name, ligand_run_dir, name, inp_file_name))

        filename_crd = name + '.crd'
        filename_top = name + '.top'
        filename_mol = name + '.mol'

        os.system('cp %s/%s %s/%s/%s' % (ligand_data_path, filename_crd, ligand_run_dir, name, filename_crd))
        os.system('cp %s/%s %s/%s/%s' % (ligand_data_path, filename_top, ligand_run_dir, name, filename_top))
        os.system('cp %s/%s %s/%s/%s' % (ligand_data_path, filename_mol, ligand_run_dir, name, filename_mol))

#------------------------------------------------------------------------------ 
# Set up run directories for host-only vm2 calculations 
#------------------------------------------------------------------------------ 

#inptemplate = "_HOSTNAME__vm2.inp"

tether_file_names = {}
tether_file_name = None

host_data_path = input_data_path + '/hosts'
os.chdir(host_data_path)

filenames_crd = glob.glob('*.crd')
filenames_mol = glob.glob('*.mol')
filenames_top = glob.glob('*.top')
filenames_tether = glob.glob('*tethered_atoms*')

if len(filenames_crd) == 0:
    print '\nNo crd data found in directory %s' %host_data_path
    sys.exit()

if len(filenames_mol) == 0:
    print '\nNo mol data found in directory %s' %host_data_path
    sys.exit()

if len(filenames_top) == 0:
    print '\nNo top data found in directory %s' %host_data_path
    sys.exit()

if len(filenames_crd) != len(filenames_mol) or \
   len(filenames_crd) != len(filenames_top) or \
   len(filenames_mol) != len(filenames_top):
    print '\nMismatch in number of crd mol and top files in %s' %host_data_path
    sys.exit()

filenames_crd.sort()
filenames_mol.sort()
filenames_top.sort()

host_names = []

for filename in filenames_crd:
    if host_key_list:
        for key in host_key_list:
            if key in filename: 
                host_names.append(filename.split('.')[0])
                break
    else:
        host_names.append(filename.split('.')[0])
            
print filenames_crd
print filenames_mol
print filenames_top

if len(filenames_tether) != 0:
    filenames_tether.sort()
    print filenames_tether
    for name in host_names:
        for tether_file_name in filenames_tether:
           if name in tether_file_name:
               tether_file_names[name] = tether_file_name 

os.chdir(initial_path)

for k, run_path in run_dirs.iteritems():

    os.chdir(run_path)

    if not os.path.exists('hosts'):
        os.mkdir('hosts')

    os.chdir('hosts')

    for host_name in host_names:
        if not os.path.exists(host_name):
            print 'make host_name dir %s' %host_name
            os.mkdir(host_name)
        else:
           print '\nDirectories for host VM2 calculations already exist! Quiting.' 
           sys.exit()

    inptemplate = host_inp_files[k]

    i = -1

    for host_name in host_names:

        i += 1

        base_name = host_name
        print base_name

        os.chdir(initial_path)

        inp_file_name = inptemplate.replace("_HOSTNAME_",base_name)

        host_run_dir = run_path + '/hosts'

        if tether_file_names.has_key(host_name):
            tether_file_name = tether_file_names[host_name]
        else:
            tether_file_name = None

        filename_crd = filenames_crd[i]
        filename_top = filenames_top[i]
        filename_mol = filenames_mol[i]

        writeVm2Input(inptemplate, inp_file_name, None,
                      filename_crd, filename_top, filename_mol, None, None, None,
                      None, None, None, None, tether_file_name) 

        os.system('mv %s %s/%s/%s' % (inp_file_name, host_run_dir, host_name, inp_file_name))

        os.system('cp %s/%s %s/%s/%s' % (host_data_path, filename_crd, host_run_dir, host_name, filename_crd))
        os.system('cp %s/%s %s/%s/%s' % (host_data_path, filename_top, host_run_dir, host_name, filename_top))
        os.system('cp %s/%s %s/%s/%s' % (host_data_path, filename_mol, host_run_dir, host_name, filename_mol))

        if tether_file_name:
            os.system('cp %s/%s %s/%s/%s' % (host_data_path, tether_file_name, host_run_dir, host_name,
                                             tether_file_name))

#------------------------------------------------------------------------------ 
# Set up run directories for host-ligand vm2 calculations 
#------------------------------------------------------------------------------ 

tether_file_names = {}
tether_file_name = None

conf_file_xyz = None
conf_file_crd = None

host_data_path = input_data_path + '/hosts'
os.chdir(host_data_path)

host_filenames_crd = glob.glob('*.crd')
host_filenames_mol = glob.glob('*.mol')
host_filenames_top = glob.glob('*.top')
host_filenames_tether = glob.glob('*tethered_atoms*')

if len(host_filenames_crd) == 0:
    print '\nNo crd data found in directory %s' %host_data_path
    sys.exit()

if len(host_filenames_mol) == 0:
    print '\nNo mol data found in directory %s' %host_data_path
    sys.exit()

if len(host_filenames_top) == 0:
    print '\nNo top data found in directory %s' %host_data_path
    sys.exit()

if len(host_filenames_crd) != len(host_filenames_mol) or \
   len(host_filenames_crd) != len(host_filenames_top) or \
   len(host_filenames_mol) != len(host_filenames_top):
    print '\nMismatch in number of crd mol and top files in %s' %host_data_path
    sys.exit()

host_filenames_crd.sort()
host_filenames_mol.sort()
host_filenames_top.sort()

host_names = []

for filename in host_filenames_crd:
    if host_key_list:
        for key in host_key_list:
            if key in filename: 
                host_names.append(filename.split('.')[0])
                break
    else:
        host_names.append(filename.split('.')[0])

print 'host names %s' %host_names
            
print host_filenames_crd
print host_filenames_mol
print host_filenames_top

if len(host_filenames_tether) != 0:
    host_filenames_tether.sort()
    print host_filenames_tether
    for host_name in host_names:
        for tether_file_name in host_filenames_tether:
           if host_name in tether_file_name:
               tether_file_names[host_name] = tether_file_name 

os.chdir(initial_path)

molecule_names = []

ligand_data_path = input_data_path + '/ligands'
template_data_path = ligand_data_path + '/template'

os.chdir(ligand_data_path)

mol_filenames = glob.glob('*.mol')

if len(mol_filenames) == 0:
    print '\nNo data found in directory %s' %ligand_data_path
    sys.exit()

mol_filenames.sort()

for filename in mol_filenames:
    if ligand_key_list:
        for key in ligand_key_list:
            if key in filename: 
                molecule_names.append(filename.split('.')[0])
                break
    else:
        molecule_names.append(filename.split('.')[0])

if os.path.exists(template_data_path):
    os.chdir(template_data_path)
    filename_template = glob.glob('*')[0]
else:
    template_data_path = None
    filename_template = None
            
os.chdir(initial_path)

for k, run_path in run_dirs.iteritems():

    os.chdir(run_path)

    if not os.path.exists('complexes'):
        os.mkdir('complexes')

    os.chdir(initial_path)

    inptemplate = inp_files[k]

    i = -1

    for host_name in host_names:

        i += 1

        host_base_name = host_name
        print host_base_name
        inp_file_base = inptemplate.replace("_HOSTNAME",host_base_name)

        os.chdir(run_path + '/complexes')
        os.mkdir(host_base_name)

        complex_run_dir = run_path + '/complexes/' + host_base_name
        os.chdir(complex_run_dir)

        if tether_file_names.has_key(host_name):
            tether_file_name = tether_file_names[host_name]
        else:
            tether_file_name = None

        complex_dir_names = {}

        for name in molecule_names:
            dirname  = host_base_name + '_' + name
            complex_dir_names[name] = dirname 
            if not os.path.exists(dirname):
                os.mkdir(dirname)
            else:
               print '\nDirectories for host-ligand complex runs already exist! Quiting.' 
               sys.exit()

        os.chdir(initial_path)

        for name in molecule_names:

            dirname = complex_dir_names[name]

            inp_file_name = inp_file_base.replace("_LIGNAME_",name)

            if conf_dirs[k]:
                conf_path = conf_dirs[k] + '/' + name
                os.chdir(conf_path)

                conf_file_xyz = glob.glob('*.xyz')
                if len(conf_file_xyz) == 0:
                    print '\nNo conformer xyz files found in directory %s' %conf_path
                    #sys.exit()
                else:
                   conf_file_xyz = glob.glob('*.xyz')[0]

                # In case rank_1 .crd supplied as starting coords
                conf_file_crd = glob.glob('*.crd')

            if conf_file_crd:
                file_crd = conf_file_crd[0].split('.')[0]
            else:
                file_crd = name 

            os.chdir(initial_path)

            filename_crd = host_filenames_crd[i]
            filename_top = host_filenames_top[i]
            filename_mol = host_filenames_mol[i]

            writeVm2Input(inptemplate, inp_file_name, conf_file_xyz,
                      filename_crd, filename_top, filename_mol,
                      None, file_crd, name, name, filename_template, None, None,
                      tether_file_name)

            os.system('mv %s %s/%s/%s' % (inp_file_name, complex_run_dir, dirname, inp_file_name))

            os.system('cp %s/%s %s/%s/%s' % (host_data_path, filename_crd, complex_run_dir, dirname, filename_crd))
            os.system('cp %s/%s %s/%s/%s' % (host_data_path, filename_top, complex_run_dir, dirname, filename_top))
            os.system('cp %s/%s %s/%s/%s' % (host_data_path, filename_mol, complex_run_dir, dirname, filename_mol))

            if tether_file_name:
                os.system('cp %s/%s %s/%s/%s' % (host_data_path, tether_file_name, complex_run_dir, dirname,
                                                 tether_file_name))

            filename_crd = name + '.crd'
            filename_top = name + '.top'
            filename_mol = name + '.mol'

            os.system('cp %s/%s %s/%s/%s' % (ligand_data_path, filename_crd, complex_run_dir, dirname, filename_crd))
            os.system('cp %s/%s %s/%s/%s' % (ligand_data_path, filename_top, complex_run_dir, dirname, filename_top))
            os.system('cp %s/%s %s/%s/%s' % (ligand_data_path, filename_mol, complex_run_dir, dirname, filename_mol))

            if filename_template:
                os.system('cp %s/%s %s/%s/%s' % (template_data_path, filename_template, complex_run_dir, dirname, filename_template))

            if conf_file_xyz:
                os.system('cp %s/%s %s/%s/%s' % (conf_path, conf_file_xyz, complex_run_dir, dirname, conf_file_xyz))

            if conf_file_crd:
                os.system('cp %s/%s %s/%s/%s' % (conf_path, conf_file_crd[0], complex_run_dir, dirname, conf_file_crd[0]))
            
