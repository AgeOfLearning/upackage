import sys
import logging
from upackage.upackage import UPackage

logging.basicConfig(level=logging.INFO)

UPackage.preprocess_assets(sys.argv[1])
UPackage.generate_package(sys.argv[1], sys.argv[2])