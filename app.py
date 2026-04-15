import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import math
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
from lattices import wyckoff_hex, wyckoff_square, get_points_for_species, SQRT3

app = dash.Dash(__name__, external_stylesheets=['https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'])

def get_current_wyckoff(ltype):
    return wyckoff_hex if ltype == 'hexagonal' else wyckoff_square

app.layout = html.Div(className="min-h-screen bg-neutral-50 p-6 font-sans text-neutral-900", children=[
    html.Div(className="max-w-6xl mx-auto", children=[
        html.Header(className="mb-8", children=[
            html.H1("Photonic Crystal Visualizer", className="text-3xl font-bold tracking-tight text-neutral-800"),
            html.P("Interactive explorer for 2D hexagonal and square lattices.", className="text-neutral-600 mt-2")
        ]),
        
        html.Div(className="grid grid-cols-1 lg:grid-cols-12 gap-8", children=[
            # Controls Panel
            html.Div(className="lg:col-span-4 space-y-6", children=[
                
                # Lattice Toggle
                html.Div(className="bg-white rounded-2xl shadow-sm border border-neutral-200 p-4", children=[
                    html.H2("Lattice Type", className="text-lg font-semibold mb-3"),
                    dcc.RadioItems(
                        id='lattice-type',
                        options=[
                            {'label': ' Hexagonal (p6mm)', 'value': 'hexagonal'},
                            {'label': ' Square (p4mm)', 'value': 'square'}
                        ],
                        value='hexagonal',
                        labelStyle={'display': 'block', 'margin-bottom': '10px'},
                        inputClassName="mr-2"
                    )
                ]),

                # Area Stats
                html.Div(className="bg-white rounded-2xl shadow-sm border border-gray-200 p-4 text-gray-900", children=[
                    html.H2("Area Statistics", className="text-lg font-semibold mb-3 text-gray-800"),
                    html.Div(id='area-stats', className="text-sm space-y-2")
                ]),

                # Species A
                html.Div(className="bg-white rounded-2xl shadow-sm border-t-4 border-red-500 border border-neutral-200 p-6", children=[
                    html.Div(className="flex justify-between items-center mb-4", children=[
                        html.H2("Species A (Red)", className="text-lg font-semibold text-red-600"),
                        dcc.Checklist(id='enable-A', options=[{'label': ' Enable', 'value': 'on'}], value=['on'], inputClassName="mr-1")
                    ]),
                    html.Div(id='panel-A', children=[
                        dcc.Dropdown(id='dropdown-A', clearable=False, className="mb-4"),
                        html.Div(id='control-x-A', children=[
                            html.Label(id='label-x-A', className="block text-sm font-medium mb-1"),
                            dcc.Slider(id='slider-x-A', min=0, max=0.5, step=0.005, value=0, tooltip={"placement": "bottom", "always_visible": False})
                        ], style={'marginBottom': '15px'}),
                        html.Label("Atom Size:", className="block text-sm font-medium mb-1"),
                        dcc.Slider(id='slider-r-A', min=0.01, max=0.3, step=0.01, value=0.08, tooltip={"placement": "bottom", "always_visible": False})
                    ])
                ]),

                # Species B
                html.Div(className="bg-white rounded-2xl shadow-sm border-t-4 border-blue-500 border border-neutral-200 p-6", children=[
                    html.Div(className="flex justify-between items-center mb-4", children=[
                        html.H2("Species B (Blue)", className="text-lg font-semibold text-blue-600"),
                        dcc.Checklist(id='enable-B', options=[{'label': ' Enable', 'value': 'on'}], value=['on'], inputClassName="mr-1")
                    ]),
                    html.Div(id='panel-B', children=[
                        dcc.Dropdown(id='dropdown-B', clearable=False, className="mb-4"),
                        html.Div(id='control-x-B', children=[
                            html.Label(id='label-x-B', className="block text-sm font-medium mb-1"),
                            dcc.Slider(id='slider-x-B', min=0, max=0.5, step=0.005, value=0, tooltip={"placement": "bottom", "always_visible": False})
                        ], style={'marginBottom': '15px'}),
                        html.Label("Atom Size:", className="block text-sm font-medium mb-1"),
                        dcc.Slider(id='slider-r-B', min=0.01, max=0.3, step=0.01, value=0.08, tooltip={"placement": "bottom", "always_visible": False})
                    ])
                ]),

                # Species C
                html.Div(className="bg-white rounded-2xl shadow-sm border-t-4 border-green-500 border border-neutral-200 p-6", children=[
                    html.Div(className="flex justify-between items-center mb-4", children=[
                        html.H2("Species C (Green)", className="text-lg font-semibold text-green-600"),
                        dcc.Checklist(id='enable-C', options=[{'label': ' Enable', 'value': 'on'}], value=[], inputClassName="mr-1")
                    ]),
                    html.Div(id='panel-C', children=[
                        dcc.Dropdown(id='dropdown-C', clearable=False, className="mb-4"),
                        html.Div(id='control-x-C', children=[
                            html.Label(id='label-x-C', className="block text-sm font-medium mb-1"),
                            dcc.Slider(id='slider-x-C', min=0, max=0.5, step=0.005, value=0, tooltip={"placement": "bottom", "always_visible": False})
                        ], style={'marginBottom': '15px'}),
                        html.Label("Atom Size:", className="block text-sm font-medium mb-1"),
                        dcc.Slider(id='slider-r-C', min=0.01, max=0.3, step=0.01, value=0.08, tooltip={"placement": "bottom", "always_visible": False})
                    ])
                ]),

                # Display Options
                html.Div(className="bg-white rounded-2xl shadow-sm border border-neutral-200 p-6", children=[
                    html.H2("Display Options", className="text-lg font-semibold mb-4"),
                    dcc.Checklist(
                        id='display-options',
                        options=[
                            {'label': ' Show Extended Lattice', 'value': 'extended'},
                            {'label': ' Highlight Wigner-Seitz Cell', 'value': 'ws'},
                            {'label': ' Show Primary Unit Cell', 'value': 'primary'},
                            {'label': ' Show Symmetry Axes', 'value': 'symmetry'}
                        ],
                        value=['extended', 'ws', 'primary'],
                        labelStyle={'display': 'block', 'margin-bottom': '10px'},
                        inputClassName="mr-2"
                    )
                ])
            ]),

            # Plot Panel
            html.Div(className="lg:col-span-8 bg-white rounded-2xl shadow-sm border border-neutral-200 p-1 flex items-center justify-center cursor-crosshair", children=[
                dcc.Graph(
                    id='crystal-plot', 
                    config={'displayModeBar': False},
                    style={'height': '1000px', 'width': '100%'}
                )
            ])
        ])
    ])
])

