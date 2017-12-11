import qctoolkit as qtk
import numpy as np
from glob import glob

outs = []
for o in sorted(glob('true/iter*/*.out')):
  out = qtk.QMOut(o, program='abinit')
  if not np.isnan(out.Et):
    outs.append(out)

R = np.stack([o.molecule.R for o in outs])
Z = np.stack([o.molecule.Z for o in outs])
band = np.stack([o.band for o in outs])
Et = np.array([o.Et for o in outs])

np.savez('data.npz', R=R, Z=Z, band=band, Et=Et)
