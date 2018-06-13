#import urllib2
import xml.etree.ElementTree as ET
import time
import urllib.parse

from .networkaccessmanager import NetworkAccessManager


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

def download_osm_diff(self, query, url=r'https://overpass-turbo.eu/', filename='data/diff.osm'):
    self.log(u'download_osm_diff')
    
    '''
    query = b'[out:xml][timeout:25][diff:"2018-06-06T13:00:00Z","2018-06-13T14:00:00Z"];(\
             node["building"](18.02701338, -63.08376483, 18.02811712, -63.08006941);\
             way["building"](18.02701338, -63.08376483, 18.02811712, -63.08006941);\
             relation["building"](18.02701338, -63.08376483, 18.02811712, -63.08006941);\
             );\
             (._;>;);\
             out meta geom;'
    '''
    
    overpass_url = 'https://overpass-api.de/api/interpreter'

    headers = {b'Content-type': b'application/osm3s+xml'}

    filename = '/home/raymond/git/animateOsm/plugin/AnimateOsm/data/diff2.osm'

    self.log(query)
    self.log(overpass_url)
    self.log(headers)

    nam = NetworkAccessManager()

    #query_fn = '/home/raymond/git/animateOsm/plugin/AnimateOsm/query.txt'
    #query_file = open(query_fn, 'r')

    (response, content) = nam.request(overpass_url, method='POST', headers=headers, body=query)
    #self.log(response)
    self.log(content)
    osm_file = open(filename, 'w')
    osm_file.write(content.decode("utf-8"))
    osm_file.close()
    #query_file.close()



class OsmDiffParser():

    def __init__(self):
        self.nodes = {}
        self.ways = {}
        self.parse_to_polygon = ['building']
        self.min_timestamp = 0
        self.max_timestamp = 0

    def __str__(self):
        result = 'OsmDiffParser[nodes: %s, ways: %s]' % (len(self.nodes), len(self.ways))
        return result

    def clear(self):
        self.nodes = {}
        self.ways = {}

    def reset_time_range(self):
        if len(self.ways) > 0:
            print(self.ways[next(iter(self.ways))]['timestamp'])
            print(self.__get_time(self.ways[next(iter(self.ways))]['timestamp']))
            ts = self.__get_time(self.ways[next(iter(self.ways))]['timestamp'])
            self.min_timestamp = ts
            self.max_timestamp = ts
            for key in self.ways:
                ts = self.__get_time(self.ways[key]['timestamp'])
                self.min_timestamp = min(self.min_timestamp, ts)
                self.max_timestamp = max(self.min_timestamp, ts)


    def __get_time(self, s):
        osm_time_format = '%Y-%m-%dT%H:%M:%SZ'
        return time.strptime(s, osm_time_format) 


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
        result = {}

        try:
            result['osm_id'] = way.attrib['id']
            result['timestamp'] = way.attrib['timestamp']
            result['user'] = way.attrib['user']
        except:
            # something is really wrong
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
                        p = False
                    # if node exists in osm file, get lat lon from it
                    points.append('%s %s' % (self.nodes[ndid]['lon'], self.nodes[ndid]['lat']))
                except:
                    # geometry is not available :(
                    pass
        if len(points) > 3:
            # TODO: check if type is polygon or linestring (or point)
            result['wkt'] = 'POLYGON((%s))' % (','.join(points))
        return result




