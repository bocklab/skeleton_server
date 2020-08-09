import io
import struct

import msgpack
import pymaid
import requests
import numpy as np

from flask import Flask, jsonify, make_response, Response
from flask_cors import CORS

from config import CATMAID_SOURCES, TRANSFORM_SOURCES

app = Flask(__name__)
CORS(app)


def get_pymaid_instance(catmaid_name):
    if catmaid_name in CATMAID_SOURCES:
        url = CATMAID_SOURCES[catmaid_name]['url']
        token = None
        pymaid.CatmaidInstance(url, token)
    else:
        raise Exception("Undefined CATMAID source: {}".format(catmaid_name))


def get_transform(transform_name):
    if transform_name in TRANSFORM_SOURCES:
        return TRANSFORM_SOURCES[transform_name]
    else:
        raise Exception("Undefined transform source: {}".format(catmaid_name))
    

def encode_skeleton(edges, vertex_positions):
    # Based on neuroglancer.skeleton.Skeleton.encode
    vertex_positions = np.array(vertex_positions, dtype='<f4')
    edges = np.array(edges, dtype='<u4')
    result = io.BytesIO()
    result.write(struct.pack('<II', vertex_positions.shape[0], edges.shape[0] // 2))
    result.write(vertex_positions.tobytes())
    result.write(edges.tobytes())
    return result.getvalue()

@app.route('/')
def hello_world():
    return '<h1>TODO: API docs</h1>'


@app.route('/catmaid/<string:catmaid>/skeleton/info', defaults={'transform' : None})
@app.route('/catmaid/<string:catmaid>/transform/<string:transform>/skeleton/info')
def datasource_skelinfo(catmaid, transform):

    info = {
        "@type" : "neuroglancer_skeletons",
        "transform" : [ 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 40, 0 ],
    }
    return jsonify(info)


@app.route('/catmaid/<string:catmaid>/skeleton/<int:skeleton>', defaults={'transform' : None})
@app.route('/catmaid/<string:catmaid>/transform/<string:transform>/skeleton/<int:skeleton>')
def get_skeleton(catmaid, transform, skeleton):
    try:
        # Get the pymaid object
        pymaid_instance = get_pymaid_instance(catmaid)

        # Get the neuron
        neuron = pymaid.get_neuron(9464046, remote_instance=pymaid_instance)

        if transform:
            # Map into FlyWire space
            tinfo = get_transform(transform)
            request_url = "%s/dataset/%s/s/%d/values_array" % (
                tinfo['url'],
                tinfo['transform'],
                tinfo['mip'])
            data = {'x' : (neuron.nodes['x']/4).tolist(), 'y' : (neuron.nodes['y']/4).tolist(), 'z' : (neuron.nodes['z']/40).tolist() }
            headers = {'Content-type': 'application/msgpack'}
            r = requests.post(request_url, data=msgpack.packb(data), headers=headers)
            if r.status_code == 200:
                resp = msgpack.unpackb(r.content)
            else:
                raise Exception("Error transforming skeleton: {}".format(r.content))

            neuron.nodes['x'] = np.asarray(resp['x']) * 4
            neuron.nodes['y'] = np.asarray(resp['y']) * 4
            neuron.nodes['z'] = np.asarray(resp['z']) * 40

        # Generate the neuroglancer skeleton
        vertex_positions = neuron.nodes[['x', 'y', 'z']].values / [4.0, 4.0, 40.0]
        edges = neuron.nodes.loc[~neuron.nodes.parent_id.isnull(), ['treenode_id', 'parent_id']].values
        treenode_index_map = dict(zip(neuron.nodes.treenode_id.values, neuron.nodes.treenode_id.index))
        edges = np.vectorize(lambda x: treenode_index_map[x])(edges)

        return Response(encode_skeleton(edges, vertex_positions), mimetype='application/octet-stream')

    except Exception as e:
        app.logger.error('Error: {}'.format(e))
        err = {'error': str(e)}
        return make_response(jsonify(err), 400)


