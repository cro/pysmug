
import os
import glob
from distutils.core import setup
from distutils.cmd import Command
from distutils.errors import DistutilsExecError
from distutils.command.sdist import sdist as _sdist

PACKAGE = "pysmug"
DESCRIPTION = "A high-performance python client for the SmugMug API."

VERSION = __import__(PACKAGE).__version__

class epydoc(Command):
  description = "Builds the documentation."
  user_options = []

  def initialize_options(self):
    pass
  
  def finalize_options(self):
    pass
  
  def run(self):
    self.mkpath("doc/html")
    stat = os.system("epydoc --config epydoc.cfg %s/*.py" % (PACKAGE))
    if not stat == 0:
      raise DistutilsExecError("failed to run epydoc")

class sdist(_sdist):
  def run(self):
    self.run_command("epydoc")
    _sdist.run(self)

def datafiles():
  """Returns a list of (path, [files]) to install.
  """
  def _datafiles():
    root = os.path.join("share", "doc", PACKAGE + "-" + VERSION)
    yield (root, ("ChangeLog", "LICENSE.txt", "README"))
    for dn, pattern in (("doc/html", "*"), ("examples", "*.py"), ("tests", "*.py")):
      files = glob.glob(os.path.join(dn, pattern))
      if files:
        yield (os.path.join(root, dn), files)
  return list(_datafiles())

def scripts():
  """Returns a list of script files to install.
  """
  return glob.glob(os.path.join("scripts", "*.py"))

setup(
  name = PACKAGE,
  version = VERSION,
  description = DESCRIPTION,
  author = "Brian Zimmer",
  author_email = "bzimmer@ziclix.com",
  url = "http://code.google.com/p/%s" % (PACKAGE),
  download_url = "http://pypi.python.org/pypi/%s/%s" % (PACKAGE, VERSION),
  packages = [PACKAGE],
  scripts = scripts(),
  data_files = datafiles(),
  platforms = ['any'],
  license = "MIT License",
  classifiers = [
    'Intended Audience :: Developers',
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
  ],
  cmdclass = {"epydoc":epydoc, "sdist":sdist},
)

