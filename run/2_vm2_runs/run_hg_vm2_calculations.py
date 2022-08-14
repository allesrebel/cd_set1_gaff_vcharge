import sys, re, os, shutil, socket
import fpformat, stat, glob
import getopt
import subprocess

def writeRunScript(template_run_script, vm2_run_script, vm2_input_file,
                   vm2_output_file, vm2_exe, threads, vc_rtlibrary_info_file,
                   exe_location):

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
            modline = line.replace("_VCEXELOCATION_",exe_location)
            if '_VCRUNEXE_' in modline:
                file.write(modline.replace("_VCRUNEXE_",vm2_exe))
            else:
                file.write(modline)
        elif '_VCFILEINP_' in line:
            file.write(line.replace("_VCFILEINP_",vm2_input_file))
        elif '_VCFILEOUT_' in line:
            file.write(line.replace("_VCFILEOUT_",vm2_output_file))
        elif '_VCOMPTHREADS_' in line:
            file.write(line.replace("_VCOMPTHREADS_",str(threads)))
        elif '_VCMKLTHREADS_' in line:
            file.write(line.replace("_VCMKLTHREADS_",str(threads)))
        else:
            file.write(line)

    file.close()


#------------------------------------------------------------------------------ 
# Start of script 
#------------------------------------------------------------------------------ 

print
print '-'*80
print "Run VM2 package free energy calculations."
print '-'*80

initial_path = os.getcwd()
input_data_path = initial_path + '/input_data'

fast_vm2_rndm_path = initial_path + '/fast_vm2_rndm'
vm2_rndm_path = initial_path + '/vm2_rndm'
vm2_single_path = initial_path + '/vm2_single'
fast_vm2_single_path = initial_path + '/fast_vm2_single'

mpi_exe = 'VC_CompChemPackage_mpi.exe'
mpi_openmp_exe = 'VC_CompChemPackage_mpi_openmp.exe'
mpi_cuda_exe = 'VC_CompChemPackage_mpi_openmp_cuda.exe'

#------------------------------------------------------------------------------ 
# Set basic defaults
#------------------------------------------------------------------------------ 

start_conf_type_argument = None
run_script_type_argument = None
vm2_type_argument = None
omp_threads_argument = None
molsystems_argument = None
exe_type_argument = None
queue_partition_argument = None

start_conf_type = 'rndm'
start_conf_rndm = True
start_conf_single = False

run_script_type = 'bsh'
prep_mode = False
clear_data = False

vm2_type = 'regular'
vm2_fast = False
vm2_regular = True

run_cuda_exe = False

molsystems = 'all'
run_ligands = True
run_complexes = True
run_hosts = True

omp_threads = 16

exe_type = 'production'
queue_partition = 'compute'

#------------------------------------------------------------------------------ 
# Get commandline arguments
#------------------------------------------------------------------------------ 

argv = sys.argv[1:]

try:                                
    opts, args = getopt.getopt(argv, "hs:r:pcv:go:m:e:q:",
                 ["help","startconfs=","runscript=", "prepmode", "clear", "vm2type=",
                  "gpu", "ompthreads=", "molsystems=", "exe=", "partition="])
                 
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
        clear_data = True
    elif opt in ("-v", "--vm2type"):
        vm2_type_argument = arg
    elif opt in ("-g", "--gpu"):
        run_cuda_exe = True
    elif opt in ("-o", "--ompthreads"):
        omp_threads_argument = arg
    elif opt in ("-m", "--molsystems"):
        molsystems_argument = arg
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
       start_conf_rndm = True
       start_conf_single = True
    elif start_conf_type_argument == 'random':
       start_conf_type = 'random'
       start_conf_rndm = True
       start_conf_single = False
    elif start_conf_type_argument == 'single':
       start_conf_type = 'single'
       start_conf_rndm = False
       start_conf_single = True
    else:
        print '\nStart conf type argument %s is not recognized!' %start_conf_type_argument
        print 'Choose from: all, random, or single'
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

if omp_threads_argument is not None:

    print omp_threads_argument

    if omp_threads_argument == '1':
        omp_threads = 1 
    elif omp_threads_argument == '2':
        omp_threads = 2 
    else:
        print '\nOpenMP threads argument %s is not recognized!' %omp_threads_argument
        print 'Choose from: 1 or 2' 
        sys.exit()

