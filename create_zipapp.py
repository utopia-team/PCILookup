import pathlib
import zipapp


FILES = (
    ('main.py',),
    ('pci.ids',)
)


def main():
    zipapp.create_archive(
        ".", 
        "PCILookup.pyz", 
        main="main:main", 
        filter=lambda x: x.parts in FILES
    )


if __name__ == "__main__":
    main()
