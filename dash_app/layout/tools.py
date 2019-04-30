import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash_cytoscape as cyto
from dash_app.layout.layout_ids import *
from .css_styles import colors3 as colors
from ..components import poagraph as poagraph_component
from ..components import mafgraph as mafgraph_component


def get_tools_tab_content(get_url_function):
    return html.Div(className="tab-content",
                    children=[
                        html.Div(id="tools_intro",
                                 children=[]),
                        dcc.Tabs(id="tabs-tools", value='process', children=[
                            dcc.Tab(label='Multialignment processing',
                                    value='process',
                                    className='tools-tab',
                                    selected_className='tools-tab--selected',
                                    children=get_process_tab_content(get_url_function)),
                            dcc.Tab(label='Visualisation',
                                    value='vis',
                                    className='tools-tab',
                                    selected_className='tools-tab--selected',
                                    children=get_vis_tab_content())
                        ], className='tools-tabs',
                                 ),

                    ])


def get_process_tab_content(get_url_function):
    return [html.Div(
        id=id_process_tab_content,
        children=[
            dcc.Store(id=id_session_state),
            html.Div(className="params_section",
                     children=[html.H4("PoaGraph Construction"),
                               html.Div(className="param",
                                        children=[html.Div("Data type", className="two columns param_name"),
                                                  dcc.RadioItems(
                                                      options=[
                                                          {'label': 'Nucleotides', 'value': 'N'},
                                                          {'label': 'Proteins', 'value': 'P'},
                                                      ],
                                                      value='N'
                                                      , className="seven columns"
                                                  ),
                                                  html.Div(
                                                      "Type of aligned sequences provided in the uploaded multialignment file.",
                                                      className="param_description three columns")]),
                               html.Div(className="param",
                                        children=[html.Div("Multialignment file", className="two columns param_name"),

                                                  html.Div(
                                                      children=[
                                                          dcc.Store(id=id_multalignment_upload_state),
                                                          html.Div(dcc.Upload(id="multialignment_upload",
                                                                              multiple=False,
                                                                              children=[
                                                                                  html.Img(
                                                                                      src=get_url_function(
                                                                                          'alignment.png'),
                                                                                      className='one column file_upload_img',
                                                                                      style={'width': '50px',
                                                                                             'margin': '5px'}
                                                                                  ),
                                                                                  html.Div(html.A(
                                                                                      'Drag & drop MAF file or choose file...'),
                                                                                      className="ten columns")
                                                                              ]),
                                                                   className="file_upload"),
                                                          html.Div(
                                                              id=id_multalignment_upload_state_info,
                                                              style={'visibility': 'hidden', 'width': 'auto', 'margin-top': '5px'}
                                                          )
                                                      ],
                                                      className="seven columns"
                                                  ),
                                                  html.Div(
                                                      children=["Multialignment file. Accepted formats: ", html.A(
                                                          href="http://www1.bioinf.uni-leipzig.de/UCSC/FAQ/FAQformat.html#format5",
                                                          target="_blank", children="maf"), ", ", html.A(
                                                          href="https://github.com/meoke/pang/blob/master/README.md#po-file-format-specification",
                                                          target="_blank", children="po"), ". See example file: ",
                                                                html.A(
                                                                    href="https://github.com/meoke/pang/blob/master/data/Fabricated/f.maf",
                                                                    target="_blank", children="example1.maf")],
                                                      className="param_description three columns")]),
                               html.Div(className="param_group",
                                        id=id_maf_specific_params,
                                        style={"display": "none", "overflow":"auto" },
                                        children=[
                                            html.Div(className="param",
                                                     children=[
                                                         html.Div("Missing nucleotides source", className="two columns param_name"),
                                                         dcc.RadioItems(
                                                             id=id_fasta_provider_choice,
                                                             options=[
                                                                 {'label': "NCBI", 'value': 'NCBI'},
                                                                 {'label': 'Fasta File', 'value': 'File'},
                                                                 {'label': 'Custom symbol', 'value': 'Symbol'},
                                                             ],
                                                             value='NCBI'
                                                             , className="seven columns"
                                                         ),
                                                         html.Div(
                                                             "MAF file may not inlcude full sequences. Specify source of missing nucleotides/proteins.",
                                                             className="param_description three columns")]),
                                            html.Div(className="param",
                                                     id=id_fasta_upload_param,
                                                     style={"display": "none"},
                                                     children=[
                                                         html.Div("Missing symbols file source",
                                                                  className="two columns param_name"),
                                                         html.Div(
                                                             children=[
                                                                 dcc.Store(id=id_fasta_upload_state),
                                                                 html.Div(dcc.Upload(id="fasta_upload",
                                                                                     multiple=False,
                                                                                     children=[
                                                                                         html.I(
                                                                                             className='one column file_upload_img fas fa-align-left fa-3x',
                                                                                             style={'line-height': 'inherit',
                                                                                                    'padding-left': '5px',
                                                                                                    }
                                                                                         ),
                                                                                         html.Div(html.A(
                                                                                             'Drag & drop FASTA/ZIP file or choose file...'),
                                                                                             className="ten columns")
                                                                                     ]),
                                                                          className="file_upload"),
                                                                 html.Div(
                                                                     id=id_fasta_upload_state_info,
                                                                     style={'visibility': 'hidden', 'width': 'auto',
                                                                            'margin-top': '5px'}
                                                                 )
                                                             ],
                                                             className="seven columns"
                                                         ),
                                                         html.Div(
                                                             "Provide zip with fasta files or single fasta file. It must contain full sequeneces which are not fully represented in provided MAF file.",
                                                             className="param_description three columns")])
                                        ])]),
            html.Div(className="params_section",
                     children=[html.H4("Consensus Tree Generation")]),
            html.Div(className="params_section",
                     children=[html.H4("Output Options")]),

            html.Button(id=id_pang_button,
                        children="Process",
                        className='button-primary form_item'),
        ]
    )]


