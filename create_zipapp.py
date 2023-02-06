import zipapp


def main():
    zipapp.create_archive("src", "PCILookup.pyz", main="main:main")


if __name__ == "__main__":
    main()
