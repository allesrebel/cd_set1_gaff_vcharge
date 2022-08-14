import sys, re, os, shutil, socket
import fpformat, stat, glob
import getopt
import subprocess

def writeRunScript(template_run_script, vm2_run_script, vm2_input_file,
                   vm2_output_file, vc_rtlibrary_info_file, exe_location):

    file = open(template_run_script, 'r')
    lines = file.readlines()
    file.close()

    if vc_rtlibrary_info_file:
       file = open(vc_rtlibrary_info_file, 'r')
       lines_rt = file.readlines()
       file.close()

    file = open(vm2_run_script, 'w')

    for line in lines:
        cols = line.split()
        if '_VCRTLIBRARIESINFO_' in line:
            if vc_rtlibrary_info_file:
                for line_rt in lines_rt:
                    file.write(line_rt)
        elif '_VCEXELOCATION_' in line:
            file.write(line.replace("_VCEXELOCATION_",exe_location))
        elif '_VCFILEINP_' in line:
            file.write(line.replace("_VCFILEINP_",vm2_input_file))
        elif '_VCFILEOUT_' in line:
            file.write(line.replace("_VCFILEOUT_",vm2_output_file))
        else:
            file.write(line)

    file.close()


#------------------------------------------------------------------------------ 
# Start of script 
#------------------------------------------------------------------------------ 

print
print '-'*80
print "Run VM2 package calculations for generation of ligand start conformers"
print '-'*80

initial_path = os.getcwd()

#------------------------------------------------------------------------------ 
# Set basic defaults
#------------------------------------------------------------------------------ 

start_conf_type_argument = None
run_script_type_argument = None
clear_data_argument = None
exe_type_argument = None
queue_partition_argument = None

start_conf_type = 'random'
run_script_type = 'bsh'
prep_mode = False
clear_data = None
exe_type = 'production'
queue_partition = None

ligand_randomconf_dir = initial_path + '/gen_ligand_start_confs_rndm'
ligand_snapconf_dir = initial_path + '/gen_ligand_start_confs_snap'

#------------------------------------------------------------------------------ 
# Get commandline arguments
#------------------------------------------------------------------------------ 

argv = sys.argv[1:]

try:                                
    opts, args = getopt.getopt(argv, "hs:r:pc:e:q:",
                 ["help","startconfs=","runscript=", "prepmode", "clear=", "exe=", \
                  "partition="])
                 
except getopt.GetoptError as err:
    # print help information and exit:
    print str(err)
    #usage()
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        #usage()                     
        sys.exit()                  
    elif opt in ("-s", "--startconfs"):
        start_conf_type_argument = arg
    elif opt in ("-r", "--runscript"):
        run_script_type_argument = arg
    elif opt in ("-p", "--prepmode"):
        prep_mode = True 
    elif opt in ("-c", "--clear"):
        clear_data_argument = arg
    elif opt in ("-e", "--exe"):
        exe_type_argument = arg
    elif opt in ("-q", "--partition"):
        queue_partition_argument = arg

#------------------------------------------------------------------------------ 
# Set basic control variables 
#------------------------------------------------------------------------------ 

if start_conf_type_argument is not None:

    if start_conf_type_argument == 'all':
       start_conf_type = 'all'
    elif start_conf_type_argument == 'random':
       start_conf_type = 'random'
    elif start_conf_type_argument == 'snap':
       start_conf_type = 'snap'
    else:
        print '\nStart conf type argument %s is not recognized!' %start_conf_type_argument
        print 'Choose from: all, random, or snap'
        sys.exit()

if run_script_type_argument is not None:

    if run_script_type_argument == 'bsh':
        run_script_type = 'bsh'
    elif run_script_type_argument == 'csh':
        run_script_type = 'csh'
    elif run_script_type_argument == 'pbs':
        run_script_type = 'pbs'
    elif run_script_type_argument == 'slurm':
        run_script_type = 'slurm'
    elif run_script_type_argument == 'vcq':
        run_script_type = 'vcq'
    else:
        print '\nRun script argument %s is not recognized!' %run_script_type_argument
        print 'Choose from: bsh, csh, pbs, or slurm'
        sys.exit()

