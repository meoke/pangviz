from collections import deque
from typing import Dict, List, Tuple, Set, Any

import math
from ..layout.colors import colors
import plotly.graph_objs as go
import pandas as pd

from pangtreebuild.consensus.ConsensusTree import ConsensusNodeID
from pangtreebuild.output.PangenomeJSON import PangenomeJSON, ConsensusNode
import networkx as nx
from networkx.readwrite import json_graph


def get_consensustree_dict(jsonpangenome: PangenomeJSON) -> Dict:
    tree = get_consensustree(jsonpangenome)
    tree_dict = tree_to_dict(tree)
    return tree_dict


def get_consensustree(jsonpangenome: PangenomeJSON) -> nx.DiGraph:
    tree_graph = nx.DiGraph()
    for consensus in sorted(jsonpangenome.consensuses, key=lambda c: c.consensus_node_id):
        node_is_leaf = True if not consensus.children else False
        tree_graph.add_node(consensus.consensus_node_id,
                            name=consensus.name,
                            comp=consensus.comp_to_all_sequences,
                            sequences_ids=consensus.sequences_int_ids,
                            show_in_table=True,
                            hidden=False,
                            children_consensuses=consensus.children,
                            # mincomp=consensus.mincomp ** (1/jsonpangenome.program_parameters.p),
                            mincomp=consensus.mincomp,
                            is_leaf=node_is_leaf)
        if consensus.parent is not None:
            tree_graph.add_edge(consensus.parent, consensus.consensus_node_id, weight=len(consensus.sequences_int_ids))

    return tree_graph


def tree_to_dict(tree_graph: nx.DiGraph) -> Dict:
    return json_graph.tree_data(tree_graph, root=0)


def dict_to_tree(tree_data: Dict) -> nx.DiGraph:
    return json_graph.tree_graph(tree_data)


def get_node_id_to_y_pos(tree: nx.DiGraph) -> Dict[ConsensusNodeID, int]:
    node_id_to_y = {}
    leafs_ids = []
    for node_id in tree.nodes:
        if not tree.nodes[node_id]['children_consensuses']:
            leafs_ids.append(node_id)
    leafs_count = len(leafs_ids)
    min_y = 0
    max_y = 100
    leaf_distance = (max_y - min_y) / (leafs_count + 1)
    for i, leaf_id in enumerate(leafs_ids):
        node_id_to_y[leaf_id] = leaf_distance * (i + 1)
    nodes_to_process = deque(leafs_ids)
    while nodes_to_process:
        processed_child_id = nodes_to_process.pop()
        parents = [node_id
                   for node_id in tree.nodes
                   if processed_child_id in tree.nodes[node_id]['children_consensuses']]
        if parents:
            parent_id = parents[0]
        else:
            break
        siblings = tree.nodes[parent_id]['children_consensuses']
        all_siblings_set = all([s in node_id_to_y.keys() for s in siblings])
        if all_siblings_set:
            for s in siblings:
                if s in nodes_to_process:
                    nodes_to_process.remove(s)
        else:
            for s in siblings:
                if s not in node_id_to_y.keys() and s not in nodes_to_process:
                    nodes_to_process.appendleft(s)
            nodes_to_process.appendleft(processed_child_id)
            continue
        siblings_positions = [y for node_id, y in node_id_to_y.items() if node_id in siblings]
        left_child_pos = min(siblings_positions)
        right_child_pos = max(siblings_positions)
        node_id_to_y[parent_id] = (right_child_pos + left_child_pos) / 2
        nodes_to_process.append(parent_id)
    return node_id_to_y