@app.callback(
    [Output('dropdown-A', 'options'), Output('dropdown-A', 'value'),
     Output('dropdown-B', 'options'), Output('dropdown-B', 'value'),
     Output('dropdown-C', 'options'), Output('dropdown-C', 'value')],
    Input('lattice-type', 'value')
)
def update_dropdowns(ltype):
    wyckoff = get_current_wyckoff(ltype)
    opts_A = [{'label': v['name'], 'value': k} for k, v in wyckoff.items() if k != 'none']
    opts_rest = [{'label': v['name'], 'value': k} for k, v in wyckoff.items()]
    
    val_A = '1a'
    val_B = '2b' if ltype == 'hexagonal' else '1b'
    val_C = '3c' if ltype == 'hexagonal' else '2c'
    return opts_A, val_A, opts_rest, val_B, opts_rest, val_C

# Helper for sliding updates
def _update_slider(sel, ltype, current_val):
    if not sel or sel == 'none': return dash.no_update, dash.no_update, "", {'display': 'none'}
    config = get_current_wyckoff(ltype)[sel]
    if config['type'] == 'variable':
        return config['maxX'], config.get('defaultX', current_val), f"Radius (x):", {'display': 'block', 'marginBottom': '15px'}
    return 0.5, 0, "", {'display': 'none'}

@app.callback([Output('slider-x-A', 'max'), Output('slider-x-A', 'value'), Output('label-x-A', 'children'), Output('control-x-A', 'style')], [Input('dropdown-A', 'value'), Input('lattice-type', 'value')], [State('slider-x-A', 'value')])
def update_slider_A(sel, ltype, current): return _update_slider(sel, ltype, current)

@app.callback([Output('slider-x-B', 'max'), Output('slider-x-B', 'value'), Output('label-x-B', 'children'), Output('control-x-B', 'style')], [Input('dropdown-B', 'value'), Input('lattice-type', 'value')], [State('slider-x-B', 'value')])
def update_slider_B(sel, ltype, current): return _update_slider(sel, ltype, current)

@app.callback([Output('slider-x-C', 'max'), Output('slider-x-C', 'value'), Output('label-x-C', 'children'), Output('control-x-C', 'style')], [Input('dropdown-C', 'value'), Input('lattice-type', 'value')], [State('slider-x-C', 'value')])
def update_slider_C(sel, ltype, current): return _update_slider(sel, ltype, current)

