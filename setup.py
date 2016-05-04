from distutils.core import setup
import py2exe,shutil,os,PyQt4

py2exe_options = {
        "includes": ["sip"],
        "dll_excludes": ["MSVCP90.dll",],
        "compressed": 1,
        "optimize": 2,
        "ascii": 0,
        "bundle_files": 1,
        }

setup(
      name = 'O2Tool',
      version = '2.1.1',
      windows = [{"script": "O2Tool.py", "icon_resources": [(1, "O2tool.ico")]}], 
      zipfile = None,
      options = {'py2exe': py2exe_options}
      )