if molsystems_argument is not None:

    if molsystems_argument == 'all':
       run_complexes = True
       run_ligands = True
       run_hosts = True
    elif molsystems_argument == 'complexes+ligands':
       run_complexes = True
       run_ligands = True
       run_hosts = False
    elif molsystems_argument == 'hosts+ligands':
       run_complexes = False
       run_ligands = True
       run_hosts = True
    elif molsystems_argument == 'complexes+hosts':
       run_complexes = True
       run_ligands = False
       run_hosts = True
    elif molsystems_argument == 'complexes':
       run_complexes = True
       run_ligands = False
       run_hosts = False
    elif molsystems_argument == 'ligands':
       run_complexes = False
       run_ligands = True
       run_hosts = False
    elif molsystems_argument == 'hosts':
       run_complexes = False
       run_ligands = False
       run_hosts = True
    else:
        print '\nMolsystems argument %s is not recognized!' %molsystems_argument
        print 'Choose from: all, complexes+ligands, hosts+ligands, complexes+hosts, complexes, ligands, or hosts'
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
#               run directory


if clear_data:

    if (start_conf_single and vm2_fast):
        os.chdir(fast_vm2_single_path)
#       os.system('rm -rf ligand')
        os.chdir('../')

    if (start_conf_single and vm2_regular):
        os.chdir(vm2_single_path)
#       os.system('rm -rf ligand')
        os.chdir('../')

    if (start_conf_rndm and vm2_fast):
        os.chdir(fast_vm2_rndm_path)
#       os.system('rm -rf ligand')
        os.chdir('../')

    if (start_conf_rndm and vm2_regular):
        os.chdir(vm2_rndm_path)
#       os.system('rm -rf ligand')
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
# Make a dictionary of required top level run paths 
#------------------------------------------------------------------------------ 

run_dirs = {}

if (start_conf_single and vm2_fast):
    run_dirs['fast_vm2_single'] = fast_vm2_single_path

if (start_conf_rndm and vm2_fast):
    run_dirs['fast_vm2_rndm'] = fast_vm2_rndm_path

if (start_conf_single and vm2_regular):
    run_dirs['vm2_single'] = vm2_single_path

if (start_conf_rndm and vm2_regular):
    run_dirs['vm2_rndm'] = vm2_rndm_path

#------------------------------------------------------------------------------ 
# Carry out reuqested VM2 runs 
#------------------------------------------------------------------------------ 

for k, run_path in run_dirs.iteritems():

    # Start with ligands 

    if run_ligands:

        vm2_exe = mpi_exe
        threads = 16

        os.chdir(run_path)

        if os.path.exists('ligands'):
            os.chdir('ligands')

        dirname_list = glob.glob('*')

        dirname_list.sort()

        for dirname in dirname_list:

            run_dir = run_path + '/ligands/' + dirname

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
                           vm2_output_file, vm2_exe, threads, vc_rtlibrary_info_file,
                           exe_location)

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

    # On to complexes 

    if run_complexes:

        vm2_exe = mpi_exe
        threads = 16

        if run_cuda_exe:
            vm2_exe = mpi_cuda_exe 
            threads = omp_threads
        elif omp_threads > 1:
            vm2_exe = mpi_openmp_exe 
            threads = omp_threads

        os.chdir(run_path)

        if os.path.exists('complexes'):
            os.chdir('complexes')

        complex_topdir_list = glob.glob('*')

        complex_topdir_list.sort()

        for topdirname in complex_topdir_list:

            os.chdir(run_path + '/complexes/' + topdirname)

            dirname_list = glob.glob('*')

            dirname_list.sort()

            for dirname in dirname_list:

                run_dir = run_path + '/complexes/' + topdirname + '/' + dirname

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
                               vm2_output_file, vm2_exe, threads, vc_rtlibrary_info_file,
                               exe_location)

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

    # On to hosts 

    if run_hosts:

        vm2_exe = mpi_exe
        threads = 16

        if run_cuda_exe:
            vm2_exe = mpi_cuda_exe 
            threads = omp_threads
        elif omp_threads > 1:
            vm2_exe = mpi_openmp_exe 
            threads = omp_threads

        os.chdir(run_path)

        if os.path.exists('hosts'):
            os.chdir('hosts')

        host_topdir_list = glob.glob('*')

        host_topdir_list.sort()

        for topdirname in host_topdir_list:

            run_dir = run_path + '/hosts/' + topdirname

            os.chdir(run_dir)
    
            inp_file_list = glob.glob('*.inp')
    
            if len(inp_file_list) == 0:
                print 'No input file in directory %s' %topdirname
                sys.exit()
            elif len(inp_file_list) > 1:
                print 'More than one input file in directory %s' %topdirname
                sys.exit()

            vm2_input_file = inp_file_list[0] 
            vm2_output_file = vm2_input_file.replace(".inp", ".out") 

            writeRunScript(template_run_script, vm2_run_script, vm2_input_file,
                           vm2_output_file, vm2_exe, threads, vc_rtlibrary_info_file,
                           exe_location)

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
