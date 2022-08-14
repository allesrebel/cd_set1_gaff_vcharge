import os
import sys
import re, sys
import argparse
import errno
import glob
import getopt

class Vm2SummaryReader:

    def __init__(self, summary_file_name = None):

        self.summary_file_name = summary_file_name 

        self.processSummaryFile()

    def processSummaryFile(self):

        sumFile = open(self.summary_file_name, 'r')
        lines = sumFile.readlines()

        self._findFE(lines)
        self._findAvgE(lines)
        self._findS(lines)
        self._findU(lines)
        self._findW(lines)
        self._findHO_PE(lines)
        self._findPB(lines)
        self._findSA(lines)
        self._findValence(lines)
        self._findCoulomb(lines)
        self._findVdW(lines)
        self._findVdW6(lines)
        self._findVdW12(lines)
        self._findBond(lines)
        self._findAngle(lines)
        self._findPdihed(lines)
        self._findIdihed(lines)
        self._findTether(lines)
        self._findCPUtime(lines)
        self._findWallTime(lines)
        self._findConvergeFail(lines)
        self._findCrashStatus(lines)
        self._findLastIterFE(lines)

    def _findFE(self, lines):
        found = False 
        pat = re.compile('.*Free Energy                        G.*')
        for line in lines:
            if pat.search(line):
                found = True 
                cols = line.split()
                self.FE = float(cols[-1])
        if not found: 
            print "Failed to find Free Energy, G..."
            self.FE = 0.0
            #sys.exit() 

    def _findAvgE(self, lines):
        found = False 
        pat = re.compile('.*Average Potential Energy         < E >.*')
        for line in lines:
            if pat.search(line): 
                found = True 
                cols = line.split()
                self.AvgE = float(cols[-1])
        if not found:
            print "Failed to find Average Potential Energy, E..."
            self.AvgE = 0.0
            #sys.exit() 

    def _findS(self, lines):
        found = False
        pat = re.compile('.*Entropy                           -TS.*')
        for line in lines:
            if pat.search(line):
                found = True 
                cols = line.split()
                self.S = float(cols[-1])
        if not found:
            print "Failed to find Entropy, -TS..."
            self.S = 0.0
            #sys.exit() 

    def _findU(self, lines):
        found = False 
        pat = re.compile('.*< U >     .*')
        for line in lines:
            if pat.search(line):
                found = True 
                cols = line.split()
                self.U = float(cols[-1])
        if not found: 
            print "Failed to find U..."
            self.U = 0.0
            #sys.exit() 

    def _findW(self, lines):
        found = False
        pat = re.compile('.*< W.PBSA. >     .*')
        for line in lines:
            if pat.search(line):
                found = True
                cols = line.split()
                self.W = float(cols[-1])
        if not found:
            print "Failed to find W..."
            self.W = 0.0
            #sys.exit()

    def _findHO_PE(self, lines):
        found = False
        pat = re.compile('.*< H.O. P.E. >     .*')
        for line in lines:
            if pat.search(line):
                found = True 
                cols = line.split()
                self.HO_PE = float(cols[-1])
        if not found:
            print "Failed to find H.O. P.E."
            self.HO_PE = 0.0
            #sys.exit() 

    def _findPB(self, lines):
        found = False
        pat = re.compile('.* < PB >     .*')
        for line in lines:
            if pat.search(line):
                found = True 
                cols = line.split()
                self.PB = float(cols[-1])
        if not found:
            print "Failed to find Pb..."
            self.PB = 0.0
            #sys.exit() 

    def _findSA(self, lines):
        found = False
        pat = re.compile('.*< SA >     .*')
        for line in lines:
            if pat.search(line):
                found = True 
                cols = line.split()
                self.SA = float(cols[-1])
        if not found: 
            print "Failed to find SA..."
            self.SA = 0.0
            #sys.exit() 

    def _findValence(self, lines):
        found = False 
        pat = re.compile('.*< Valence >     .*')
        for line in lines:
            if pat.search(line):
                found = True 
                cols = line.split()
                self.Valence = float(cols[-1])
        if not found:
            print "Failed to find Valence..."
            self.Valence = 0.0
            #sys.exit() 

    def _findCoulomb(self, lines):
        found = False 
        pat = re.compile('.*< Coulomb >     .*')
        for line in lines:
            if pat.search(line):
                found = True 
                cols = line.split()
                self.Coulomb = float(cols[-1])
        if not found:
            print "Failed to find Coulomb..."
            self.Coulomb = 0.0
            #sys.exit() 

    def _findVdW(self, lines):
        found = False 
        pat = re.compile('.*< VdW >     .*')
        for line in lines:
            if pat.search(line):
                found = True 
                cols = line.split()
                self.VdW = float(cols[-1])
        if not found:
            print "Failed to find Vdw..."
            self.VdW = 0.0
            #sys.exit() 

    def _findVdW6(self, lines):
        found = False	
        pat = re.compile('.*< VdW6  >     .*')
        for line in lines:
            if pat.search(line):
                found = True 
                cols = line.split()
                self.VdW6 = float(cols[-1])
        if not found: 
            print "Failed to find VdW6..."
            self.VdW6 = 0.0
            #sys,exit() 

    def _findVdW12(self, lines):
        found = False 
        pat = re.compile('.*< VdW12 >     .*')
        for line in lines:
            if pat.search(line):
                found = True 
                cols = line.split()
                self.VdW12 = float(cols[-1])
        if not found:
            print "Failed to find VdW12..."
            self.VdW12 = 0.0
            #sys.exit()

    def _findBond(self, lines):
        found = False
        pat = re.compile('.*< Bond >     .*')
        for line in lines:
            if pat.search(line):
                found = True 
                cols = line.split()
                self.Bond = float(cols[-1])
        if not found:
            print "Failed to find Bond..."
            self.Bond = 0.0
            #sys.exit() 

    def _findAngle(self, lines):
        found = False	
        pat = re.compile('.*< Angle >     .*')
        for line in lines:
            if pat.search(line):
                found = True	
                cols = line.split()
                self.Angle = float(cols[-1])
        if not found:
            print "Failed to find Angle..."
            self.Angle = 0.0
            #sys.exit() 

    def _findPdihed(self, lines):
        found = False 
        pat = re.compile('.*< Pdihed >     .*')
        for line in lines:
            if pat.search(line):
                found = True 
                cols = line.split()
                self.Pdihed = float(cols[-1])
        if not found:
            print "Failed to find Pdihed..."
            self.Pdihed = 0.0
            #sys.exit() 

    def _findIdihed(self, lines):
        found = False 
        pat = re.compile('.*< Idihed >     .*')
        for line in lines:
            if pat.search(line):
                found = True 
                cols = line.split()
                self.Idihed = float(cols[-1])
        if not found:
            print "Failed to find Idihed..."
            self.Idihed = 0.0
            #sys.exit() 

    def _findTether(self, lines):
        found = False 
        pat = re.compile('.*< Tether >                .*')
        for line in lines:
            if pat.search(line):
                found = True 
                cols = line.split()
                self.Tether = float(cols[-1])
        if not found:
            print "Failed to find Tether..."
            self.Tether = 0.0
            #sys,exit() 

    def _findCPUtime(self, lines):
        found = False 
        pat = re.compile('.*Total cpu time for run.*')
        for line in lines:
            if pat.search(line):
                found = True 
                cols = line.split()
                self.Runtime = float(cols[-2])
        if not found:
            print "Failed to find CPU time..."
            self.Runtime = 0.0
            #sys,exit() 

    def _findWallTime(self, lines):
        found = False 
        pat = re.compile('.*Total wall time for run.*')
        for line in lines:
            if pat.search(line):
                found = True 
                cols = line.split()
                self.WallTime = float(cols[-2])
        if not found:
            print "Failed to find Wall time..."
            self.WallTime = 0.0
            #sys,exit() 

    def _findConvergeFail(self, lines):
        found = False 
        pat = re.compile('.*VM2 Free Energy failed to converge.*')
        for line in lines:
            if pat.search(line):
                found = True 
                self.FeConv = 'no'
                print "VM2 Free Energy failed to converge..."
        if not found:
            self.FeConv = 'yes' 

    def _findCrashStatus(self, lines):
        found = False 
        pat = re.compile('.*VCPack job finished normally.*')
        for line in lines:
            if pat.search(line):
                found = True 
                self.CrashStatus = 'no' 
        if not found:
            print "This VM2 calculation did not finish normally..."
            self.CrashStatus = 'yes' 
            #sys,exit() 

    def _findLastIterFE(self, lines):

        # If run crashed try and get the free energy of
        # the last VM2 iteration

        if self.FE == 0.0 and self.CrashStatus == 'yes':

            self.FeConv = 'no' 

            last_line = lines[-1]
            cols = last_line.split()

            length1 = len(cols)

            # Iteration line has 5 columns and columns 2 and 3
            # have 6 numbers after the decimal point.

            if length1 == 5:

                teststr = cols[1]
                length2 = 0
                try:
                    length2 = len(teststr.split('.')[1])
                except:
                    pass

                teststr = cols[2]
                length3 = 0
                try:
                    length3 = len(teststr.split('.')[1])
                except:
                    pass

                if length2 == 6 and length3 == 6:
                    self.FE = float(cols[1])



