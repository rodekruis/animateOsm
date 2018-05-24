#import urllib2
import xml.etree.ElementTree as ET


'''
[out:xml][timeout:25]
[diff:"2017-05-13T08:41:45Z","2018-05-20T08:41:45Z"];
(
	node["building"](18.024057499596754, -63.08702778317096, 18.029378372819536, -63.07829188032329);
	way["building"](18.024057499596754, -63.08702778317096, 18.029378372819536, -63.07829188032329);
	relation["building"](18.024057499596754, -63.08702778317096, 18.029378372819536, -63.07829188032329);
);
(._;>;);
out meta;
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
                        print(child.tag)
                        if child.tag == 'node':
                            node = self.parse_node(child)
                            if node is not None:
                                self.nodes[node['id']] = node
                
                if action_type == 'create':
                    create_cnt += 1
                    for child in action:
                        print(child.tag)
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
            print(node.attrib['id'])
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
            print(way.attrib['id'])
            result['osm_id'] = way.attrib['id']
            result['timestamp'] = way.attrib['timestamp']
            result['user'] = way.attrib['user']
        except:
            print('Invalid way')
            return None

        points = []
        nds = way.findall('nd')
        for nd in nds:
            #print(nd)
            ndid = nd.attrib['ref'] 
            #print(nd.attrib['ref'])
            #print(self.nodes[ndid])
            points.append('%s %s' % (self.nodes[ndid]['lon'], self.nodes[ndid]['lat']))
        if len(points) > 3:
            # TODO: check if type is polygon or linestring (or point)
            result['wkt'] = 'POLYGON((%s))' % (','.join(points))
            #print(result['wkt'])
            print(result)
        return result










''' old code




overpass_url = 'https://overpass-api.de/api/interpreter?data=[adiff:%222017-08-19T06:00:00Z%22,%222017-08-19T07:00:00Z%22];(node(bbox)(changed);way(bbox)(changed););out%20meta%20geom(bbox);&bbox=86.612,26.47,87.55,26.846'


def get_osm_data(start_time, end_time, xmin, ymin, xmax, ymax):
    overpass_url = 'https://overpass-api.de/api/interpreter?data=[adiff:%22'
    overpass_url += start_time
    overpass_url += '%22,%22'
    overpass_url += end_time
    overpass_url += '%22];(node(bbox)(changed);way(bbox)(changed););out%20meta%20geom(bbox);&bbox='
    overpass_url += str(xmin) + ',' + str(ymin) + ',' + str(xmax) + ',' + str(ymax)
    print(overpass_url)
    response = urllib2.urlopen(overpass_url)
    print response.info()
    html = response.read()
    response.close()  # best practice to close the file
    return html


def parse_xml_diff(xml_txt, filename):
    errors = 0
    inserts = 0
    root = ET.fromstring(xml_txt)
    print root
    outfile = open(filename,'w')
    for way in root.iter('way'):
        insert = way_to_insert(way, 'ways')
        #print(insert)
        try:
            outfile.write(insert + '\n')
            inserts += 1
        except:
            print(insert)
            errors += 1
    outfile.close()
    print r'inserts: ' + str(inserts) + r'  errors: ' + str(errors) + r'(' + str((float(errors) / float(inserts)) * 100) + r'%)'

def way_to_insert(way, table):
    result = r'INSERT INTO ' + table + r' (id, timestamp, geom) VALUES ('
    result += way.attrib['id']
    result += r", '" + way.attrib['timestamp'] + r"'"
    #result += r", '" + way.attrib['user'].replace("'",'#') + r"'"
    wkt = way_to_wkt(way)
    if wkt is not None:
        result += r", ST_GeomFromText('" + wkt + r"',4326)"
    else:
        result += r', NULL'
    result += r");"
    return result
    

def way_to_wkt(way):
    xy_list = []
    for nd in way.iter('nd'):
        try:
            xy_list.append(nd.attrib['lon'] + r' ' + nd.attrib['lat'])
        except:
            print r'error: ' + str(nd.attrib)
    if len(xy_list) < 2:
        return None
    return r'LINESTRING(' + r','.join(xy_list) + r')'


'''