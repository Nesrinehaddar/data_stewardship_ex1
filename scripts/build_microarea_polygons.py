#!/usr/bin/env python

"""
Create geometries for Fater microareas (~300 for the whole Italy) by merging
ISTAT nanoareas shapes.
"""

import argparse
import glob
import os

from IPython import embed
import pandas as pd
import geopandas as gpd

def main():
    
    # Load nanoarea shapes
    italy_raw_shape = pd.read_pickle("data/clean/italy_nanoarea_shape.p")

    # Load nanoarea definitions
    nanoarea_df = pd.read_excel("data/raw/cluster_def_05_08_2019.xlsx", sheet_name='cluster_def_05_08_2019')
    nanoarea_df["SEZ2011"] = nanoarea_df.astype(str)

    # Join the nanoarea into the microcode data
    italy_raw_shape = pd.merge(italy_raw_shape, nanoarea_df, on='SEZ2011', how = "left")

    # Fix some invalid geometries (which have is_valid = 0)
    italy_raw_shape["geometry"] = italy_raw_shape["geometry"].buffer(0)

    # http://geopandas.org/aggregation_with_dissolve.html
    # as_index=False to keep the nanoarea id as a column
    nanoarea_w_geoms_df = italy_raw_shape.dissolve(by='CLUSTER', as_index=False)

    # Save full dataset (dissolve takes a while..)
    nanoarea_w_geoms_df.to_file('data/clean/microareas_full.geojson', driver='GeoJSON')
    nanoarea_w_geoms_df.to_pickle('data/clean/microareas_full.p')

    # Simplify geometries to speed up loading in Kepler
    nanoarea_simple_df = nanoarea_w_geoms_df.copy()
    nanoarea_simple_df["geometry"] = nanoarea_w_geoms_df.simplify(tolerance=1e-3, preserve_topology=True)

    nanoarea_simple_df.to_file('data/clean/microareas.geojson', driver='GeoJSON')


if __name__ == "__main__":
    main()

