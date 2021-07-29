# python_cli (Project name : jbackup)

jbackup - python_cli

<h2>INSTALLATION</h2>
###
<br>
<br>
<h2>DEPENDENCY</h2>
Xtrabackup (https://www.percona.com/software/mysql-database/percona-xtrabackup)<br>
<br>
(CentOS)<br>
root# yum install percona-xtrabackup<br>
<br>
(Ubuntsu)<br>
root# apt-get install percona-xtrabackup<br>
<br>
if you want to install the Python, pip and Xtrabackup, please refer to the manual!<br>
(###)<br>
<br>
root# pip install --allow-all-external mysql-connector-python<br>
<br><br>
(if you can't install mysql-connector-python, please install manually)<br>
root# git clone https://github.com/mysql/mysql-connector-python.git<br>
root# cd mysql-connector-python<br>
root# python ./setup.py build<br>
root# python ./setup.py install<br>
<br>
<br>
<h2>UNINSTALL</h2>
pip uninstall jbackup-cli<br>
<br>
<br>
<h2>DEFAULT CONFIG FILE</h2>
Please edit configuration file as follows<br>
<br>
file : /usr/local/mysql/.cnf/.jbackup.cnf<br>
-----------------<br>
[manageDB]<br>
hostname = ${MANAGE_DB_HOST}<br>
port = ${MANAGE_DB_PORT}<br>
user = ${MANAGE_DB_USER}<br>
password = ${MANAGE_DB_PASSWORD}<br>
[clientDB]<br>
hostname = ${CLIENT_DB_HOST}<br>
port = ${CLIENT_DB_PORT}<br>
user = ${CLIENT_DB_USER}<br>
password = ${CLIENT_DB_PASSWORD}<br>
-----------------<br>
<br>
<br>
<h2>REFERENCE MANUAL</h2>
###
