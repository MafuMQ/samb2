from pyvis.network import Network
import pandas as pd
import os


got_net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", select_menu=True, filter_menu=True)

"""
add "notebook=false" to show method when using pyvis
see https://pyvis.readthedocs.io/en/latest/tutorial.html
set_options method cannot co-exist with show_buttons method for some reason idk
"""

inputCSVpath = os.path.abspath("search\stormofswords.csv")

# set the physics layout of the network
got_net.barnes_hut()
got_data = pd.read_csv(inputCSVpath)

sources = got_data['Source']
targets = got_data['Target']
weights = got_data['Weight']

edge_data = zip(sources, targets, weights)

for e in edge_data:
                src = e[0]
                dst = e[1]
                w = e[2]

                got_net.add_node(src, src, title=src)
                got_net.add_node(dst, dst, title=dst)
                got_net.add_edge(src, dst, value=w)

neighbor_map = got_net.get_adj_list()

# add neighbor data to node hover data
for node in got_net.nodes:
                node["title"] += " Neighbors:\n" + "\n".join(neighbor_map[node["id"]])
                node["value"] = len(neighbor_map[node["id"]])

got_net.show_buttons()

got_net.show("gameofthrones.html", notebook=False)