from setuptools import setup, find_packages
exec(open('jbackup/_version.py').read())

setup(
    name='jbackup_cli',
    version=__version__,
    description='MySQL Backup (Jbackup)',
    url='https://github.com/lejpower/Jbackup.git',
    
    # Author details
    author='Uijun Lee',
    author_email='lejpower@gmail.com',
     
    packages=find_packages(),
    install_requires=['mysql-connector-python','requests'],
    dependency_links=['http://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-2.0.3.zip#md5=9fda73a7f69e769e6a545c98b6739514'],
    entry_points={
        'console_scripts':
            'jbackup = jbackup.main:cli_main'
    },
    zip_safe=False,
    classifiers=[
          'Development Status :: 3 - Alpha',
	  'Version :: 0.1.7',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Linux :: CentOS',
          'Operating System :: Linux :: Ubuntu',
          'Programming Language :: Python',
    ],
)