class Vm2ConformerExtractor:
    
    def __init__(self):
        return
    
    def mol2_conf_extract(self, system_name, mol2path, output_dir_path, numconf):

        # open input file and read all lines
        with open(mol2path) as mol2file:
            all_lines = [line for line in mol2file] 

        # set output array
        output_lines = []
        
        #search the lines for tags which define start and stop of a conformer
        search_string = '@<TRIPOS>MOLECULE'
        conf_count = 0
        
        for line in all_lines:
            #do we have as many as required?
            if conf_count > numconf:
                conf_count = numconf
                break
            # is this the beginning of a conformer?
            if search_string in line :
                if conf_count <= numconf:
                    conf_count +=1
                if conf_count <= numconf:
                    output_lines.append(line)
                    #print 'FOUND CONF#', conf_count
                
            else:
                output_lines.append(line) 

        # create an output file path
        filename = system_name + '_' + str(conf_count) + '_conformers.mol2'
        out_file_path = os.path.join(output_dir_path, filename)

        silentremove(out_file_path) # in case it already exists

        #open output file
        outfile = open(out_file_path, 'a')
        
        # write output file
        for new_line in output_lines:
            outfile.write(new_line)
        
        #close all files
        outfile.close()
        
        #print 'MOL2 OUTPUT LINES:', len (output_lines)
        #print 'MOL2 INPUT LINES', len (all_lines), '\n\n'

        return
    
    def pdb_conf_extract(self, system_name, pdbpath, output_dir_path, numconf):

        #open input file and read all lines
        with open(pdbpath) as pdbfile:
            all_lines = [line for line in pdbfile] 

        # set output array
        output_lines = []
        
        #search the lines for tags which define start and stop of a conformer
        search_string = 'ENDMDL'
        conf_count = 0
        
        for line in all_lines:
            #do we have as many as required?
            if conf_count == numconf:
                break
            # is this the END of a conformer?
            if search_string in line :
                conf_count +=1
                output_lines.append(line)
                #print 'FOUND CONF#', conf_count                    
            else:
                output_lines.append(line) 

        # create an output file path
        filename = system_name + '_' + str(conf_count) + '_conformers.pdb'
        out_file_path = os.path.join(output_dir_path, filename)

        silentremove(out_file_path) # in case it already exists

        #open output file
        outfile = open(out_file_path, 'a')
        
        # write output file
        for new_line in output_lines:
            outfile.write(new_line)
        
        #close all files
        outfile.close()
        
        #print 'PDB OUTPUT LINES:', len (output_lines)
        #print 'PDB INPUT LINES', len (all_lines), '\n\n'

        return

    def sdf_conf_extract(self, system_name, sdfpath, output_dir_path, numconf):

        #open input file and read all lines
        with open(sdfpath) as sdffile:
            all_lines = [line for line in sdffile] 

        # set output array
        output_lines = []
        
        #search the lines for tags which define start and stop of a conformer
        search_string = '$$$$'
        conf_count = 0
        
        for line in all_lines:
            #do we have as many as required?
            if conf_count == numconf:
                break
            # is this the END of a conformer?
            if search_string in line :
                conf_count +=1
                output_lines.append(line)
                #print 'FOUND CONF#', conf_count                    
            else:
                output_lines.append(line) 

        # create an output file path
        filename = system_name + '_' + str(conf_count) + '_conformers.sdf'
        out_file_path = os.path.join(output_dir_path, filename)

        silentremove(out_file_path) # in case it already exists

        #open output file
        outfile = open(out_file_path, 'a')
        
        # write output file
        for new_line in output_lines:
            outfile.write(new_line)
        
        #close all files
        outfile.close()
        
        #print 'SDF OUTPUT LINES:', len (output_lines)
        #print 'SDF INPUT LINES', len (all_lines), '\n\n'
        return
    
    def xyz_conf_extract(self, system_name, xyzpath, output_dir_path, numconf):

        #open input file and read all lines
        with open(xyzpath) as xyzfile:
            all_lines = [line for line in xyzfile] 
        
        # set output array
        output_lines = []
        
        # search the lines for tags which define start  of a conformer
        # for xyz files written by vm2 this is an atom count, always a line with length 7 chars
        # no other lines are this short
        
        conf_count = 0
        
        for line in all_lines:
            #do we have as many as required?
            if conf_count > numconf:
                conf_count = numconf
                break
            # is this the beginning of a conformer?
            if len(line) == 7 :
                if conf_count <= numconf:
                    conf_count +=1
                if conf_count <= numconf:
                    output_lines.append(line)
                    #print 'FOUND CONF#', conf_count
                
            else:
                output_lines.append(line) 

        # create an output file path
        filename = system_name + '_' + str(conf_count) + '_conformers.xyz'
        out_file_path = os.path.join(output_dir_path, filename)

        silentremove(out_file_path) # in case it already exists

        #open output file
        outfile = open(out_file_path, 'a')
        
        # write output file
        for new_line in output_lines:
            outfile.write(new_line)
        
        #close all files
        outfile.close()
        
        #print 'XYZ OUTPUT LINES:', len (output_lines)
        #print 'XYZ INPUT LINES', len (all_lines), '\n\n'        
        return    
    
    def gms_conf_extract(self, system_name, gmspath, output_dir_path, numconf):

        #open input file and read all lines
        with open(gmspath) as gmsfile:
            all_lines = [line for line in gmsfile] 

        # set output array
        output_lines = []
        
        #search the lines for tags which define start and stop of a conformer
        search_string = '$$$$'
        conf_count = 0
        
        for line in all_lines:
            #do we have as many as required?
            if conf_count > numconf:
                conf_count = numconf
                break
            # is this the beginning of a conformer?
            if search_string in line :
                if conf_count <= numconf:
                    conf_count +=1
                if conf_count <= numconf:
                    output_lines.append(line)
                    #print 'FOUND CONF#', conf_count
                
            else:
                output_lines.append(line) 

        # create an output file path
        filename = system_name + '_' + str(conf_count) + '_conformers.gms'
        out_file_path = os.path.join(output_dir_path, filename)

        silentremove(out_file_path) # in case it already exists

        #open output file
        outfile = open(out_file_path, 'a')
        
        # write output file
        for new_line in output_lines:
            outfile.write(new_line)
        
        #close all files
        outfile.close()
        
        #print 'GMS OUTPUT LINES:', len (output_lines)
        #print 'GMS INPUT LINES', len (all_lines), '\n\n'
        return
    
    

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def get_receptor_list(receptor_dir):

    os.chdir(receptor_dir)
    receptor_list = glob.glob('*')
    receptor_list.sort()
    os.chdir(initial_path)

    return receptor_list

