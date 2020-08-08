#
# Basic configuration settings for skeleton datasoruces.
#

CATMAID_SOURCES = {
    'vfb_fafb' : {
        'type' : 'catmaid',
        'url' : 'https://fafb.catmaid.virtualflybrain.org'
    }
}

TRANSFORM_SOURCES = {
    'v14_to_flywire' : {
        'url' : 'https://spine.janelia.org/app/flyconv',
        'transform' : 'flywire_v1_inverse',
        'mip' : 4
    },
    'flywire_to_v14' : {
        'url' : 'https://spine.janelia.org/app/flyconv',
        'transform' : 'flywire_v1_inverse',
        'mip' : 4
    }
}
