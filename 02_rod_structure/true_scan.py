
# coding: utf-8

# In[1]:

import qctoolkit as qtk
import numpy as np
import ast
import os


# In[2]:

mol_base = qtk.Molecule('xyz/gaas_2.xyz')
mol_base.extend([6,1,1], normalize=True)
mol_base.name = 'gaas_ref'
ccs = qtk.CCS(mol_base, 'ccs.yml')
log_file = 'logs/iter_names.db'
log = qtk.Logger(log_file)
mols = []

if os.path.exists(log_file):
    for rec in log.list():
        coord = ast.literal_eval(rec.comment)
        mol = ccs.generate(**coord)
        mol.name = rec.content
        mols.append(mol)
else:
    log = qtk.Logger(log_file)
    #entries = log.list(has_data=True, order='descent')[1:500:10]
    #for e in entries:
    for e in range(1, 1001):
        coord = ccs.random()[1]
        mol = ccs.generate(**coord)
    
        #try:
        #    name = e.comment.split("'")[1]
        #except:
        #    name = e.comment
        #coord = ast.literal_eval(e.content)
        #mol = ccs.generate(**coord)
        mol.name = 'iter_%04d' % e
        log.push(mol.name, comment=str(coord))
        mols.append(mol)

# In[3]:

print mols


# In[4]:

qmsetting = {
    'program': 'abinit',
    'kmesh': [1, 4, 4],
    'band_scan': [
     [10, 10],
     [[1.0, 0.0, 0.5], # L
      [0.0, 0.0, 0.0],   # Gamma
      [0.0, 1.0, 1.0],   # X
     ]],
    'threads': 6,
    'omp': 4,
    'ks_states': 8,
    'save_restart': True,
    'save_density': True,
    'abinit_setting': ['chkprim 0', 'nsym 1'],
}
qmsetting['unfold'] = qmsetting['kmesh']


# In[5]:

inps = [qtk.QMInp(m, **qmsetting) for m in mols]
print inps


# In[6]:

qtk.qmRunAll(inps, 'true', threads=1)

