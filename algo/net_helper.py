import geopandas as gpd
import pandas as pd

cols_static = ["edge_id", "osm_id", "length", "geometry"]
cols_dir_basic = ["access_bicycle", "access_pedestrian"]

def netascore_to_routable_net(netascore_gdf: gpd.GeoDataFrame, mode="bike", access="bicycle", routing_factor = 4, access_penalty_factor = 4):
    # if input does not have 'edge_id' column, generate it from index
    if not 'edge_id' in netascore_gdf.columns:
        netascore_gdf['edge_id'] = netascore_gdf.index
        print("net helper: created 'edge_id' column from gdf index.")
    cols_dir = cols_dir_basic + [f"index_{mode}"]
    # filter input df
    cols = cols_static + ["from_node", "to_node"] + [f"{x}_ft" for x in cols_dir] + [f"{x}_tf" for x in cols_dir]
    net_a = netascore_gdf.filter(cols, axis=1).copy()
    # append inverted state
    net_a["inv"] = False
    # generate mapping for renaming dir-specific columns
    mapping = {f'{k}_ft': f'{k}_tf' for k in cols_dir}
    mapping.update({f'{k}_tf': f'{k}_ft' for k in cols_dir})
    mapping.update({"from_node":"to_node", "to_node":"from_node"})
    net_b = net_a.rename(columns=mapping)
    net_b["inv"] = True
    # append inverted direction net
    net = None
    net = pd.concat([net_a, net_b], ignore_index=True)
    # remove inverted-dir columns
    net.drop([f'{k}_tf' for k in cols_dir], axis=1, inplace=True, errors="ignore")
    # append routing cost columns
    print(f"orig: {len(netascore_gdf)}, routable (di-): {len(net)}")
    net[f"cost_{mode}_ft"] = ((1 + (1-net[f"index_{mode}_ft"]) * routing_factor) * net['length'])
    # apply penalty for segments with non-legal access (e.g. pushing bike for short
    # pedestrian-only section) if no alternative available / high detour induced
    net.loc[~net[f"access_{access}_ft"], f"cost_{mode}_ft"] *= access_penalty_factor
    net.loc[(~net[f"access_{access}_ft"]) & (net[f"cost_{mode}_ft"].isna()), f"cost_{mode}_ft"] = 1000
    return net