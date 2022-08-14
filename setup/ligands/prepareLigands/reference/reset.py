import glob, os

filenames = glob.glob('*_vm2*')

filenames += glob.glob('*mol2')
filenames += glob.glob('*inpcrd')
filenames += glob.glob('*prmtop')


filenames += ['cdset1_ligands_runAc.log','run_prepareLigands.out']

for filename in filenames:
    if os.path.exists(filename):
        os.system('rm %s' % filename)
