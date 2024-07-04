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

# helper function to add centrality results to input network DataFrame
def add_centr_to_netascore(netascore_gdf: gpd.GeoDataFrame, centrality, centr_name: str, edge_key: str = "edge_id"):
    # convert from dict with compound key to pandas df
    tdf = pd.DataFrame(list(centrality.keys()))
    tdf.rename(columns={0:"from_node", 1:"to_node", 2:"edge_key"}, inplace=True)
    tdf["centrality"] = centrality.values()
    # map centrality value back to original (geo)pandas df (for both directions)
    if netascore_gdf.index.name == edge_key and edge_key in netascore_gdf.columns:
        netascore_gdf.index.name = "index"
    net_tmp = netascore_gdf.merge(tdf, left_on=["from_node", "to_node", edge_key], right_on=["from_node", "to_node", "edge_key"], how="left", suffixes=[None, "_b"])
    net_tmp.rename(columns={"centrality":"centrality_ft"}, inplace=True)
    net_ready = net_tmp.merge(tdf, left_on=["to_node", "from_node", "edge_key"], right_on=["from_node", "to_node", "edge_key"], how="left", suffixes=[None, "_c"])
    net_ready.rename(columns={"centrality":"centrality_tf"}, inplace=True)
    net_ready.set_index("edge_key", drop=False, inplace=True)
    if edge_key in netascore_gdf.columns:
        netascore_gdf.set_index(edge_key, drop=False, inplace=True)
        netascore_gdf.index.name = "index"
    if "index" in netascore_gdf.columns:
        netascore_gdf.drop(columns=["index"], inplace=True)
    netascore_gdf[f"centr_{centr_name}_ft"] = net_ready[~net_ready.index.isnull()].centrality_ft
    netascore_gdf[f"centr_{centr_name}_tf"] = net_ready[~net_ready.index.isnull()].centrality_tf
    centr_sum = net_ready.centrality_tf + net_ready.centrality_ft
    netascore_gdf[f"centr_{centr_name}_sum"] = centr_sum[~centr_sum.index.isnull()]