def extract_complex(run_var, cpx_dir, receptor_to_process, first_line):

    print '\nExtracting Complex Data \n'

    type_var = 'complex'

    receptor_names = []

    os.chdir(cpx_dir)
    receptor_list = glob.glob('*')
    receptor_list.sort()
    os.chdir(initial_path)

    if receptor_to_process is not 'all':
       if receptor_to_process in receptor_list:
           receptor_names.append(receptor_to_process)
           cpx_out_file = receptor_to_process + '_' + run_var + '_' + type_var + '.csv'
       else:
           print '\nComplex directory for supplied receptor name %s not found' %receptor_to_process
           sys.exit()
    else:

        receptor_names = receptor_list

        prepend_name = ''
        for receptor_name in receptor_names:
            prepend_name = prepend_name + receptor_name + '_'
       
        cpx_out_file = prepend_name + run_var + '_' + type_var + '.csv'

    silentremove(cpx_out_file) # in case it already exists

    ccsv_handle = open(cpx_out_file, 'a')
    ccsv_handle.write(first_line)

    for receptor_name in receptor_names:

        top_cpx_dir = os.path.join(cpx_dir, receptor_name) 
    
        subdir_list = get_immediate_subdirectories(top_cpx_dir)
        subdir_list.sort()
  
        for member in subdir_list:
            member_dir = os.path.join(top_cpx_dir, member)
            os.chdir(member_dir)
            inp_file_list = glob.glob('*.inp')
            os.chdir(initial_path)
            inp_file = inp_file_list[0]
            this_sum_file = inp_file.replace(".inp", ".summary.out") 
            filename = os.path.join(top_cpx_dir, member, this_sum_file)

            reader_obj = Vm2SummaryReader(filename)
    
            this_line = run_var + ','
            this_line = this_line + type_var + ','
            this_line = this_line + member + ',' 
            this_line = this_line + str(reader_obj.FE) + ',' 
            this_line = this_line + str(reader_obj.AvgE) + ',' 
            this_line = this_line + str(reader_obj.S) + ',' 
            this_line = this_line + str(reader_obj.U) + ',' 
            this_line = this_line + str(reader_obj.W) + ',' 
            this_line = this_line + str(reader_obj.HO_PE) + ',' 
            this_line = this_line + str(reader_obj.PB) + ',' 
            this_line = this_line + str(reader_obj.SA) + ',' 
            this_line = this_line + str(reader_obj.Valence) + ',' 
            this_line = this_line + str(reader_obj.Coulomb) + ',' 
            this_line = this_line + str(reader_obj.VdW) + ',' 
            this_line = this_line + str(reader_obj.VdW6) + ',' 
            this_line = this_line + str(reader_obj.VdW12) + ','
            this_line = this_line + str(reader_obj.Bond) + ',' 
            this_line = this_line + str(reader_obj.Angle) + ',' 
            this_line = this_line + str(reader_obj.Pdihed) + ',' 
            this_line = this_line + str(reader_obj.Idihed) + ',' 
            this_line = this_line + str(reader_obj.Tether) + ',' 
            this_line = this_line + str(reader_obj.Runtime) + ',' 
            this_line = this_line + str(reader_obj.WallTime) + ',' 
            this_line = this_line + str(reader_obj.FeConv) + ',' 
            this_line = this_line + str(reader_obj.CrashStatus) 
            this_line = this_line + '\n'
            ccsv_handle.write(this_line)
    
    ccsv_handle.close()
    

