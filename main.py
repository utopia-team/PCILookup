#!/usr/bin/python3
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.environ.get("_MEIPASS2",os.path.abspath("."))

    return os.path.join(base_path, relative_path)

def lookup(vendor, device):
    pci_ids = open(resource_path('pci.ids')).readlines()
    ids_lib = {}
    for line in pci_ids:
        # If line is tabbed or contains an hashtag skips
        if line[:3] == "\t\t" or line[0] == "#":
            continue

        # If line isn't tabbed and isn't a newline create a :
        if not line[:1] in ['\t', '\n']:
            temp_vendor = line.split()[0]
            ids_lib[temp_vendor] = { 'name' : line[6:-1] }

        if line.startswith('\t\t') or line.startswith('\n'):
            continue
        if line.startswith('\t'):
            ids_lib[temp_vendor][line.split()[0]] = {'name': ' '.join(line.split()[1:])}
    return ids_lib[vendor][device]

if len(sys.argv) < 2:
    print(f'Wrong usage detected. Usage: ./pcilookup PCIInfo.txt')
    sys.exit(1)

pciinfo_file = open(sys.argv[1], 'r').readlines()
loc = int(len(pciinfo_file)/2) + 1

parsed_pciinfo = {}

for x in range(1,loc):
    parsed_pciinfo[x] = {
        'vendor_id': '',
        'device_id': '',
        'device_path': '',
        'description': ''}


vendor_ids = [line.split()[3][2:-1].lower() for line in pciinfo_file if not line.startswith('   ')]
device_ids = [line.split()[6][2:-1].lower() for line in pciinfo_file if not line.startswith('   ')]
device_paths = [line.split()[1] for line in pciinfo_file if line.startswith('   ')]

for x in range(1, loc):
    parsed_pciinfo[x]['vendor_id'] = vendor_ids[x-1]    
    parsed_pciinfo[x]['device_id'] = device_ids[x-1]    
    parsed_pciinfo[x]['device_path'] = device_paths[x-1]    
    try:
        parsed_pciinfo[x]['description'] = lookup(vendor=vendor_ids[x-1], device=device_ids[x-1])['name']
    except:
        parsed_pciinfo[x]['description'] = 'No data available'    


for k,v in parsed_pciinfo.items():
    print(f"{k}: {v['description']}\n\tVendor ID: {v['vendor_id']}\n\tDevice ID: {v['device_id']}\n\tDevice Path: {v['device_path']}")