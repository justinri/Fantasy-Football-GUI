from cx_Freeze import setup, Executable
import sys, platform, os.path
import matplotlib


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = "Win32Gui"
# base = None

# if sys.platform == "win32":
	# base = "Win32GUI"

execute = [Executable("gui_2.py", base=base)]

# # build_exe_options = {"include_files": ["databases/info_database.db"], "include_msvcr": True, "packages": ["tkinter","matplotlib"]}
build_exe_options = {"include_files": ["databases/", os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'), os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')], 
					 # "include_msvcr": True,
					 "includes": ["numpy.core._methods", "numpy.lib.format", "tkinter","matplotlib"],
					 "excludes":["scipy","PyQt5","PyQt4"]}

setup(name = "Fantasy Tool_Kit",
	  version = "0.1",
	  description = "A GUI tool kit for fantasy football",
	  options = {"build_exe": build_exe_options},
	  executables = execute)