def extract_ligand(run_var, lig_dir, first_line):

    print '\nExtracting Ligand Data\n'
    
    type_var = 'ligand'
    lig_out_file = run_var + '_' + type_var + '.csv'
    silentremove(lig_out_file) # in case it already exists
    lig_subdir_list = get_immediate_subdirectories(lig_dir)
    lig_subdir_list.sort()
    
    lcsv_handle = open(lig_out_file, 'a')
    lcsv_handle.write(first_line)
    
    for member in lig_subdir_list:
        os.chdir(lig_dir + '/' + member)
        inp_file_list = glob.glob('*.inp')
        os.chdir(initial_path)
        inp_file = inp_file_list[0]
        this_sum_file = inp_file.replace(".inp", ".summary.out") 
        filename = os.path.join(lig_dir, member, this_sum_file)
        lig_reader_obj = Vm2SummaryReader(filename)
    
        this_line = run_var + ','
        this_line = this_line + type_var + ','
        this_line = this_line + member + ',' 
        this_line = this_line + str(lig_reader_obj.FE) + ',' 
        this_line = this_line + str(lig_reader_obj.AvgE) + ',' 
        this_line = this_line + str(lig_reader_obj.S) + ',' 
        this_line = this_line + str(lig_reader_obj.U) + ',' 
        this_line = this_line + str(lig_reader_obj.W) + ',' 
        this_line = this_line + str(lig_reader_obj.HO_PE) + ',' 
        this_line = this_line + str(lig_reader_obj.PB) + ',' 
        this_line = this_line + str(lig_reader_obj.SA) + ',' 
        this_line = this_line + str(lig_reader_obj.Valence) + ',' 
        this_line = this_line + str(lig_reader_obj.Coulomb) + ',' 
        this_line = this_line + str(lig_reader_obj.VdW) + ',' 
        this_line = this_line + str(lig_reader_obj.VdW6) + ',' 
        this_line = this_line + str(lig_reader_obj.VdW12) + ','
        this_line = this_line + str(lig_reader_obj.Bond) + ',' 
        this_line = this_line + str(lig_reader_obj.Angle) + ',' 
        this_line = this_line + str(lig_reader_obj.Pdihed) + ',' 
        this_line = this_line + str(lig_reader_obj.Idihed) + ',' 
        this_line = this_line + str(lig_reader_obj.Tether) + ',' 
        this_line = this_line + str(lig_reader_obj.Runtime) + ',' 
        this_line = this_line + str(lig_reader_obj.WallTime) + ',' 
        this_line = this_line + str(lig_reader_obj.FeConv) + ',' 
        this_line = this_line + str(lig_reader_obj.CrashStatus) 
        this_line = this_line + '\n'
        lcsv_handle.write(this_line)
    
    lcsv_handle.close()


