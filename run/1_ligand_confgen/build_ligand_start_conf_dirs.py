import sys, re, os, shutil, socket
import fpformat, stat, glob
import getopt
import subprocess

def writeLigandInput(template_input_file, vm2_input_file, ligand_base, template_ligand,
                     pairs_map1, pairs_map2):

    file = open(template_input_file, 'r')
    lines = file.readlines()
    file.close()

    file = open(vm2_input_file, 'w')

    for line in lines:
        cols = line.split()
        if cols[0] == '_LIGNAMECRD_':
            file.write('%s.crd\n' % ligand_base)
        elif cols[0] == '_LIGNAMETOP_':
            file.write('%s.top\n' % ligand_base)
        elif cols[0] == '_LIGNAMEMOL_':
            file.write('%s.mol\n' % ligand_base)
        elif cols[0] == '_TEMPLATENAME_':
            file.write('%s\n' % template_ligand)
        elif cols[0] == '_PAIRSMAP1_':
            file.write('%s\n' % pairs_map1)
        elif cols[0] == '_PAIRSMAP2_':
            file.write('%s\n' % pairs_map2)
        else:
            file.write(line)

    file.close()

def parsePairMap(pair_map_file, pairs_map_list):

    file = open(pair_map_file, 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        pairs_map_list.append(line.strip())

def parsePairMapToDict(pair_map_file, pairs_map_dict):

    file = open(pair_map_file, 'r')
    lines = file.readlines()
    file.close()

    key_lines = lines[::2]

    for line in key_lines:
        cols = line.split()
        length = len(cols[0])
        key = line[0:length]
        pairs_map_dict[key] = []

    for line in lines:
        cols = line.split()
        length = len(cols[0])
        key = line[0:length]
        pairs_map_dict[key].append(line[length:].strip())

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

#------------------------------------------------------------------------------ 
# Set basic defaults
#------------------------------------------------------------------------------ 

data_source_argument = None
name_trim_argument = None
start_conf_type_argument = None
template_argument = None
clear_data_argument = None
ligand_key_argument = None

data_source = 'new'
name_trim = None
do_name_trim = True
start_conf_type = 'random'
filename_template = None 
clear_data = None

ligand_key_file = None
ligand_key_list = []

pair_map_filename = 'scaffold_mapping_wkey.txt'

#------------------------------------------------------------------------------ 
# Get commandline arguments
#------------------------------------------------------------------------------ 

argv = sys.argv[1:]

try:                                
    opts, args = getopt.getopt(argv, "hd:n:s:t:c:k:",
                 ["help","data=","nametrim=","startconfs=","template=", \
                  "clear=","keyfile="])
                 
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
    elif opt in ("-k", "--keyfile"):
       ligand_key_argument = arg

#------------------------------------------------------------------------------ 
# Set basic control variables 
#------------------------------------------------------------------------------ 

ligand_randomconf_dir = 'gen_ligand_start_confs_rndm'

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
       start_conf_type = 'random'
    elif start_conf_type_argument == 'random':
       start_conf_type = 'random'
    else:
        print '\nStart conf type argument %s is not recognized!' %start_conf_type_argument
        print 'Choose from: all, random'
        sys.exit()

if template_argument is not None:
    filename_template = template_argument
    print 'Template coordinate file name: %s' %filename_template
#elif data_source != 'reuse': 
#    print '\nA template coordinate file (e.g. co-xtal ligand .pdb) is required!'
#    sys.exit()

if clear_data_argument is not None:

    if clear_data_argument == 'all':
        clear_data = 'all'
        if data_source == 'reuse':
            print 'Request to clear input data and reuse it!'
            sys.exit()
    elif clear_data_argument == 'random':
        clear_data = 'random'
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

if ligand_key_argument is not None:
    ligand_key_file = ligand_key_argument
    print 'Ligand key file name: %s' %ligand_key_file

#------------------------------------------------------------------------------ 
# Clear directories as requested by user 
#------------------------------------------------------------------------------ 

if clear_data == 'all' or clear_data == 'input':

    if not os.path.exists(input_data_path):
        print '\nThe directory %s not foumd!' %input_data_path
        sys.exit()
    else:
        os.chdir(input_data_path)
        os.system('rm -rf *')
        os.chdir('../')

if clear_data == 'all' or clear_data == 'rundirs':

    if not os.path.exists(ligand_randomconf_dir):
        print '\nThe directory %s not foumd!' %ligand_randomconf_dir
        sys.exit()
    else:
        os.chdir(ligand_randomconf_dir)
        os.system('rm -rf *')
        os.chdir('../')

#------------------------------------------------------------------------------ 
# Populate input data directory 
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

    print 'ligand prep dir %s' %ligand_prep_dir

    os.chdir(ligand_prep_dir)

    mol_filenames = glob.glob('*.mol')

    mol_filenames.sort()

    for filename in mol_filenames:
        print filename
        molecule_names.append(filename.split('.')[0])

    if not os.path.exists(input_data_path):
        os.mkdir(input_data_path)

    os.chdir(input_data_path)

    if os.path.exists('template'):
        os.system('rm -rf template')

    if filename_template is not None:
        if not os.path.exists('template'):
            os.mkdir('template')
        os.chdir('template')
        print 'cp ../../%s%s %s' % (ligand_prep_dir, filename_template, filename_template)
        os.system('cp ../../%s%s %s' % (ligand_prep_dir, filename_template, filename_template))
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

        os.system('cp ../%s%s %s' % (ligand_prep_dir, filename_crd, filename_trimmed_crd))
        os.system('cp ../%s%s %s' % (ligand_prep_dir, filename_top, filename_trimmed_top))
        os.system('cp ../%s%s %s' % (ligand_prep_dir, filename_mol, filename_trimmed_mol))

    os.chdir('../')

#------------------------------------------------------------------------------ 
# Get ligand key list - tells which run directories to make 
#------------------------------------------------------------------------------ 

if ligand_key_file:
    parseLigandKey(ligand_key_file, ligand_key_list)

#------------------------------------------------------------------------------ 
# Set up directory for generation of randomly orientated ligand conformers
# with their center of geometry (COG) moved to the template's COG. 
#------------------------------------------------------------------------------ 

if start_conf_type  == 'all' or start_conf_type == 'random':

    molecule_names = []

    os.chdir(input_data_path)

    mol_filenames = glob.glob('*.mol')

    mol_filenames.sort()

    for filename in mol_filenames:
        if ligand_key_list:
            for key in ligand_key_list:
                if key in filename:
                    molecule_names.append(filename.split('.')[0])
                    break
        else:
            molecule_names.append(filename.split('.')[0])
            
    os.chdir('../')

    if data_source == 'reuse':
        os.chdir(input_data_path + '/template')
        filename_template = glob.glob('*')[0]
        os.chdir('../..')

    if not os.path.exists(ligand_randomconf_dir):
        os.mkdir(ligand_randomconf_dir)

    os.chdir(ligand_randomconf_dir)

    for name in molecule_names:
        if not os.path.exists(name):
            os.mkdir(name)
        else:
           print '\nDirectories for random ligand conformer generation already exist! Quiting.' 
           sys.exit()

    os.chdir('../')
    inptemplate = "_LIGNAME__confgen4.inp"

    for name in molecule_names:

        inp_file_name = inptemplate.replace("_LIGNAME_",name)  
        writeLigandInput(inptemplate, inp_file_name, name, filename_template, None, None)
        os.system('mv %s %s/%s/%s' % (inp_file_name, ligand_randomconf_dir, name, inp_file_name))

        filename_crd = name + '.crd'
        filename_top = name + '.top'
        filename_mol = name + '.mol'

        os.system('cp %s/%s %s/%s/%s' % (input_data_path, filename_crd, ligand_randomconf_dir, name, filename_crd))
        os.system('cp %s/%s %s/%s/%s' % (input_data_path, filename_top, ligand_randomconf_dir, name, filename_top))
        os.system('cp %s/%s %s/%s/%s' % (input_data_path, filename_mol, ligand_randomconf_dir, name, filename_mol))

        if filename_template:
            os.system('cp %s/%s/%s %s/%s/%s' % (input_data_path, 'template', filename_template, 
                                          ligand_randomconf_dir, name, filename_template))
