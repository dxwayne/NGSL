from setuptools import setup, find_packages


with open("README.rst", "r", encoding='utf-8') as fh:
    long_description = fh.read()


setup(name = 'NGSL',
    description      = 'Spectroscic reference star data, tools, documentation',
    long_description = long_description,
    version          = '0.0.1',
    author           = 'Wayne Green, Anthony Rodda, Clarke Yeager',
    author_email     = 'no_reply@gmail.com',
    url              = 'https://dxwayne/NGSL',
    packages         = find_packages(),
    classifiers      = [
       'Development Status :: 3 - Alpha',
       'Environment :: Console',
       'Intended Audience :: Science/Research',
       'Intended Audience :: End Users/Desktop',
       'License :: OSI Approved :: MIT',
       'Operating System :: POSIX :: Linux',
       'Programming Language :: Python :: 3',
       'Programming Language :: C++'
       'Topic :: Scientific/Engineering :: Astronomy',
       'Topic :: Scientific/Engineering :: Physics'
       ]
    )