if clear_data_argument is not None:

    if clear_data_argument == 'all':
        clear_data = 'all'
    elif clear_data_argument == 'random':
        clear_data = 'random'
    elif clear_data_argument == 'snap':
        clear_data = 'snap'
    else:
        print '\nClear data argument %s is not recognized!' %clear_data_argument
        print 'Choose from: all, input, or rundirs'
        sys.exit()

if exe_type_argument is not None:

    if exe_type_argument == 'production':
        exe_type = 'production'
    elif exe_type_argument == 'main':
        exe_type = 'main'
    elif exe_type_argument == 'dev':
        exe_type = 'dev'
    else:
        print '\nExe type argument %s is not recognized!' %exe_type_argument
        print 'Choose from: production, main, or dev'
        sys.exit()

if run_script_type == 'pbs' or run_script_type == 'slurm' or run_script_type == 'vcq':

    if queue_partition_argument is not None:
        queue_partition = queue_partition_argument


#------------------------------------------------------------------------------ 
# Clear run results from directories as requested by user
#------------------------------------------------------------------------------ 

# Placeholder : needs to be able to delete only output files in each individual
#               ligand run directory

if clear_data == 'all':

    os.chdir(ligand_randomconf_dir)
#   os.system('rm -rf *')
    os.chdir('../')

    os.chdir(ligand_snapconf_dir)
#   os.system('rm -rf *')
    os.chdir('../')

elif clear_data == 'random':

    os.chdir(ligand_randomconf_dir)
#   os.system('rm -rf *')
    os.chdir('../')

elif clear_data == 'snap':

    os.chdir(ligand_snapconf_dir)
#   os.system('rm -rf *')
    os.chdir('../')


#------------------------------------------------------------------------------ 
# Get name of run script template and set run script name
#------------------------------------------------------------------------------ 

if run_script_type == 'bsh':
    template_run_script = initial_path + '/runvm2_TEMPLATE_.bsh'
    vm2_run_script = 'runvm2.bsh'
elif run_script_type == 'csh':
    template_run_script = initial_path + '/runvm2_TEMPLATE_.csh'
    vm2_run_script = 'runvm2.csh'
elif run_script_type == 'pbs':
    template_run_script = initial_path + '/runvm2_TEMPLATE_.pbs'
    vm2_run_script = 'runvm2.pbs'
elif run_script_type == 'slurm':
    template_run_script = initial_path + '/runvm2_TEMPLATE_.slm'
    vm2_run_script = 'runvm2.slm'
elif run_script_type == 'vcq':
    template_run_script = initial_path + '/runvm2_TEMPLATE_.bsh'
    vm2_run_script = 'runvm2.bsh'

#------------------------------------------------------------------------------ 
# Get type of executable (production or a development line) and set file
# for runtime library info and exe directory if needed.
#------------------------------------------------------------------------------ 

vc_rtlibrary_info_file = None 

exe_location = None

if exe_type == 'production':
    
    if run_script_type == 'bsh' or run_script_type == 'pbs' \
    or run_script_type == 'slurm' or run_script_type == 'vcq':
        vc_rtlibrary_info_file = initial_path + '/runvm2_LIBRARIES_bsh'
    elif run_script_type == 'csh':
        vc_rtlibrary_info_file = initial_path + '/runvm2_LIBRARIES_csh'

    if "VCHOME" not in os.environ:
        print 'For production runs the environment variable VCHOME must be set. Quitting.'
        sys.exit()
    else:
        exe_location = '$VCHOME/exe'

elif exe_type == 'main':
    exe_location = '~/fromPerforce/fortran_package_main'
elif exe_type == 'dev':
    exe_location = '~/fromPerforce/fortran_package_dev'


#------------------------------------------------------------------------------ 
# Carry out VM2 runs for generation of randomly orientated ligand conformers
# with their center of geometry (COG) moved to the template's COG. 
#------------------------------------------------------------------------------ 

