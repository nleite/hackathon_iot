#!/usr/bin/python
import shapefile
import click

class GeoPlace(object):
    def __init__(self, name, geojson, **kwargs):
        self.name = name
        self.geojson = geojson
        #self.bbox = bbox
        #////.....
    def to_mongo(self):
        d = {
                'name': self.name,
                'position': self.geojson
                }

        return d

def build_polygon(points):
    d = { 'type': 'Polygon', 'coordinates': [points]}
    return d

def build_multipolygon( polygon_points):
    d = { 'type': 'MultiPolygon', 'coordinates': [polygon_points]}
    return d

def parse_shapepoints(parts, points):
    polygons = []
    cur = 0
    prev = -1
    if len(parts) == 1:
       return build_polygon(points)

    for x in parts[1:]:
       polygons.append([points[cur:x]])
    return build_multipolygon(polygons)

def parse_record(fields, record):
    d = {}
    num = len(record.record)
    #import ipdb;ipdb.set_trace()
    for f in range(num):
        d[fields[f+1][0]] = record.record[f]
    return d


def parser(fields, shapeRecord):
    record = shapeRecord.record
    shape = shapeRecord.shape
    geo = parse_shapepoints(shape.parts, shape.points)
    d = parse_record(fields, record)
    d['geo'] = geo
    return d


@click.command()
@click.option('--folder', default='.', help='folder name where to load the shx, shp, dbf files')
def main(folder):

    reader = shapefile.Reader(folder)

    for i in range(reader.numRecords):
        print parse_record(reader.fields, reader.shapeRecord(i))



if __name__ == '__main__':
    main()

