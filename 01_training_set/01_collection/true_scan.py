
# coding: utf-8

# In[1]:

import qctoolkit as qtk
import numpy as np
import ast


# In[2]:

log = qtk.Logger('logs/algaas_333_02.db')
mol_base = qtk.Molecule('xyz/gaas_2.xyz')
mol_base.extend([3,3,3])
mol_base.name = 'gaas_ref'
ccs = qtk.CCS(mol_base, 'ccs.yml')


# In[3]:

entries = log.list(has_data=True, order='descent')[1:500:10]
mols = []
for e in entries:
    try:
        name = e.comment.split("'")[1]
    except:
        name = e.comment
    coord = ast.literal_eval(e.content)
    mol = ccs.generate(**coord)
    mol.name = name
    mols.append(mol)
print mols


# In[4]:

qmsetting = {
    'program': 'abinit',
    'kmesh': [3, 3, 3],
    'band_scan': [
     [20, 20],
     [[1.0, 0.0, 0.5], # L
      [0.0, 0.0, 0.0],   # Gamma
      [0.0, 1.0, 1.0],   # X
     ]],
    'threads': 6,
    'omp': 4,
    'ks_states': 16,
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

