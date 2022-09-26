#!/usr/bin/env python3

# ####################################################################################
# Copyright IBM Corp. 2016 All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# ####################################################################################

# ####################################################################################
#
# Purpose : The script is executed from QRadar
#           to run a Job defined in CDM using 
#           CDM API calls
#
# Author  : Shashank Shingornikar
# 
# Date 
# Written : Mon May 30 22:10:53 IST 2022
# 
# Version : 0.1 : Initial attempt
# 			0.2 : Update Pepe Lam 
#					- New function to get SLA policy
#					- Added _data to runAPI
#					- global definition of _data = {}
#			0.3 : Not using getSLAPolicy function
#				  Program adapted to run Restore Job only
# 
# usage: runjob.py [-h] -s CDM_SERVER [-p CDM_PORT] -u CDM_USER -P CDM_PASS -j RESTORE_JOB_NAME
#
# ####################################################################################

# ####################################################################################
#		
#						**** DISCLAIMER ****
#
# This script is written to demonstrate the cyber resiliency workflow in a controlled
# environment. 
#
# There is no official support on the script from IBM.
# 
# Under no circumstances the script may be deployed in Production environment.
#
# Users are encouraged to develop their own programatical response based on this sample.
#
# ####################################################################################

import sys
import json
import argparse
import requests
from requests.packages.urllib3.exceptions import *

def main():

	_session_id = getSessionId()
	_hdr['x-endeavour-sessionid'] = _session_id

	_job_id = getJobId()
	#sla_policy_id = getSLAPolicy(_job_id)

	if _job_id is not None:
		_endpoint = URL + '/api/endeavour/job/' + str(_job_id) + \
			'?action=start&actionname=start'
	#	_data['actionname'] = str(sla_policy_id)
		runAPI( _endpoint, 'post', _hdr, _data )


def getJobId():
	"""
		The function is used to get the backup job id 
		and return the same

		Parameters:
			- IN - None
			- Out - jobid
	"""
	_endpoint = URL + '/api/endeavour/job'
	_response = runAPI( _endpoint, 'get', _hdr, _data )

	total = _response['total']

	_i = jobid = 0

	while( _i < total ):

		if cdm_job_name == _response['jobs'][_i]['name']:
			jobid = _response['jobs'][_i]['id']
			return jobid

		_i+=1

def getSLAPolicy(jobid):
	"""
		The function is used to get the SLA policy for the job
		This is required when running a backup job.

		Parameters:
			IN - jobid
			OUT - SLA Policy ID	
	"""

	_slaEndpoint = URL + '/api/endeavour/policy/' + str(jobid)
	_slaResponse = runAPI( _slaEndpoint, 'get', _hdr, _data)

	for x in _slaResponse['spec']['storageworkflow']:
		if cdm_sla_policy == x['name']:
			return x['id']

def getSessionId():
	"""
		The function is used to initiate a session
		and return the sessionid

		Params:
			IN - None
			OUT - sessionid
	"""

	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
	_endpoint = URL + '/api/endeavour/session'

	try:
		_requests = requests.post(
			_endpoint,
			auth = (cdm_user, cdm_pass),
			verify = spp_verify,
			timeout = 30
		)
		try:
			_response = json.loads( _requests.text )
		except json.decoder.JSONDecodeError:
			print('Unknown response from server')
			sys.exit(1)
	except requests.exceptions.ConnectionError:
		print('ERROR: Connection refused. Check CDM Server IP & PORT')
		sys.exit(1)
	except requests.exceptions.ConnectTimeout:
		print('ERROR: Connection timeout.')
		sys.exit(1)
	
	try:
		if 'sessionid' in _response:
			return _response['sessionid']

		if _response['id'] == 'XSBAuthenticationException':
			print('Authentication ERROR: {0}'.format(_response['description']))
			sys.exit(1)
	except KeyError:
		pass

def runAPI( URL, METHOD, HDR, DATA ):
	"""
		Generic function to make api call based on method
		and return any value if requested

		Params:
			IN 
				- URL - Url with endpoint
				- METHOD - POST / GET
				- HDR - JSON based header, optionally with sessionid
				- RETURN_VAL - Return specific value or entire json object
			OUT
				- API call ouput
	"""

	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

	_response = ''

	try:
		if METHOD == 'post':
			_requests = requests.post(
				URL,
				headers = HDR,
				verify = spp_verify,
				timeout = 30,
				data=json.dumps(DATA)
			)
		else:
			_requests = requests.get(
				URL,
				headers = HDR,
				verify = spp_verify,
				timeout = 30
			)
		try:
			_response = json.loads( _requests.text )
		except json.decoder.JSONDecodeError:
			print('Unknown response from server')
			sys.exit(1)
	except requests.exceptions.ConnectionError:
		print("ERROR: Connection refused. Check CDM Server IP & PORT")
	
	return _response


if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument(
		'-s',
		'--cdm_server',
		type=str,
		required=True,
		help='<Mandatory> IP/FQDN of CDM server'
	)

	parser.add_argument(
		'-p',
		'--cdm_port',
		type=int,
		required=False,
		default=8443,
		help='<Optional> Port of CDM server'
	)

	parser.add_argument(
		'-u',
		'--cdm_user',
		type=str,
		required=True,
		help='<Mandatory> CDM user'
	)

	parser.add_argument(
		'-P',
		'--cdm_pass',
		type=str,
		required=True,
		help='<Mandatory> CDM user Password'
	)

	parser.add_argument(
		'-j',
		'--restore_job_name',
		type=str,
		required=True,
		help='<Mandatory> CDM Restore Job name'
	)

	#parser.add_argument(
	#	'-w',
	#	'--bkup_sla_policy',
	#	type=str,
	#	required=False,
	#	help='<Mandatory> CDM Backup SLA Policy name'
	#)

	args = parser.parse_args()

	cdm_ip = args.cdm_server.strip()
	cdm_port = args.cdm_port
	cdm_user = args.cdm_user.strip()
	cdm_pass = args.cdm_pass.strip()
	cdm_job_name = args.restore_job_name.strip()
	#cdm_sla_policy = args.sla_policy

	spp_verify = False

	URL = 'https://' + cdm_ip + ':' + str(cdm_port)

	_hdr = {
		'Accept': 'application/json',
		'Content-type': 'application/json'
	}

	_data = {}

	main()