def extract_receptor(run_var, receptor_dir, receptor_to_process, first_line):

    print '\nExtracting Receptor Data\n'
    
    type_var = 'host'

    receptor_names = []

    os.chdir(receptor_dir)
    receptor_list = glob.glob('*')
    receptor_list.sort()
    os.chdir(initial_path)

    if receptor_to_process is not 'all':
       if receptor_to_process in receptor_list:
           receptor_names.append(receptor_to_process)
           rec_out_file = receptor_to_process + '_' + run_var + '_' + type_var + '.csv'
       else:
           print '\nComplex directory for supplied receptor name %s not found' %receptor_to_process
           sys.exit()
    else:
        receptor_names = receptor_list

        prepend_name = ''
        for receptor_name in receptor_names:
            prepend_name = prepend_name + receptor_name + '_'

        rec_out_file = prepend_name +  run_var + '_' + type_var + '.csv'

    silentremove(rec_out_file) # in case it already exists
    
    pcsv_handle = open(rec_out_file, 'a')
    pcsv_handle.write(first_line)

    for receptor_name in receptor_names:

        top_rec_dir = os.path.join(receptor_dir, receptor_name) 
    
        os.chdir(top_rec_dir) 
        inp_file_list = glob.glob('*.inp')
        os.chdir(initial_path)
        inp_file = inp_file_list[0]
        rec_sum_file_name = inp_file.replace(".inp", ".summary.out") 
        filename = os.path.join(top_rec_dir, rec_sum_file_name)
    
        prot_reader_obj = Vm2SummaryReader(filename)
    
        this_line = run_var + ','
        this_line = this_line + type_var + ','
        this_line = this_line + receptor_name + ',' 
        this_line = this_line + str(prot_reader_obj.FE) + ',' 
        this_line = this_line + str(prot_reader_obj.AvgE) + ',' 
        this_line = this_line + str(prot_reader_obj.S) + ',' 
        this_line = this_line + str(prot_reader_obj.U) + ',' 
        this_line = this_line + str(prot_reader_obj.W) + ',' 
        this_line = this_line + str(prot_reader_obj.HO_PE) + ',' 
        this_line = this_line + str(prot_reader_obj.PB) + ',' 
        this_line = this_line + str(prot_reader_obj.SA) + ',' 
        this_line = this_line + str(prot_reader_obj.Valence) + ',' 
        this_line = this_line + str(prot_reader_obj.Coulomb) + ',' 
        this_line = this_line + str(prot_reader_obj.VdW) + ',' 
        this_line = this_line + str(prot_reader_obj.VdW6) + ',' 
        this_line = this_line + str(prot_reader_obj.VdW12) + ','
        this_line = this_line + str(prot_reader_obj.Bond) + ',' 
        this_line = this_line + str(prot_reader_obj.Angle) + ',' 
        this_line = this_line + str(prot_reader_obj.Pdihed) + ',' 
        this_line = this_line + str(prot_reader_obj.Idihed) + ',' 
        this_line = this_line + str(prot_reader_obj.Tether) + ',' 
        this_line = this_line + str(prot_reader_obj.Runtime) + ',' 
        this_line = this_line + str(prot_reader_obj.WallTime) + ',' 
        this_line = this_line + str(prot_reader_obj.FeConv) + ',' 
        this_line = this_line + str(prot_reader_obj.CrashStatus) 
        this_line = this_line + '\n'
        pcsv_handle.write(this_line)
    
    pcsv_handle.close()


def extract_complex_conformer_files(run_var, cpx_dir, receptor_to_process, output_dir, numconf):

    print '\nGathering Complex Conformer Files \n'

    conf_extractor = Vm2ConformerExtractor()

    receptor_names = []

    os.chdir(cpx_dir)
    receptor_list = glob.glob('*')
    receptor_list.sort()
    os.chdir(initial_path)

    if receptor_to_process is not 'all':
       if receptor_to_process in receptor_list:
           receptor_names.append(receptor_to_process)
       else:
           print '\nComplex directory for supplied receptor name %s not found' %receptor_to_process
           sys.exit()
    else:
        receptor_names = receptor_list

    for receptor_name in receptor_names:

        top_cpx_dir = os.path.join(cpx_dir, receptor_name) 
    
        subdir_list = get_immediate_subdirectories(top_cpx_dir)
        subdir_list.sort()
  
        for member in subdir_list:

            member_dir = os.path.join(top_cpx_dir, member)
            os.chdir(member_dir)
            inp_file_list = glob.glob('*.inp')
            os.chdir(initial_path)
            inp_file = inp_file_list[0]
            basename = inp_file.split('.')[0]

            # mol2 file
            this_conf_file = inp_file.replace(".inp", ".mol2") 
            filename = os.path.join(top_cpx_dir, member, this_conf_file)
            if os.path.isfile(filename):
                conf_extractor.mol2_conf_extract(basename, filename, output_dir, numconf)

            # sdf file
            this_conf_file = inp_file.replace(".inp", ".sdf") 
            filename = os.path.join(top_cpx_dir, member, this_conf_file)
            if os.path.isfile(filename):
                conf_extractor.sdf_conf_extract(basename, filename, output_dir, numconf)

            # pdb file
            this_conf_file = inp_file.replace(".inp", ".pdb") 
            filename = os.path.join(top_cpx_dir, member, this_conf_file)
            if os.path.isfile(filename):
                conf_extractor.pdb_conf_extract(basename, filename, output_dir, numconf)

            # xyz file
            this_conf_file = inp_file.replace(".inp", ".xyz") 
            filename = os.path.join(top_cpx_dir, member, this_conf_file)
            if os.path.isfile(filename):
                conf_extractor.xyz_conf_extract(basename, filename, output_dir, numconf)

            # gms file
            this_conf_file = inp_file.replace(".inp", ".gms") 
            filename = os.path.join(top_cpx_dir, member, this_conf_file)
            if os.path.isfile(filename):
                conf_extractor.gms_conf_extract(basename, filename, output_dir, numconf)


def extract_ligand_conformer_files(run_var, lig_dir, output_dir, numconf):

    print '\nGathering Ligand Conformer Files \n'

    conf_extractor = Vm2ConformerExtractor()
    
    lig_subdir_list = get_immediate_subdirectories(lig_dir)
    lig_subdir_list.sort()
    
    for member in lig_subdir_list:

        os.chdir(lig_dir + '/' + member)
        inp_file_list = glob.glob('*.inp')
        os.chdir(initial_path)
        inp_file = inp_file_list[0]
        basename = inp_file.split('.')[0]

        # mol2 file
        this_conf_file = inp_file.replace(".inp", ".mol2") 
        filename = os.path.join(lig_dir, member, this_conf_file)
        if os.path.isfile(filename):
            conf_extractor.mol2_conf_extract(basename, filename, output_dir, numconf)

        # sdf file
        this_conf_file = inp_file.replace(".inp", ".sdf") 
        filename = os.path.join(lig_dir, member, this_conf_file)
        if os.path.isfile(filename):
            conf_extractor.sdf_conf_extract(basename, filename, output_dir, numconf)

        # pdb file
        this_conf_file = inp_file.replace(".inp", ".pdb") 
        filename = os.path.join(lig_dir, member, this_conf_file)
        if os.path.isfile(filename):
            conf_extractor.pdb_conf_extract(basename, filename, output_dir, numconf)

        # xyz file
        this_conf_file = inp_file.replace(".inp", ".xyz") 
        filename = os.path.join(lig_dir, member, this_conf_file)
        if os.path.isfile(filename):
            conf_extractor.xyz_conf_extract(basename, filename, output_dir, numconf)

        # gms file
        this_conf_file = inp_file.replace(".inp", ".gms") 
        filename = os.path.join(lig_dir, member, this_conf_file)
        if os.path.isfile(filename):
            conf_extractor.gms_conf_extract(basename, filename, output_dir, numconf)


