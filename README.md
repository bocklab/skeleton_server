# Sekleton Server

This is a small web service to serve [CATMAID](https://www.catmaid.org/) skeletons
as a [neuroglancer](https://github.com/google/neuroglancer) datasource.

## Usage

Run the server, e.g. `flask run` after installing dependencies.

### Neuroglancer layer definition

For FAFBv14, no translation:
```
{
    "type": "segmentation",
    "name": "VFB Skeletons",
    "source": "precomputed://http://127.0.0.1:5000/catmaid/vfb_fafb/skeleton/",
    "segments": [
        "815776"
    ],
    "selectedAlpha": 0,
        "skeletonRendering": {
        "mode2d": "lines",
        "lineWidth2d": 25,
        "mode3d": "lines_and_points",
        "lineWidth3d": 10
    }
}
```

For FAFBv14, with translation to FlyWire:
```
{
    "type": "segmentation",
    "name": "VFB Skeletons",
    "source": "precomputed://http://127.0.0.1:5000/catmaid/vfb_fafb/transform/v14_to_flywire/skeleton/",
    "segments": [
        "815776"
    ],
    "selectedAlpha": 0,
        "skeletonRendering": {
        "mode2d": "lines",
        "lineWidth2d": 25,
        "mode3d": "lines_and_points",
        "lineWidth3d": 10
    }
}
```

## Notes
* Dimensions are currently using the FAFB extents 

## References
* [neuroglancer skeleton spec](https://github.com/google/neuroglancer/blob/master/src/neuroglancer/datasource/precomputed/skeletons.md)