@app.callback(Output('panel-A', 'style'), Input('enable-A', 'value'))
def toggle_panel_A(val): return {'display': 'block'} if val and 'on' in val else {'opacity': '0.5', 'pointerEvents': 'none'}

@app.callback(Output('panel-B', 'style'), Input('enable-B', 'value'))
def toggle_panel_B(val): return {'display': 'block'} if val and 'on' in val else {'opacity': '0.5', 'pointerEvents': 'none'}

@app.callback(Output('panel-C', 'style'), Input('enable-C', 'value'))
def toggle_panel_C(val): return {'display': 'block'} if val and 'on' in val else {'opacity': '0.5', 'pointerEvents': 'none'}

@app.callback(
    [Output('crystal-plot', 'figure'), Output('area-stats', 'children')],
    [Input('lattice-type', 'value'),
     Input('enable-A', 'value'), Input('dropdown-A', 'value'), Input('slider-x-A', 'value'), Input('slider-r-A', 'value'),
     Input('enable-B', 'value'), Input('dropdown-B', 'value'), Input('slider-x-B', 'value'), Input('slider-r-B', 'value'),
     Input('enable-C', 'value'), Input('dropdown-C', 'value'), Input('slider-x-C', 'value'), Input('slider-r-C', 'value'),
     Input('display-options', 'value')]
)
def update_plot(ltype, en_A, sel_A, x_A, r_A, en_B, sel_B, x_B, r_B, en_C, sel_C, x_C, r_C, display_opts):
    display_opts = display_opts or []
    show_extended = 'extended' in display_opts
    show_ws = 'ws' in display_opts
    show_primary = 'primary' in display_opts
    show_sym = 'symmetry' in display_opts
    
    fig = go.Figure()
    wyckoff = get_current_wyckoff(ltype)
    
    is_hex = (ltype == 'hexagonal')
    shapes = []
    
    # Base Grid Lines
    if show_extended:
        for v in range(-3, 4):
            if is_hex:
                x_val = (SQRT3/2)*v
                shapes.append(dict(type="line", x0=x_val, y0=-5, x1=x_val, y1=5, line=dict(color="rgba(150,150,150,0.2)", width=1)))
                shapes.append(dict(type="line", x0=-5*(SQRT3/2), y0=v-2.5, x1=5*(SQRT3/2), y1=v+2.5, line=dict(color="rgba(150,150,150,0.2)", width=1)))
                shapes.append(dict(type="line", x0=-5*(SQRT3/2), y0=v+2.5, x1=5*(SQRT3/2), y1=v-2.5, line=dict(color="rgba(150,150,150,0.2)", width=1)))
            else:
                shapes.append(dict(type="line", x0=v, y0=-5, x1=v, y1=5, line=dict(color="rgba(150,150,150,0.2)", width=1)))
                shapes.append(dict(type="line", x0=-5, y0=v, x1=5, y1=v, line=dict(color="rgba(150,150,150,0.2)", width=1)))

    if show_primary:
        if is_hex: path = f"M 0,0 L {SQRT3/2},0.5 L {SQRT3/2},1.5 L 0,1 Z"
        else: path = "M 0,0 L 1,0 L 1,1 L 0,1 Z"
        shapes.append(dict(type="path", path=path, line=dict(color="orange", width=2, dash="dash"), fillcolor="rgba(0,0,0,0)"))

    if show_ws:
        if is_hex: path = f"M {SQRT3/6},0.5 L {SQRT3/3},0 L {SQRT3/6},-0.5 L {-SQRT3/6},-0.5 L {-SQRT3/3},0 L {-SQRT3/6},0.5 Z"
        else: path = "M -0.5,-0.5 L 0.5,-0.5 L 0.5,0.5 L -0.5,0.5 Z"
        shapes.append(dict(type="path", path=path, line=dict(color="blue", width=2), fillcolor="rgba(59, 130, 246, 0.08)"))

    if show_sym:
        sym_lines = [dict(x0=0, y0=-2, x1=0, y1=2), dict(x0=-2, y0=0, x1=2, y1=0)]
        if is_hex: sym_lines.extend([dict(x0=-SQRT3, y0=-1, x1=SQRT3, y1=1), dict(x0=SQRT3, y0=-1, x1=-SQRT3, y1=1), dict(x0=-1, y0=-SQRT3, x1=1, y1=SQRT3), dict(x0=1, y0=-SQRT3, x1=-1, y1=SQRT3)])
        else: sym_lines.extend([dict(x0=-2, y0=-2, x1=2, y1=2), dict(x0=2, y0=-2, x1=-2, y1=2)])
        for line in sym_lines:
            line.update(dict(type="line", line=dict(color="red", width=1, dash="dashdot")))
            shapes.append(line)

    extent = 2 if show_extended else 0
    calc_extent = 1 # We must calculate with neighbors to catch overlaps at unit cell boundaries
    
    if is_hex:
        cell_poly = Polygon([(0, 0), (SQRT3/2, 0.5), (SQRT3/2, 1.5), (0, 1)])
    else:
        cell_poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    
    all_circles = []

    def process_species(pts, r, color_rgb_str, calc_pts=None):
        for p in pts:
            alpha = 1.0 if p['is_base'] else 0.3
            border_alpha = 1.0 if p['is_base'] else 0.0
            shapes.append(dict(
                type="circle", x0=p['x']-r, y0=p['y']-r, x1=p['x']+r, y1=p['y']+r, 
                fillcolor=f"rgba({color_rgb_str}, {alpha})", line=dict(color=f"rgba({color_rgb_str}, {border_alpha})", width=1.5)
            ))
        
        # Collect circles for the correct true area overlap calc even if visually hidden
        if calc_pts:
            for p in calc_pts:
                all_circles.append(Point(p['x'], p['y']).buffer(r, resolution=64))

    # Process A
    if en_A and 'on' in en_A and sel_A != 'none':
        pts_A = get_points_for_species(ltype, wyckoff.get(sel_A), x_A, extent)
        calc_pts_A = get_points_for_species(ltype, wyckoff.get(sel_A), x_A, calc_extent)
        process_species(pts_A, r_A, "239, 68, 68", calc_pts_A)

    # Process B
    if en_B and 'on' in en_B and sel_B != 'none':
        pts_B = get_points_for_species(ltype, wyckoff.get(sel_B), x_B, extent)
        calc_pts_B = get_points_for_species(ltype, wyckoff.get(sel_B), x_B, calc_extent)
        process_species(pts_B, r_B, "59, 130, 246", calc_pts_B)

    # Process C
    if en_C and 'on' in en_C and sel_C != 'none':
        pts_C = get_points_for_species(ltype, wyckoff.get(sel_C), x_C, extent)
        calc_pts_C = get_points_for_species(ltype, wyckoff.get(sel_C), x_C, calc_extent)
        process_species(pts_C, r_C, "34, 197, 94", calc_pts_C)

    # Calculate actual overlapping areas precisely via Shapely
    if all_circles:
        combined_atoms = unary_union(all_circles)
        atoms_inside_cell = combined_atoms.intersection(cell_poly)
        total_atom_area = atoms_inside_cell.area
    else:
        total_atom_area = 0.0

    shapes.append(dict(type="circle", x0=-0.02, y0=-0.02, x1=0.02, y1=0.02, fillcolor="black", line_color="black"))

    fig.update_layout(
        shapes=shapes,
        xaxis=dict(range=[-2, 2], scaleanchor="y", scaleratio=1, showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-2, 2], showgrid=False, zeroline=False, visible=False),
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="white",
        dragmode="pan"
    )
    
    # Generate Stats Content
    cell_area = SQRT3 / 2 if is_hex else 1.0
    empty_area = cell_area - total_atom_area
    empty_fraction = empty_area / cell_area
    
    stats_ui = html.Div(className="grid grid-cols-1 space-y-1.5 text-gray-800", children=[
        html.Div(className="flex justify-between", children=[
            html.Span("Unit Cell Area:"), html.Span(f"{cell_area:.4f}", className="font-mono text-gray-500")
        ]),
        html.Div(className="flex justify-between", children=[
            html.Span("Total Atom Area:"), 
            html.Span(f"{total_atom_area:.4f}", className="font-mono text-blue-600 font-bold")
        ]),
        html.Div(className="flex justify-between font-bold pt-2 mt-1 border-t border-gray-200", children=[
            html.Span("Empty Fraction:"), 
            html.Span(f"{empty_fraction:.4f}", className="font-mono text-gray-800")
        ]),
        html.Div("(*Calculated using exact geometric intersections, resolving overlays smoothly)", className="text-[10px] text-gray-400 mt-2 italic")
    ])
    
    return fig, stats_ui

if __name__ == '__main__':
    import webbrowser
    from threading import Timer

    def open_browser():
        webbrowser.open_new("http://127.0.0.1:8050/")

    # Open the browser automatically after 1.5 seconds
    Timer(1.5, open_browser).start()
    
    # Run the server with debug=False for production
    app.run(debug=False, port=8050)
