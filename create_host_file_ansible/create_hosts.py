#!/bin/python
#Script to create hosts file for ansible to automate CEE installation and operations
#Written to be used with python 2.7.5
#Script needs to be place at vFuel, no matter location
#config.yaml needs to be placed at /mnt/cee_config/config.yaml for the script to work
#Execute "python create_hosts.py" for script usage
#If any bug or malfunction is found, please contact me via email

#Author: Miguel Sama Merino (miguel.sama@ericsson.com)
#Version: v2

import yaml
import sys

CONFIG_YAML_PATH = './config.yaml'
FILEPATH = './hosts'

def helpMessage():
	print('[INFO] Tool usage:\n\tIf no VSA: python create_hosts.py -1\n\tIf VSA\n\t\tOne compute: python create_hosts.py 4 (4 reffers to compute-0-4)\n\t\tTwo or more computes: python create_hosts.py 4,5,6 (comma separated)')

#######SCRIPT START#######

if len(sys.argv) != 2:
	helpMessage()
	exit(0)
else:
	vsa_list = sys.argv[1].split(',')
	if vsa_list[0] == str(-1):
		vsa = False
	else:
		vsa = True
	
try:
	with open(FILEPATH, 'w') as hosts_file, open(CONFIG_YAML_PATH, 'r') as config_yaml:
		yaml_parsed = yaml.load(config_yaml)
	
		#Write CICs
		hosts_file.write('[cics]\n')
		for i in range(1,4):
			hosts_file.write('cic-'+ str(i) + '\n')

		#Write Computes
		hosts_file.write('\n[computes]\n')
		for i in yaml_parsed['ericsson']['shelf'][0]['blade']:
			hosts_file.write('compute-0-' + str(i['id']) + '\n')
	
		#Write tenants
		hosts_file.write('\n[tenants]\n')
		for i in yaml_parsed['ericsson']['shelf'][0]['blade']:
			if i['id'] != 1 and i['id'] != 2 and i['id'] != 3 and not str(i['id']) in vsa_list:
				hosts_file.write('compute-0-' + str(i['id']) + '\n')

		#Write VSA
		if vsa:		
			hosts_file.write('\n[vsa]\n')
			for i in vsa_list:
				hosts_file.write('compute-0-' + i + '\n')
				
		#write childen and vars
		hosts_file.write('\n[common:children]\n'
							+ 'cics\n'
							+ 'computes\n'
							+ 'tenants\n')
		if vsa:
			hosts_file.write('vsa\n')
		hosts_file.write('\n[common:vars]\n'
							+ 'ansible_connection=ssh\n'
							+ 'ansible_user=root\n')
except:
	print("[ERROR] Please execute this script as root")
	if 'hosts_file' in locals():
		hosts_file.close()
	sys.exit(1)