def extract_receptor_conformer_files(run_var, receptor_dir, receptor_to_process, output_dir, numconf):

    print '\nGathering Receptor Conformer Files\n'

    conf_extractor = Vm2ConformerExtractor()

    receptor_names = []

    os.chdir(receptor_dir)
    receptor_list = glob.glob('*')
    receptor_list.sort()
    os.chdir(initial_path)

    if receptor_to_process is not 'all':
       if receptor_to_process in receptor_list:
           receptor_names.append(receptor_to_process)
       else:
           print '\nComplex directory for supplied receptor name %s not found' %receptor_to_process
           sys.exit()
    else:
        receptor_names = receptor_list

    for receptor_name in receptor_names:

        top_rec_dir = os.path.join(receptor_dir, receptor_name) 
    
        os.chdir(top_rec_dir) 
        inp_file_list = glob.glob('*.inp')
        os.chdir(initial_path)
        inp_file = inp_file_list[0]
        basename = inp_file.split('.')[0]

        # mol2 file
        this_conf_file = inp_file.replace(".inp", ".mol2") 
        filename = os.path.join(receptor_dir, receptor_name, this_conf_file)
        if os.path.isfile(filename):
            conf_extractor.mol2_conf_extract(basename, filename, output_dir, numconf)

        # sdf file
        this_conf_file = inp_file.replace(".inp", ".sdf") 
        filename = os.path.join(receptor_dir, receptor_name, this_conf_file)
        if os.path.isfile(filename):
            conf_extractor.sdf_conf_extract(basename, filename, output_dir, numconf)

        # pdb file
        this_conf_file = inp_file.replace(".inp", ".pdb") 
        filename = os.path.join(receptor_dir, receptor_name, this_conf_file)
        if os.path.isfile(filename):
            conf_extractor.pdb_conf_extract(basename, filename, output_dir, numconf)

        # xyz file
        this_conf_file = inp_file.replace(".inp", ".xyz") 
        filename = os.path.join(receptor_dir, receptor_name, this_conf_file)
        if os.path.isfile(filename):
            conf_extractor.xyz_conf_extract(basename, filename, output_dir, numconf)

        # gms file
        this_conf_file = inp_file.replace(".inp", ".gms") 
        filename = os.path.join(receptor_dir, receptor_name, this_conf_file)
        if os.path.isfile(filename):
            conf_extractor.gms_conf_extract(basename, filename, output_dir, numconf)

 
def get_id(line):
    components = line.split(',')
    line_id = components[2]
    #print 'Line ID', line_id
    return line_id

def get_DelG_exp(line):
        components = line.split(',')
        delG = components[1]
        clean_delG = delG.strip()
        return clean_delG

def get_FE(line):
    components = line.split(',')
    this_FE_str = components[3]  
    #print 'FE', this_FE_str
    return float(this_FE_str)
    
def get_avgE(line):
    components = line.split(',')
    this_avE_str = components[4]  
    #print 'Avg E', this_avE_str
    return float(this_avE_str)
    
def get_FeConv(line):
    components = line.split(',')
    this_feconv = components[23].strip()
    return this_feconv
    
def get_CrashStatus(line):
    components = line.split(',')
    this_crash_status = components[24].strip()
    return this_crash_status

def get_cpx_lig(cpx):
    n = cpx.find('_')
    cpx_lig = cpx[n+1:]
    return cpx_lig

def get_cpx_rec(cpx):
    n = cpx.find('_')
    cpx_rec = cpx[:n]
    return cpx_rec

def get_exp_id(line):
    components = line.split(',')
    exp_line_id = components[0].strip()
    return exp_line_id

def get_exp_lig(line):
    components = line.split(',')
    exp_line_id = components[0].strip()
    return exp_line_id

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: 
        if e.errno != errno.ENOENT: 
            raise 



