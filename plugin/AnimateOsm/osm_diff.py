#import urllib2
import xml.etree.ElementTree as ET
import time


'''
[out:xml][timeout:25]
[diff:"2017-05-13T08:41:45Z","2018-05-20T08:41:45Z"];
(
	node["building"](18.024057499596754, -63.08702778317096, 18.029378372819536, -63.07829188032329);
	way["building"](18.024057499596754, -63.08702778317096, 18.029378372819536, -63.07829188032329);
	relation["building"](18.024057499596754, -63.08702778317096, 18.029378372819536, -63.07829188032329);
);
(._;>;);
out meta geom;
'''

def download_osm_diff(query, url=r'https://overpass-turbo.eu/', filename='data/diff.osm'):
    pass
    

class OsmDiffParser():

    def __init__(self):
        self.nodes = {}
        self.ways = {}
        self.parse_to_polygon = ['building']

    def __str__(self):
        result = 'OsmDiffParser[nodes: %s, ways: %s]' % (len(self.nodes), len(self.ways))
        return result

    def clear(self):
        self.nodes = {}
        self.ways = {}

    def reset_time_range(self):
        ts = time.mktime(time.strptime(next(iter(self.ways))['timestamp'], '%Y-%m-%dT%H:%M:%SZ'))
        self.min_timestamp = ts
        self.max_timestamp = ts
        if len(self.ways) > 0:
            for key in self.ways:
                ts = time.mktime(time.strptime(self.ways[key]['timestamp'], '%Y-%m-%dT%H:%M:%SZ'))
                self.min_timestamp = min(self.min_timestamp, ts)
                self.max_timestamp = min(self.min_timestamp, ts)


    def read(self, filename):
        infile = open(filename, 'r')
        root = ET.fromstring(infile.read())
        infile.close()
        
        action_cnt = 0
        delete_cnt = 0
        modify_cnt = 0
        create_cnt = 0
        other_cnt = 0
        
        for action in root.iter('action'):
            action_cnt += 1
            action_type = action.attrib['type']
            if action_type in ['delete', 'modify', 'create']:
                
                if action_type == 'delete':
                    delete_cnt += 1
                
                if action_type == 'modify':
                    modify_cnt += 1
                    new = action.find('new')
                    for child in new:
                        if child.tag == 'node':
                            node = self.parse_node(child)
                            if node is not None:
                                self.nodes[node['id']] = node
                
                if action_type == 'create':
                    create_cnt += 1
                    for child in action:
                        if child.tag == 'node':
                            node = self.parse_node(child)
                            if node is not None:
                                self.nodes[node['id']] = node
                        if child.tag == 'way':
                            way = self.parse_way(child)
                            if way is not None:
                                self.ways[way['osm_id']] = way
            else:
                other_cnt += 1
                print('other action type!')


        
        print('action_cnt: %s' % action_cnt)
        print('delete_cnt: %s' % delete_cnt)
        print('modify_cnt: %s' % modify_cnt)
        print('create_cnt: %s' % create_cnt)
        print('other_cnt: %s' % other_cnt)

        print(len(self.nodes))
        print(len(self.ways))


        
    def parse_node(self, node):
        #<node id="1703119312" lat="18.0242059" lon="-63.0808480" version="2" timestamp="2015-04-15T06:31:13Z" changeset="30228200" uid="402624" user="bdiscoe"/>
        result = {}
        try:
            result['id'] = node.attrib['id']
            result['lat'] = node.attrib['lat']
            result['lon'] = node.attrib['lon']
        except:
            result = None
        return result


    def parse_way(self, way):
        #<node id="1703119312" lat="18.0242059" lon="-63.0808480" version="2" timestamp="2015-04-15T06:31:13Z" changeset="30228200" uid="402624" user="bdiscoe"/>
        result = {}

        try:
            result['osm_id'] = way.attrib['id']
            result['timestamp'] = way.attrib['timestamp']
            result['user'] = way.attrib['user']
        except:
            print('Invalid way')
            return None

        p = True
        points = []
        nds = way.findall('nd')
        for nd in nds:
            ndid = nd.attrib['ref']
            try:
                # node has geometry:
                points.append('%s %s' % (nd.attrib['lon'], nd.attrib['lat']))
            except: 
                try:
                    if p:
                        print('I should never get here')
                        p = False
                    # if node exists in file, get lat lon from it
                    points.append('%s %s' % (self.nodes[ndid]['lon'], self.nodes[ndid]['lat']))
                except:
                    # geometry is not available :(
                    pass
        if len(points) > 3:
            # TODO: check if type is polygon or linestring (or point)
            result['wkt'] = 'POLYGON((%s))' % (','.join(points))
        return result




