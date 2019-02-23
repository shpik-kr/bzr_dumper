# bzr dumper
Bazaar(bzr) is used for the purpose of DCVS like git.

It was developed in python.

The purpose of this tool is to dump .bzr on the web server. (e.g. http://targeturl/.bzr)

## Development Environment
- Ubuntu 16.04

- python 3.5.2

## Usage
python3 dumper.py -u "http://targeturl/" -o test

- -u, --url : set target url (e.g. http://shpik.kr/)

- -o, --output : set output dir (default : output)

