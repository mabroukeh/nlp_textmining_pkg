from setuptools import setup, find_packages

packages_list = find_packages('src/main/python', exclude=['test'])
packages_list.extend([])  # needed to force inclusion of py modules in source root
setup(name='nlp-textmining-pkg', # String
      version='0.1', # String vMajor.vMinor
      package_dir={'':'src/main/python'},
      packages=packages_list,
      install_requires=[], # array of string, keep empty in case of application, maintain requirements.txt instead
      # in case of library project, maintain this array with a list of required non-conda libraries
      # assume all conda libraries are installed
      # These libraries will be installed during library deploy process 
     )
