# coding=utf-8
"""将tcollector.py编译为so文件
"""
import os
import glob
from distutils.core import setup
from Cython.Build import cythonize


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# step1: rename .py to .pyx
tcollector_py = os.path.join(base_dir, 'tcollector.py')
tcollector_pyx = os.path.join(base_dir, 'tcollector.pyx')
os.rename(tcollector_py, tcollector_pyx)

# step2: build .so
setup(name='tcollector',
      ext_modules=cythonize(tcollector_pyx)
      )

# step3: link & replace origin .py with .so
tcollector_so = glob.glob('build/lib.*/*/tcollector.so')[0]
os.symlink(os.path.join(base_dir, 'cython_builder', tcollector_so), tcollector_py)
os.remove(tcollector_pyx)
