#!/usr/bin/env python
"""
Command-line unit test runner for mayapy.
This can be used to run tests from a commandline environment like on a build
server.
Usage:
python runmayatests.py -m 2016
"""
import argparse
import errno
import os
import platform
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid

_current_dir = os.path.abspath(os.path.join(os.path.realpath(__file__), '..'))
UNITTEST_PATH = os.path.join(_current_dir, 'mayaunittest.py')
CLEAN_MAYA_APP_DIR = os.path.join(_current_dir, '_clean_maya_app_dir')

# Add unittest path to system paths
if UNITTEST_PATH not in sys.path:
    sys.path.insert(0, UNITTEST_PATH)


def get_maya_location(maya_version):
    """Get the location where Maya is installed.
    :param maya_version: The maya version number.
    :type maya_version: int
    :return: The path to where Maya is installed.
    """
    if 'MAYA_LOCATION' in os.environ.keys():
        return os.environ['MAYA_LOCATION']
    if platform.system() == 'Windows':
        return 'C:/Program Files/Autodesk/Maya{0}'.format(maya_version)
    elif platform.system() == 'Darwin':
        path = '/Applications/Autodesk/maya{0}/Maya.app/Contents'
        return path.format(maya_version)
    else:
        location = '/usr/autodesk/maya{0}'.format(maya_version)
        if maya_version < 2016:
            # Starting Maya 2016, the default install directory name changed.
            location += '-x64'
        return location


def mayapy(maya_version, maya_location=None):
    """Get the mayapy executable path.
    :param maya_version: The maya version number.
    :type maya_version: int
    :param maya_location: Optional path to a maya version directory to find
                          the mayapy file.
    :type maya_location: String
    :return: The mayapy executable path.
    """
    def mayapy_path(maya):
        python_exe = '{0}/bin/mayapy'.format(maya)
        if platform.system() == 'Windows':
            python_exe += '.exe'
        return python_exe

    # Attempt to find the maya version location
    maya = maya_location if maya_location else get_maya_location(maya_version)
    python_exe = mayapy_path(maya)

    # If it's not found, prompt the user to provide a correct path manually
    while not os.path.isfile(python_exe):
        maya = input('There is no version of Maya located at {0}. \n'
                     'Please select a valid Maya directory.\n>'.format(maya))

        python_exe = mayapy_path(maya)

    return python_exe


def create_clean_maya_app_dir(directory=None):
    """Creates a copy of the clean Maya preferences so we can create
    predictable results.

    :param directory: Location to store temporary maya app directory location
    :type directory: string
    :return: The path to the clean MAYA_APP_DIR folder.
    """
    # Location to the temporary maya app dir location
    app_dir = CLEAN_MAYA_APP_DIR

    temp_dir = tempfile.gettempdir()
    # Finds the user temp directory to create a clean maya app dir
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    path = 'maya_app_dir{0}'.format(str(uuid.uuid4()))
    dst = directory if directory else os.path.join(temp_dir, path)

    if os.path.exists(dst):
        shutil.rmtree(dst, ignore_errors=False, onerror=remove_read_only)
    shutil.copytree(app_dir, dst)
    return dst


def remove_read_only(func, path, exc):
    """Called by shutil.rmtree when it encounters a readonly file.
    :param func:
    :param path:
    :param exc:
    """
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise RuntimeError('Could not remove {0}'.format(path))


def grab_directories_to_run_tests(paths=None):
    """If nothing is passed, try running tests found in all dirs in current
    directory. If passed a single string, assume it's relative to the current
    directory. If passed an absolute path, use that

    :param paths: List of paths to test
    :return: List of paths, MAYA_MODULE_PATH concatenated string
    """
    if paths:  # Provided by user
        paths = [os.path.normpath(os.path.realpath(d)) for d in paths]
    else:
        # All possible directories in the current directory
        paths = [os.path.normpath(d) for d in os.listdir(_current_dir)
                 if os.path.isdir(d)
                 and not d.startswith('.')
                 and not d.startswith('_')]
    return ';'.join(paths)
	


def main():
    global UNITTEST_PATH
    # Provide top directory, relative path or project name, or absolute path
    # to test directory
    # Provide maya version if desired, if not found, provide absolute path to
    # maya directory
    parser = argparse.ArgumentParser(description='Runs unit tests for a Maya '
                                     'module')
    parser.add_argument('-m', '--maya',
                        help='Maya version',
                        type=int,
                        default=2016)
    parser.add_argument('-mad', '--maya-app-dir',
                        help='Just create a clean MAYA_APP_DIR and exit')
    parser.add_argument('-dir', '--directory',
                        help='Add optional unit testing directory(ies)',
                        default='',
                        nargs='*')
    parser.add_argument('-m_dir', '--maya_directory',
                        help='Maya directory location')
    parser.add_argument('-t', '--test',
                        default='', 
                        help='Add optional test string')

    pargs = parser.parse_args()

    maya_module_string = grab_directories_to_run_tests(pargs.directory)
    test_str = pargs.test

    # Test whether or not UNNITEST is found before running the testing commands
    while not os.path.isfile(UNITTEST_PATH):
        try:
            UNITTEST_PATH = input('Unit testing python file path '
                                  '(mayaunittest.py) not found.\nProvide the '
                                  'correct location.\n>')
        except Exception:
            raise RuntimeError('You must provide a string directory path.\n')

    cmd = [mayapy(pargs.maya, pargs.maya_directory), UNITTEST_PATH,
           maya_module_string, test_str]

    app_directory = pargs.maya_app_dir
    maya_app_dir = create_clean_maya_app_dir(app_directory)
    # Create clean prefs
    os.environ['MAYA_APP_DIR'] = maya_app_dir
    # Clear out any MAYA_SCRIPT_PATH value so we know we're in a clean env.
    os.environ['MAYA_SCRIPT_PATH'] = ''
    # Run the tests in this module.
    os.environ['MAYA_MODULE_PATH'] = maya_module_string
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        sys.exit(2)
    finally:
        shutil.rmtree(maya_app_dir)


if __name__ == '__main__':
    main()
