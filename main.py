#!/usr/bin/python3
import pathlib
import re
import sys


def lookup(
    pci_ids: list[str], 
    vendor: str, 
    device: str
) -> str:
    check = False

    for line in pci_ids:
        if line[:1].isdigit():
            if check:
                break
            check = line.split()[0] == vendor

        if line.startswith('\t') and check:
            if (desc := line.split(maxsplit=1))[0] == device:
                return desc[-1].replace('\n', '')

    return 'Unknown device'


def main():
    if len(sys.argv) < 2:
        print(f'Wrong usage detected. Usage: ./pcilookup PCIInfo.txt')
        sys.exit(1)

    path = pathlib.Path(sys.argv[1])
    path_pci_ids = pathlib.Path('.') / 'pci.ids'

    if not path.exists() or not path.is_file():
        print(f'{path.name} not exist or isn\'t a file')
        sys.exit(1)
    
    if not path_pci_ids.exists():
        print('pci.ids not exist')
        sys.exit(1)    

    with open(path, 'r') as f:
        pciinfo_file = f.read()

    with open(path_pci_ids, 'r') as f:
        pci_ids = f.readlines()

    pci_list = [
        re.sub(r'\s+', ' ', x.strip())
        for x in re.split(r'\d+\.', pciinfo_file.replace('\n', ''))
        if x
    ]
    parsed_pciinfo = {}

    for i, pci in enumerate(pci_list):
        vendor_id = re.search(r'Vendor ID: 0[xX]([0-9a-fA-F]+),', pci).group(1).lower()
        device_id = re.search(r'Device ID: 0[xX]([0-9a-fA-F]+),', pci).group(1).lower()
        device_path = re.search(r'DevicePath: ([a-zA-Z0-9\(\)\/,]+)', pci).group(1)

        parsed_pciinfo[i + 1] = {
            'vendor_id': vendor_id,
            'device_id': device_id,
            'device_path': device_path,
            'description': lookup(pci_ids, vendor_id, device_id)
        }

    for k, v in parsed_pciinfo.items():
        print(f"{k}: {v['description']}\n\tVendor ID: {v['vendor_id']}\n\tDevice ID: {v['device_id']}\n\tDevice Path: {v['device_path']}")


if __name__ == "__main__":
    main()
