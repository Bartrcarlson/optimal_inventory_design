#!/Users/bartlycarlson/Library/CloudStorage/Dropbox/Mac/Documents/svr/prelim_inventory_design/src/opt_plot_alloc/bin/python3

import sys

from osgeo.gdal import UseExceptions, deprecation_warn

# import osgeo_utils.ogr_layer_algebra as a convenience to use as a script
from osgeo_utils.ogr_layer_algebra import *  # noqa
from osgeo_utils.ogr_layer_algebra import main

UseExceptions()

deprecation_warn("ogr_layer_algebra")
sys.exit(main(sys.argv))