if __name__ == "__main__":
    
    # set some defaults

    data_source_argument = None
    data_source = ''

    calc_type_argument = None
    run_var = None

    receptor_name_argument = None
    receptor_name = 'all'
    
    reference_ligand_argument = None
    reference_lig = None 

    get_confs_argument = None
    numconf = 8 

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "hd:c:n:l:g:",
                     ["help","data=","calctype=","receptorname=","refligand=","getconfs="])

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
        elif opt in ("-c", "--calctype"):
           calc_type_argument = arg
        elif opt in ("-n", "--receptorname"):
           receptor_name_argument = arg
        elif opt in ("-l", "--refligand"):
           reference_ligand_argument = arg


    # Set control variables based on command line arguments

    if data_source_argument is not None:

        if data_source_argument == 'reference':
           data_source = 'reference'
        elif data_source_argument == 'new':
           data_source = ''
        else:
            print '\nData source argument %s is not recognized!' %data_source_argument
            print 'Choose from: reference or new'
            sys.exit()

    if calc_type_argument is not None:

        if calc_type_argument == 'fast_vm2_rndm':
           run_var = calc_type_argument 
        elif calc_type_argument == 'vm2_rndm':
           run_var = calc_type_argument 
        elif calc_type_argument == 'fast_vm2_single':
           run_var = calc_type_argument 
        elif calc_type_argument == 'vm2_single':
           run_var = calc_type_argument 
        else:
            print '\nCalcntype argument %s is not recognized!' %calc_type_argument
            print 'Choose from: fast_vm2_rndm or vm2_rndm or fast_vm2_single, or vm2_single'
            sys.exit()

    else:
        print '\nA calctype argument is required through -c or --calctype!'
        print 'Choose from: fast_vm2_rndm, vm2_rndm, fast_vm2_single, or vm2_single'
        sys.exit()

    print '\nThe calculation type is %s\n' %run_var 

    if receptor_name_argument is not None:
        receptor_name = receptor_name_argument

    print '\nThe receptor to process is %s\n' %receptor_name 

    if reference_ligand_argument is not None:
        reference_lig = reference_ligand_argument

    print '\nThe reference ligand is %s\n' %reference_lig

    if get_confs_argument is not None:
        numconf = int(get_confs_argument)
    
    print '\nNumber of conformers to be extracted is %s\n' %numconf


    # construct paths

    initial_path = os.getcwd()
    rel_run_path = 'run/2_vm2_runs'
    base_results_dir = os.path.join('..', rel_run_path, data_source, run_var)
    print '\nResults will be taken from %s\n' %base_results_dir

    cpx_dir = os.path.join(base_results_dir, 'complexes')
    lig_dir = os.path.join(base_results_dir, 'ligands')
    receptor_dir = os.path.join(base_results_dir, 'hosts')
    
    # construct first line of each csv file    

    first_line = "run, type, Ident, FE, AvgE, S, U, W, HO_PE, PB, SA, " + \
                 "Valence, Coulomb, VdW, VdW6, VdW12, Bond, Angle, Pdihed, Idihed, " + \
                 "Tether, RunTime, WallTime, Converged, Crashed\n"    
    
    # create the csv files containing complex, ligand, and receptor energies

    receptor_list = get_receptor_list(receptor_dir)

    extract_complex(run_var, cpx_dir, receptor_name, first_line)
    extract_ligand(run_var, lig_dir, first_line)
    extract_receptor(run_var, receptor_dir, receptor_name, first_line)

    # gather conformer files trimming to numconf conformers. Also output single
    # conformer files.

    numconf = 8

    os.chdir(initial_path)
    if not os.path.exists('conformers'):
        os.mkdir('conformers')

    os.chdir('conformers')
    if not os.path.exists(run_var):
        os.mkdir(run_var)

    os.chdir(run_var)

    if not os.path.exists('complexes'):
        os.mkdir('complexes')
    if not os.path.exists('ligands'):
        os.mkdir('ligands')
    if not os.path.exists('hosts'):
        os.mkdir('hosts')

    os.chdir(initial_path)

    output_dir = os.path.join(initial_path, 'conformers', run_var, 'complexes')
    extract_complex_conformer_files(run_var, cpx_dir, receptor_name, output_dir, numconf)

    output_dir = os.path.join(initial_path, 'conformers', run_var, 'ligands')
    extract_ligand_conformer_files(run_var, lig_dir, output_dir, numconf)

    output_dir = os.path.join(initial_path, 'conformers', run_var, 'hosts')
    extract_receptor_conformer_files(run_var, receptor_dir, receptor_name, output_dir, numconf)

    if run_var != 'fast_vm2_single':

        numconf = 1

        output_dir = os.path.join(initial_path, 'conformers', run_var, 'complexes')
        extract_complex_conformer_files(run_var, cpx_dir, receptor_name, output_dir, numconf)

        output_dir = os.path.join(initial_path, 'conformers', run_var, 'ligands')
        extract_ligand_conformer_files(run_var, lig_dir, output_dir, numconf)

        output_dir = os.path.join(initial_path, 'conformers', run_var, 'hosts')
        extract_receptor_conformer_files(run_var, receptor_dir, receptor_name, output_dir, numconf)
        
    # calculate summary containing deltaG's etc.

    recname_run_var = run_var

    if receptor_name is not 'all':
        recname_run_var = receptor_name + '_' + run_var
    else:
        prepend_name = ''
        for receptor in receptor_list:
            prepend_name = prepend_name + receptor + '_'

        recname_run_var = prepend_name + run_var

    deltas_output_file = recname_run_var + '_SUMMARY.csv'
    silentremove(deltas_output_file) # in case it already exists
    
    # get all files in this dir

    complex_out = recname_run_var + '_complex.csv'
    ligand_out = run_var + '_ligand.csv'
    receptor_out = recname_run_var + '_host.csv'

    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if complex_out == f:
            cpx_infile = f
        if ligand_out in f:
            lig_infile = f
        if receptor_out == f:
            rec_infile = f
        if 'experimental_data' in f:
            exp_infile = f    
    
    # open the files
    cpx_file = open(cpx_infile, 'r')
    lig_file = open(lig_infile, 'r')
    rec_file = open(rec_infile, 'r')
    exp_file = open(exp_infile, 'r')
    
    # read the files
    cpx_lines = cpx_file.readlines()
    lig_lines = lig_file.readlines()
    rec_lines = rec_file.readlines()
    exp_lines = exp_file.readlines()
    
    # write the output header

    if reference_lig:
        first_line = "Ident, Complex G, Host G, Ligand G, Exp DeltaG, Calc Ref DelG, Error, " + \
                     "Abs Error, Calculated DeltaG, Error, Abs Error, Converged, Crashed\n"
    else:
        first_line = "Ident, Complex G, Host G, Ligand G, Exp DeltaG, Calculated DeltaG, Error, " + \
                     "Abs Error, Converged, Crashed\n"

    outfile = open(deltas_output_file, 'a')
    outfile.write(first_line)
    
    if reference_lig:

        # find reference cpxG, ligG, and experimental cpx G

        for this_exp_line in exp_lines:
            exp_id = get_exp_id(this_exp_line)
            exp_lig = get_cpx_lig(exp_id)
            cpx_rec = get_cpx_rec(exp_id)
            if reference_lig == exp_lig:
                if receptor_name == 'all' or cpx_rec == receptor_name:
                   ref_exp_E = get_DelG_exp(this_exp_line)
                   break

        for this_cpx_line in cpx_lines:
            cpx_id =  get_id(this_cpx_line)
            if cpx_id  == ' Ident':
                continue
            cpx_lig = get_cpx_lig(cpx_id)
            if reference_lig == cpx_lig and cpx_id == exp_id:
                ref_cpx_E = get_FE(this_cpx_line)
                cpx_rec = get_cpx_rec(cpx_id)
                break

        for this_rec_line in rec_lines:
            rec_id = get_id(this_rec_line)
            if rec_id == cpx_rec:
                ref_rec_E = get_FE(this_rec_line)

        for this_lig_line in lig_lines:
            lig_id = get_id(this_lig_line)
            if lig_id  == ' Ident':
                continue
            if reference_lig == lig_id:
                ref_lig_E = get_FE(this_lig_line)
                break

        # calculate reference constant        
        ref_const = (-1.0 * float(ref_cpx_E)) + float(ref_rec_E) + float(ref_lig_E) + float(ref_exp_E)
    
    # match lines by ligand id, calculate and output deltas

    for this_cpx_line in cpx_lines:

        cpx_id =  get_id(this_cpx_line)

        if cpx_id  == ' Ident':
            continue

        cpx_lig = get_cpx_lig(cpx_id)

        cpx_feconv = get_FeConv(this_cpx_line)
        cpx_crash_status = get_CrashStatus(this_cpx_line)

        for this_lig_line in lig_lines:
            lig_id = get_id(this_lig_line)

            if cpx_lig == lig_id:

                lig_feconv = get_FeConv(this_lig_line)
                lig_crash_status = get_CrashStatus(this_lig_line)

                for this_rec_line in rec_lines:
                    rec_id = get_id(this_rec_line)

                    # match the identifiers ()

                    length = len(rec_id)

                    if rec_id == cpx_id[:length]:
                        cpx_FE = get_FE(this_cpx_line)
                        cpx_avgE = get_avgE(this_cpx_line)

                        lig_FE = get_FE(this_lig_line)
                        lig_avgE = get_avgE(this_lig_line)

                        rec_FE = get_FE(this_rec_line)
                        rec_avgE = get_avgE(this_rec_line)

                        deltaG = cpx_FE - lig_FE - rec_FE
                        deltaE = cpx_avgE - lig_avgE - rec_avgE

                        rec_feconv = get_FeConv(this_rec_line)
                        rec_crash_status = get_CrashStatus(this_rec_line)

                        # check for the experimental delG equal to the complex name

                        for this_exp_line in exp_lines:

                            exp_id = get_exp_id(this_exp_line)

                            if cpx_id == exp_id:
                                this_exp_delG = get_DelG_exp(this_exp_line)

                                if reference_lig:
                                    # calculate reference delta G
                                    calc_ref_delg = cpx_FE - lig_FE - rec_FE + ref_const
                                    error1 = calc_ref_delg - float(this_exp_delG)

                                error2 = deltaG - float(this_exp_delG)
                                break # exit exp lines loop

                        # If a calculation bombed end up with zero energies

                        if cpx_FE == 0.0 or lig_FE == 0.0 or rec_FE == 0.0:
                           deltaG = 0.0
                           calc_ref_delg = 0.0
                           error1 = 0.0
                           error2 = 0.0

                        if cpx_avgE == 0.0 or lig_avgE == 0.0 or rec_avgE == 0.0:
                           deltaE = 0.0

                        # If no experiment to compare no error either

                        if float(this_exp_delG) == 0.0:
                            error1 = 0.0
                            error2 = 0.0

                        # Indicate convergence failure or crash 

                        feconv = 'no'
                        if cpx_feconv == 'yes' and lig_feconv == 'yes' and rec_feconv == 'yes':
                            feconv = 'yes'

                        crash = 'no'
                        if cpx_crash_status == 'yes' or  lig_crash_status == 'yes' or rec_crash_status == 'yes':
                            crash = 'yes'

                        # write new deltas line

                        if reference_lig:
                            new_line =  (cpx_id + ',' + 
                                         str(cpx_FE) + ',' +
                                         str(rec_FE) + ',' +
                                         str(lig_FE) + ',' +
                                         str(this_exp_delG) + ',' +
                                         str(calc_ref_delg) + ',' +
                                         str(error1) + ',' +
                                         str(abs(error1)) + ',' +
                                         str(deltaG) + ',' + 
                                         str(error2) + ',' +
                                         str(abs(error2)) + ',' + 
                                         feconv + ',' + 
                                         crash + '\n' 
                                     )
                        else:
                            new_line =  (cpx_id + ',' + 
                                         str(cpx_FE) + ',' +
                                         str(rec_FE) + ',' +
                                         str(lig_FE) + ',' +
                                         str(this_exp_delG) + ',' +
                                         str(deltaG) + ',' + 
                                         str(error2) + ',' +
                                         str(abs(error2)) + ',' + 
                                         feconv + ',' + 
                                         crash + '\n' 
                                     )
                
                        outfile.write(new_line)
                        break # exit rec lines loop
    
    # close all files
    cpx_file.close()
    lig_file.close()
    rec_file.close()
    exp_file.close()
    outfile.close()
    
    # show results
    summary_string = '\nFound ' + str(len(cpx_lines)-1) + ' complexes\n'
    print summary_string
    
    