def get_consensustree_graph(tree: nx.DiGraph, slider_value: float, leaf_info_value: str, full_consensustable: pd.DataFrame) -> go.Figure:
    node_id_to_y = get_node_id_to_y_pos(tree)
    minCompsLabels = [format(tree.nodes[node_id]["mincomp"], '.4f') for node_id in range(len(node_id_to_y))]
    labels_on_hover = [f'{minCompLabel}' for minCompLabel in minCompsLabels]
    labels = [f"{node_id}" for node_id in range(len(node_id_to_y))]
    positions = [(tree.nodes[node_id]["mincomp"], node_id_to_y[node_id]) for node_id in range(len(node_id_to_y))]

    tree_nodes_graph = get_tree_nodes_graph(positions, labels_on_hover)
    tree_nodes_annotations = get_tree_nodes_annotations(positions, labels)
    tree_lines_graph = get_tree_lines_graph(positions, tree)

    line_graph = get_line_graph(slider_value)

    leaves_text_graph = get_leaves_text_graph(positions, tree, leaf_info_value, full_consensustable)

    layout = dict(title='Consensuses Tree',
                  annotations=tree_nodes_annotations,
                  font=dict(size=12),
                  showlegend=False,
                  xaxis=go.layout.XAxis(dict(range=[0, 1.2], showline=False, zeroline=False, showgrid=False,
                                             showticklabels=False,)),
                  yaxis=go.layout.YAxis(dict(range=[0, 100], showline=False, zeroline=False, showgrid=False,
                                             showticklabels=False,)),
                  margin=dict(l=20, r=10, b=0, t=0),
                  hovermode='closest',
                  plot_bgcolor=colors['transparent'],
                  autosize=True,
                  )

    return go.Figure(
            data=[tree_lines_graph, tree_nodes_graph, line_graph, leaves_text_graph],
            layout=layout,

            )


def get_line_graph(slider_value: float) -> go.Scatter:
    return go.Scatter(x=[slider_value, slider_value],
                      y=[0, 100],
                      mode='lines',
                      line=dict(color=colors['accent']))


def get_tree_nodes_graph(positions: List[Tuple[float, float]], labels_on_hover: List[str]) -> go.Scatter:
    return go.Scatter(x=[x for [x, _] in positions],
                      y=[y for [_, y] in positions],
                      mode='markers',
                      name='',
                      textposition='top left',
                      marker=dict(symbol='circle',
                                  size=20,
                                  color='rgba(255, 255, 255, 1)',
                                  line=dict(color='rgba(49, 55, 21, 1)',
                                            width=1),
                                  ),
                      text=labels_on_hover,
                      hoverinfo='text',
                      opacity=1)


def get_tree_lines_graph(positions: List[Tuple[float, float]], tree: nx.DiGraph) -> go.Scatter:
    lines_x = []
    lines_y = []
    for u, v in tree.edges:
        lines_x += [positions[u][0], positions[v][0], None]
        lines_y += [positions[u][1], positions[v][1], None]
    tree_lines_graph = go.Scatter(x=lines_x,
                                  y=lines_y,
                                  mode='lines',
                                  line=dict(color='rgba(49, 55, 21, 1)',width=2),
                                  hoverinfo='none'
                                  )
    return tree_lines_graph


def get_tree_nodes_annotations(positions: List[Tuple[float, float]], labels: List[str]) -> List[Dict]:
    return [{'x': position[0],
             'y': position[1],
             'text': f"{labels[i]}",
             'showarrow': False}
             for i, position in enumerate(positions)]


def get_leaf_label(sequences_ids: List[int], leaf_info_value: str, full_consensustable: pd.DataFrame) -> str:
    return ", ".join([str(l) for l in set(full_consensustable[leaf_info_value].loc[full_consensustable["ID"].isin(sequences_ids)])])


def get_leaves_text_graph(positions: List[Tuple[float, float]], tree: nx.DiGraph, leaf_info_value: str,
                          full_consensustable: pd.DataFrame) -> go.Scatter:
    x = []
    y = []
    text = []
    for i in range(len(tree.nodes)):
        if not tree.nodes[i]['is_leaf']:
            continue
        x.append(positions[i][0] + 0.02)
        y.append(positions[i][1])
        text.append(get_leaf_label(sequences_ids=tree.nodes[i]['sequences_ids'],
                                   leaf_info_value=leaf_info_value,
                                   full_consensustable=full_consensustable))

    return go.Scatter(
        x=x,
        y=y,
        text=text,
        mode='text+markers',
        textposition='middle right',
        hoverinfo='none',
        marker=dict(symbol='line-ew-open',
                    size=3,
                    color='black',
                    line=dict(color='rgb(50,50,50)', width=0),
                    )
    )


def get_leaf_info_dropdown_options(metadata: List[str]) -> List[Dict[str, str]]:
    return [ {'label': m, 'value': m} for m in metadata]


def get_offspring_ids(tree: nx.DiGraph, current_node_id: ConsensusNodeID) -> List[ConsensusNodeID]:
    nodes_to_visit = deque(tree.nodes[current_node_id]['children_consensuses'])
    offspring_ids = []
    while nodes_to_visit:
        current_node_id = nodes_to_visit.pop()
        offspring_ids.append(current_node_id)
        nodes_to_visit.extend(tree.nodes[current_node_id]['children_consensuses'])
    return offspring_ids