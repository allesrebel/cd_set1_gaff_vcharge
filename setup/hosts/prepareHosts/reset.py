import glob, os

filenames = glob.glob('*_vm2*')

filenames += glob.glob('*mol2')
filenames += glob.glob('*inpcrd')
filenames += glob.glob('*prmtop')


filenames += ['a-cyclodex_runAc.log','run_prepareHosts.out']

for filename in filenames:
    if os.path.exists(filename):
        os.system('rm %s' % filename)
