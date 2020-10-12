import sys
from upackage.upackage import UPackage


def main():
    if len(sys.argv) != 3:
        print("usage: upackage path/to/content output.unitypackage")
        exit(1)

    package_root = sys.argv[1]
    output_path = sys.argv[2]

    UPackage.preprocess_assets(package_root)
    UPackage.generate_package(package_root, output_path)


if __name__ == "__main__":
    main()
