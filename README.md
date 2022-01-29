# SnmpWeb

It is an application developed to use the SNMP service from the web interface. 

## Installation

- Tested on Debian based systems.

- Snmp service must be installed and active in the system. 

- for Linux:

  `sudo apt install snmp snmpd snmp-mibs-downloader`

  `service snmpd start`

- You should replace the /etc/snmp/snmpd.conf file on the target device with the snmpd.conf file I gave you. (SnmpWeb/snmpd.conf) 

- Installing necessary python modules: 

  `pip install -r requirements.txt`

- To create the database and tables, run the following commands. (python or python3) 

  `python manage.py makemigrations`

  `python manage.py migrate`

## Usage
- Run this command. (python or python3) 

  `python manage.py runserver`

- You can use the application by entering the address http://127.0.0.1:8000/
