#!/usr/bin/env python3
# nsndswap/web.py
# copyright 2017 ViKomprenas, 2-clause BSD license (LICENSE.md)

import datetime
import nsndswap.util


def _xmlencode(string):
    chars = {
        # note that this one has to be first, or else the other &s are caught
        '&': '&amp;',
        '"': '&quot;',
        '\'': '&apos;',
        '<': '&lt;',
        '>': '&gt;',
    }
    for ch in chars.keys():
        string = string.replace(ch, chars[ch])
    return string


class NodeData:
    def __init__(self):
        self.in_deg = 0
        self.out_deg = 0
        self.weighted_in_deg = 0
        self.weighted_out_deg = 0
        self.color = (0, 0, 0) # between 0 and 256
        self.size = 1

    @property
    def deg(self):
        return self.in_deg + self.out_deg

    @property
    def weighted_deg(self):
        return (self.weighted_in_deg + self.weighted_out_deg) / 2


class Web:
    def __init__(self):
        self.nodes = []  # list of strings
        self.edges = []  # list of edges, as (from, to) tuples

    def _get_id_of(self, title):
        try:
            return self.nodes.index(title)
        except ValueError:
            print(f'Discovered a new song, "{title}"')
            self.nodes.append(title)
            r = len(self.nodes) - 1
            assert self.nodes[r] is title
            return r

    def append(self, nsnd):
        for next_song in nsnd:
            assert isinstance(next_song, nsndswap.util.Track)
            if next_song.title == "":
                print('Skipping a null song')
                continue
            print(f'Turning references into map for "{next_song.title}"')

            node_id = self._get_id_of(next_song.title)

            # document references
            for ref in next_song.references:
                if ref == "":
                    print('Skipping a null reference')
                    continue
                ref_node_id = self._get_id_of(ref)
                if ref_node_id == node_id:
                    print(f'Skipping a reference from "{next_song.title}" to itself')
                    continue
                edge = (node_id, ref_node_id)
                if edge in self.edges:
                    print(f'Skipping a duplicated reference from "{next_song.title}" to "{ref}"')
                    continue
                self.edges += [edge]
                print(f'Followed a reference from "{next_song.title}" to "{ref}"')

    def _build_node_data(self):
        nodes_data = [NodeData() for _ in self.nodes]

        print('Adding degrees to node_data')
        for i in range(len(self.nodes)):
            for ref in self.edges:
                if ref[0] == i:
                    nodes_data[i].out_deg += 1
                elif ref[1] == i:
                    nodes_data[i].in_deg += 1

        print('Computing largest degree (for weighted degrees)')
        largest_in = 1
        largest_out = 1
        for data in nodes_data:
            largest_in = max(largest_in, data.in_deg)
            largest_out = max(largest_out, data.out_deg)
        
        print('Computing weighted degrees, colors, and sizes')
        for data in nodes_data:
            data.weighted_in_deg = data.in_deg / largest_in
            data.weighted_out_deg = data.out_deg / largest_out
            data.color = [data.weighted_in_deg * 127, data.weighted_out_deg * 127, 32]
            data.color = tuple(map(lambda x: x + 65, map(round, data.color)))
            assert len(data.color) == 3
            data.size = data.weighted_in_deg * 29 + 1

        print('Done building node data')
        return nodes_data
            

    def dump_gexf(self, outf):
        node_data = self._build_node_data()
        print('Dumping web')
        outf.write(f"""<?xml version="1.0" encoding="UTF-8" ?>
<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2" xmlns:viz="http://www.gexf.net/1.1draft/viz">
    <meta lastmodifieddate="{str(datetime.date.today())}">
        <creator>nsndswap</creator>
        <description>This is a list of references (remixes, arrangements, samples, etc.) in Homestuck music.</description>
    </meta>
    <graph mode="static" defaultedgetype="directed">
        <nodes>\n""")
        for node_id in range(len(self.nodes)):
            outf.write(f"""
            <node id=\"{node_id}\" label=\"{_xmlencode(self.nodes[node_id])}\" >
                <viz:size value="{node_data[node_id].size}"></viz:size>
                <viz:position x="0" y="0"></viz:position>
                <viz:color r="{node_data[node_id].color[0]}" g="{node_data[node_id].color[1]}" b="{node_data[node_id].color[2]}"></viz:color>
            </node>""")
        outf.write("""
        </nodes>
        <edges>\n""")
        for edge_id in range(len(self.edges)):
            outf.write(f"""
            <edge id="{edge_id}" source="{self.edges[edge_id][0]}" target="{self.edges[edge_id][1]}">
                <viz:color r="192" g="192" b="192"></viz:color>
            </edge>""")
        outf.write("""
        </edges>
    </graph>
</gexf>\n""")
        print('Done dumping web')
