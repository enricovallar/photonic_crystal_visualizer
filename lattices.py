import math

SQRT3 = math.sqrt(3)

def generate_points_hex_6d(x):
    return [{'u': x, 'v': 0}, {'u': 0, 'v': x}, {'u': -x, 'v': x}, 
            {'u': -x, 'v': 0}, {'u': 0, 'v': -x}, {'u': x, 'v': -x}]

def generate_points_hex_6e(x):
    return [{'u': x, 'v': x}, {'u': -x, 'v': 2*x}, {'u': -2*x, 'v': x}, 
            {'u': -x, 'v': -x}, {'u': x, 'v': -2*x}, {'u': 2*x, 'v': -x}]

wyckoff_hex = {
    'none': { 'name': 'None', 'type': 'none', 'points': [] },
    '1a': { 'name': '1a (Origin)', 'type': 'fixed', 'points': [{'u': 0, 'v': 0}] },
    '2b': { 'name': '2b (Honeycomb)', 'type': 'fixed', 'points': [{'u': 1/3, 'v': 1/3}, {'u': 2/3, 'v': 2/3}] },
    '3c': { 'name': '3c (Kagome)', 'type': 'fixed', 'points': [{'u': 1/2, 'v': 0}, {'u': 0, 'v': 1/2}, {'u': 1/2, 'v': 1/2}] },
    '6d': { 'name': '6d (Primary Hexamer)', 'type': 'variable', 'points': generate_points_hex_6d, 'defaultX': 0.25, 'maxX': 0.5 },
    '6e': { 'name': '6e (Secondary Hexamer)', 'type': 'variable', 'points': generate_points_hex_6e, 'defaultX': 0.15, 'maxX': 0.333 }
}

def generate_points_sq_4d(x):
    return [{'u': x, 'v': x}, {'u': -x, 'v': x}, {'u': -x, 'v': -x}, {'u': x, 'v': -x}]

def generate_points_sq_4e(x):
    return [{'u': x, 'v': 0}, {'u': 0, 'v': x}, {'u': -x, 'v': 0}, {'u': 0, 'v': -x}]

wyckoff_square = {
    'none': { 'name': 'None', 'type': 'none', 'points': [] },
    '1a': { 'name': '1a (Origin)', 'type': 'fixed', 'points': [{'u': 0, 'v': 0}] },
    '1b': { 'name': '1b (Center)', 'type': 'fixed', 'points': [{'u': 1/2, 'v': 1/2}] },
    '2c': { 'name': '2c (Edges)', 'type': 'fixed', 'points': [{'u': 1/2, 'v': 0}, {'u': 0, 'v': 1/2}] },
    '4d': { 'name': '4d (Diagonals)', 'type': 'variable', 'points': generate_points_sq_4d, 'defaultX': 0.25, 'maxX': 0.5 },
    '4e': { 'name': '4e (Axes)', 'type': 'variable', 'points': generate_points_sq_4e, 'defaultX': 0.25, 'maxX': 0.5 }
}

def get_points_for_species(lattice_type, config, x_param, extent=2):
    if not config or config['type'] == 'none':
        return []
        
    base_points = config['points'](x_param) if config['type'] == 'variable' else config['points']
    all_points = []
    
    for i in range(-extent, extent + 1):
        for j in range(-extent, extent + 1):
            for p in base_points:
                u, v = p['u'] + i, p['v'] + j
                if lattice_type == 'hexagonal':
                    x = (SQRT3 / 2) * v
                    y = u + 0.5 * v
                else:
                    x = u
                    y = v
                    
                all_points.append({
                    'x': x, 'y': y, 'u': u, 'v': v, 
                    'is_base': (i == 0 and j == 0)
                })
                
    return all_points
