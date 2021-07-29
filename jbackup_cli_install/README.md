jbackup_installer
=====
Overview
-----
    installation of the jbackup-client automatically
      - install Python
      - install pip
      - install xtrabackup
      - install mysql-connector-python
      - install ConfigParser
      - install jbackup
      - set /etc/logrotate.d/jbackup
      - set /etc/init.d/jbackupd
        (if these are not exists)

Usage  
-----
    jbackup_installer [ install | uninstall | update | check ]
    
Option
-----
    install   - install jbackup client.
    uninstall - uninstall jbackup client.
    update    - update jbackup-cli.
    check     - check the installation.

Initial Operation
-----
    user% sudo su -
    root# bash
    root# curl -kL ${URL}/jbackup_installer -o /tmp/jbackup_installer && sh /tmp/jbackup_installer

    
After Installation
-----
    root# jbackup_installer [ install | uninstall | update | check ]
    root# /etc/init.d/jbackupd [ start | stop | status ]
