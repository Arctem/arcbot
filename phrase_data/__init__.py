import os
import glob
import imp
import phrase_maker.phrase_maker as phrase_maker

for module in glob.glob(os.path.dirname(__file__) + "/*.py"):
    if '__init__.py' in module:
        continue

    name = module.split('/')[-1].split('.')[0]
    phrase_maker.load_module(imp.load_source(name, module))

del os
del glob
del imp
del phrase_maker
