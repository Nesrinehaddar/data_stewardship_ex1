#!/usr/bin/env python

"""
Census shapes for 2011 are only available by region
(from https://www.istat.it/it/archivio/104317 "basi territoriali")
This script merges them into a single GeoDataFrame.
"""

import glob

import geopandas as gpd
import pandas as pd

def main():
    shape_files_paths = list(sorted(glob.glob('data/raw/SEZ2011/*/*.shp')))
    assert shape_files_paths
    
    print("Reading shape files")
    shapes = []
    for fp in shape_files_paths:
        shape = gpd.read_file(fp)
        shapes.append(shape)
    
    print("Converting CRS")
    italy_raw_shape = pd.concat(shapes).sort_values('SEZ2011')
    italy_raw_shape.to_crs({'init': 'epsg:4326'}, inplace =True )
    
    # Cast columns as int, then string
    for col in ['SEZ2011', 'LOC2011', 'COD_ISTAT', 'COD_REG']:
        italy_raw_shape[col] = italy_raw_shape[col].astype(str)
        
    # Simplify geometries to speed up loading in Kepler
    simple_df = italy_raw_shape.copy()
    simple_df["geometry"] = italy_raw_shape.simplify(tolerance=1e-3, preserve_topology=True)

    print("Exporting data")
    simple_df.to_file('data/clean/italy_nanoarea_shape.geojson', driver='GeoJSON')
    italy_raw_shape.to_pickle('data/clean/italy_nanoarea_shape.p')

if __name__ == "__main__":
    main()