def get_vis_tab_content():
    return html.Div(
        id="vis_tab_content",
        children=[html.Div(id="tools_load_section",
                           children=[
                               html.Div(dcc.Upload(id=id_pangenome_upload,
                                                   children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                                                   multiple=False, ),
                                        className='three columns'),
                               html.Div(children="or load example data: ",
                                        style={'display': 'None', 'textAlign': 'center', 'lineHeight': '60px'},
                                        className='two columns'),
                               dcc.Dropdown(id="example_data_dropdown",
                                            options=[{'label': 'Ebola', 'value': 'Ebola'}],
                                            value='Ebola',
                                            className='five columns form_item'),
                               html.Button(id=id_load_pangenome_button,
                                           children=["Load pangenome"],
                                           className='button-primary form_item')
                           ]
                           ),
                  html.Div(id="tools_info_section",
                           children=[
                               html.Div(id=id_program_parameters,
                                        className='three columns section'),
                               html.Div(id=id_pangenome_info,
                                        className='nine columns section')]
                           ),
                  html.Div(id=id_mafgraph,
                           children=[
                               html.Div(id=id_mafgraph_container,
                                        className='twelve columns section row',
                                        children=[cyto.Cytoscape(id=id_mafgraph_graph,
                                                                 elements=[],
                                                                 layout={'name': 'cose'},
                                                                 style={'width': 'auto', 'height': '300px'},
                                                                 stylesheet=mafgraph_component.get_mafgraph_stylesheet(),
                                                                 # autolock=True,
                                                                 boxSelectionEnabled=False,
                                                                 autoungrabify=True,
                                                                 autounselectify=True)])
                           ]),
                  html.Div(id="tools_poagraph_section",
                           children=[html.Div(id=id_poagraph_container,
                                              className='twelve columns section row',
                                              children=[html.Div(id=id_poagraph_node_info),
                                                        cyto.Cytoscape(id=id_poagraph,
                                                                       layout={
                                                                           'name': 'preset'},
                                                                       stylesheet=poagraph_component.get_poagraph_stylesheet(),
                                                                       elements=[
                                                                       ],
                                                                       style={'width': 'auto', 'height': '500px'},
                                                                       # zoom=1,
                                                                       # minZoom=0.9,
                                                                       # maxZoom=1.1,
                                                                       # panningEnabled=False,
                                                                       # userPanningEnabled=False,
                                                                       boxSelectionEnabled=False,
                                                                       autoungrabify=True,
                                                                       autolock=True,
                                                                       autounselectify=True
                                                                       )

                                                        ]),
                                     html.Div(id=id_full_pangenome_container,
                                              className="twelve columns section row",
                                              children=[dcc.Graph(
                                                  id=id_full_pangenome_graph,
                                                  style={'width': 'auto'},
                                                  # style={'height': '400px', 'width': 'auto'},
                                                  figure={},
                                                  config={
                                                      'displayModeBar': False,
                                                  }
                                              )])
                                     ]
                           ),
                  html.Div(id=id_consensus_tree_container,
                           style={'display': 'none'},
                           children=[
                               html.Div(
                                   id='tree',
                                   children=[
                                       html.Div(
                                           id='graphics',
                                           children=[
                                               dcc.Graph(
                                                   id=id_consensus_tree_graph,
                                                   style={'height': '1000px', 'width': 'auto'}
                                               ),
                                               html.Div(
                                                   [html.Div(
                                                       dcc.Slider(
                                                           id=id_consensus_tree_slider,
                                                           min=0,
                                                           max=1,
                                                           marks={
                                                               int(i) if i % 1 == 0 else i: '{}'.format(i)
                                                               for i
                                                               in
                                                               [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8,
                                                                0.9,
                                                                1]},
                                                           step=0.01,
                                                           value=0.5,
                                                           dots=True
                                                       ),
                                                       style={'margin-top': '1%'},
                                                       className='ten columns'
                                                   ),
                                                       html.P(
                                                           id='consensus_tree_slider_value',
                                                           style={'font-size': 'large'},
                                                           className='two columns'
                                                       )],
                                                   className='row',
                                                   style={'margin-left': '3%',
                                                          'margin-right': '2%',
                                                          'margin-top': '-7%'}
                                               ),
                                           ],
                                           className='nine columns'
                                       ),
                                       html.Div(
                                           id='tree_info',
                                           children=[
                                               html.H5("Metadata in consensuses tree leaves:"),
                                               dcc.Dropdown(
                                                   id=id_leaf_info_dropdown,
                                                   style={'margin-bottom': '20px'},
                                                   options=[
                                                   ],
                                                   value='SEQID'
                                               ),
                                               html.H5("Consensus tree node details:"),
                                               html.H5(
                                                   id=id_consensus_node_details_header
                                               ),
                                               html.Img(
                                                   id=id_consensus_node_details_distribution,
                                               ),
                                               dash_table.DataTable(
                                                   id=id_consensus_node_details_table,
                                                   style_table={
                                                       'maxHeight': '800',
                                                       'overflowY': 'scroll'
                                                   },
                                                   style_cell={'textAlign': 'left'},
                                                   sorting=True
                                               )
                                           ],
                                           style={'padding-top': '7%', 'padding-right': '2%'},
                                           className='three columns'
                                       )
                                   ],
                                   className='row'
                               ),
                               html.Div(
                                   children=[html.Div(
                                       id='consensus_table_info',
                                       children=[
                                           dcc.Markdown("t",  # texts.table_info_markdown,
                                                        className='ten columns'),
                                           html.A(html.Button("Download table as csv",
                                                              id="csv_download",
                                                              disabled=False,
                                                              className='form_item two columns'),
                                                  href='download_csv'),
                                           html.Div(id='hidden_csv_generated',
                                                    style={'display': 'none'})
                                       ],
                                       style={'padding': '2%'}
                                   ),
                                   ],
                                   style={'margin-top': '25px'},
                               )
                           ]
                           ),
                  html.Div(id="consensus_table_container",
                           children=[dash_table.DataTable(id=id_consensuses_table,
                                                          sorting=True,
                                                          sorting_type="multi"),
                                     ],
                           style={'display': 'none'}, className='row')
                  ]
    )