if start_conf_type  == 'all' or start_conf_type == 'random':

    os.chdir(ligand_randomconf_dir)

    dirname_list = glob.glob('*')

    dirname_list.sort()

    for dirname in dirname_list:

        run_dir = ligand_randomconf_dir + '/' + dirname

        os.chdir(run_dir)

        inp_file_list = glob.glob('*.inp')

        if len(inp_file_list) == 0:
            print 'No input file in directory %s' %dirname
            sys.exit()
        elif len(inp_file_list) > 1:
            print 'More than one input file in directory %s' %dirname
            sys.exit()

        vm2_input_file = inp_file_list[0] 
        vm2_output_file = vm2_input_file.replace(".inp", ".out") 

        writeRunScript(template_run_script, vm2_run_script, vm2_input_file,
                       vm2_output_file, vc_rtlibrary_info_file, exe_location)

        os.system('chmod 755 %s' %vm2_run_script)

        if not prep_mode:
            if run_script_type == 'pbs':
                if queue_partition:
                    subprocess.call('qsub -q ' +  queue_partition + ' ' + vm2_run_script, shell=True)
                else:
                    subprocess.call('qsub ' + vm2_run_script, shell=True)
            elif run_script_type == 'slurm':
                if queue_partition:
                    subprocess.call('sbatch --partition=' + queue_partition + ' ' + vm2_run_script, shell=True)
                else:
                    subprocess.call('sbatch ' + vm2_run_script, shell=True)
            elif run_script_type == 'vcq':
                curdir = os.getcwd()
                vm2_run_script_path = os.path.join(curdir, vm2_run_script)
                if queue_partition:
                    subprocess.call('q_sub ' + vm2_run_script_path + ' -' + queue_partition, shell=True)
                else:
                    subprocess.call('q_sub ' + vm2_run_script_path + ' -cpu', shell=True)
            else:
                subprocess.call('./' + vm2_run_script + ' >& runvm2.log', shell=True)

#------------------------------------------------------------------------------ 
# Carry out VM2 runs for generation of ligand conformers whose scaffold is
# 'snapped' to that of the template's corresponding atoms. 
#------------------------------------------------------------------------------ 

if start_conf_type  == 'all' or start_conf_type == 'snap':

    os.chdir(ligand_snapconf_dir)

    dirname_list = glob.glob('*')

    dirname_list.sort()

    for dirname in dirname_list:

        run_dir = ligand_snapconf_dir + '/' + dirname

        os.chdir(run_dir)

        inp_file_list = glob.glob('*.inp')

        if len(inp_file_list) == 0:
            print 'No input file in directory %s' %dirname
            sys.exit()
        elif len(inp_file_list) > 1:
            print 'More than one input file in directory %s' %dirname
            sys.exit()

        vm2_input_file = inp_file_list[0] 
        vm2_output_file = vm2_input_file.replace(".inp", ".out") 

        writeRunScript(template_run_script, vm2_run_script, vm2_input_file,
                       vm2_output_file)

        os.system('chmod 755 %s' %vm2_run_script)

        if not prep_mode:
            if run_script_type == 'pbs':
                if queue_partition:
                    subprocess.call('qsub -q ' +  queue_partition + ' ' + vm2_run_script, shell=True)
                else:
                    subprocess.call('qsub ' + vm2_run_script, shell=True)
            elif run_script_type == 'slurm':
                if queue_partition:
                    subprocess.call('sbatch --partition=' + queue_partition + ' ' + vm2_run_script, shell=True)
                else:
                    subprocess.call('sbatch ' + vm2_run_script, shell=True)
            elif run_script_type == 'vcq':
                curdir = os.getcwd()
                vm2_run_script_path = os.path.join(curdir, vm2_run_script)
                if queue_partition:
                    subprocess.call('q_sub ' + vm2_run_script_path + ' -' + queue_partition, shell=True)
                else:
                    subprocess.call('q_sub ' + vm2_run_script_path + ' -cpu', shell=True)
            else:
                subprocess.call('./' + vm2_run_script + ' >& runvm2.log', shell=True)
