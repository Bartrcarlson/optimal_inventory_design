#!/Users/bartlycarlson/Library/CloudStorage/Dropbox/Mac/Documents/svr/prelim_inventory_design/src/opt_plot_alloc/bin/python3

import sys

from osgeo.gdal import UseExceptions, deprecation_warn

# import osgeo_utils.gdalcompare as a convenience to use as a script
from osgeo_utils.gdalcompare import *  # noqa
from osgeo_utils.gdalcompare import main

UseExceptions()

deprecation_warn("gdalcompare")
sys.exit(main(sys.argv))
