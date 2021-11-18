import datetime
from datetime import date

import pandas as pd
import json
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__)
server=app.server

df=pd.read_csv('dummy.csv')

col=list(df.columns)
#print(col[len(col)-1])
layout=[]
output=[]
input=[]
dat={}
dd1=[]
dd2=[]

ward_61 = json.load(open('ward61.geojson', 'r'))
regions = json.load(open('region_ward61.geojson', 'r'))


dfd = pd.read_csv('ward61_dummy.csv')

date_list=dfd['coll_date']
date_list=pd.to_datetime(date_list)
min_d=date_list.min()
max_d=date_list.max()
#dfr = pd.read_csv('dummy_r.csv')
radio=list(dfd.columns)
for i in range(0,12,1):
    radio.pop(0)
l = []
rad_graph=[]
for i in range(2,len(col)):
    rad_graph.append(col[i])
# handling null values in geojson
# i = 0
# for feature in ward_61['features']:
#     if feature['properties']['name'] is None:
#             feature['properties']['name'] = 'random_' + str(i)
#             i += 1
#     l.append(feature['properties']['name'])
i=0
building_id_map = {}
reg_map={}
#mapping geojson with csv using id columns (osm_id)
for feature in ward_61["features"]:
    # feature["properties"]["oid"]=i
    # feature["id"] = feature["properties"]["osm_id"]
    feature["id"] = i
    i+=1
    building_id_map[feature["properties"]["name"]] = feature["id"]

dfd["id"] = dfd["name"].apply(lambda x: building_id_map[x])
i=0
# for feature in regions["features"]:
#     # feature["properties"]["oid"]=i
#     # feature["id"] = feature["properties"]["id"]
#     feature["id"] = i
#     i+=1
#     reg_map[feature["properties"]["region_nam"]] = feature["id"]
#
# dfr["id"] = dfr["region_nam"].apply(lambda x: reg_map[x])

#print(dfd)

#function to create marks on date slider


# def slider_dic():
#     dat={}
#     d = date_list['Date'].unique()
#     d.sort()
#     j=0
#     for i in d:
#         dat[j] = i
#         j+=1
#     return dat

#marks dictionary for date slider

# dat=slider_dic()

# layout.append(dbc.Row(dbc.Col([html.Br(),html.H1("DASHBOARD"),html.Br()],
#                         width={'size': 8, 'offset': 5},
#                         ),
#                 ))
# layout.append(dbc.Row(dbc.Col(html.P('Select Date'),
#                               width={'size': 6},)))
# layout.append(dbc.Row(dbc.Col(html.Div([
#     dcc.Slider(
#         id='my-slider',
#         min=0,
#         max=len(dat)-1,
#         step=1,
#         marks=dat,
#         value=0,
#     ),
#     html.Div(id='slider-output-container',children=["date selected is: "+dat[0]])
# ]),
# width=10), justify="center"
# ))

#adding dropdowns to layout

# for i in range(0,len(col)):
#     dd1.append(dbc.Col(
#         html.H5(col[i]),
#         width=3
#     ))
# layout.append(dbc.Row(dd1))
###UNCOMMENT FROM HERE IF NEEDED######
# dd2.append(dbc.Col(html.Div([
#     html.H5(col[0]),
#     dcc.Dropdown(
#       id=col[0],
#       options=[{"label":x,"value":x} for x in df[col[0]].unique()]
#
#  )]),
#       width=3,
#       xs=10, sm=6, md=6, lg=3, xl=3,
#     ),
#
# )
#
# for i in range(1,len(col)):
#     dd2.append(dbc.Col(html.Div([
#         html.H5(col[i]),
#         dcc.Dropdown(
#         id=col[i],
#         options=[]
#     ),
#         ]),
#     width=3,
#     xs=10, sm=6, md=6, lg=3, xl=3,),
#
#
#     )
dd2.append(html.Div([
               html.H6("         "+"    Select Waste Type:"),
               dcc.RadioItems(
                   id='waste_type',
                   options=[{'value': x, 'label':"    "+ x+"     "+"   "+ "    "}
                            for x in radio],
                   value=radio[0],
                   labelStyle={'display': 'block'}
               ),
               html.H6("Select Area:"),
               dcc.RadioItems(
                   id='area',
                   options=[{'value': x, 'label': "    " + x + "  " +"     "+ "       "}
                            for x in rad_graph],
                   value=rad_graph[0],
                   labelStyle={'display': 'block'}
               )
           ]))
dd2.append(html.Div([
    html.H6(col[0]),
    dcc.Dropdown(
      id=col[0],
      options=[{"label":x,"value":x} for x in df[col[0]].unique()]

 )]),
)

for i in range(1,len(col)):
    dd2.append(html.Div([
        html.H6(col[i]),
        dcc.Dropdown(
        id=col[i],
        options=[]
    ),
        ]))
    # width=3,
    # xs=10, sm=6, md=6, lg=3, xl=3,),
#
# layout.append(dbc.Row([dbc.Col(html.Div(
#     [
#      html.H5("Select Waste Type:"),
#      dcc.RadioItems(
#          id='waste_type',
#          options=[{'value': x, 'label': x}
#                   for x in radio],
#          value=radio[0],
#          labelStyle={'display': 'inline-block'}
#      ),
#      html.H5("Select Area:"),
#      dcc.RadioItems(
#          id='area',
#          options=[{'value': x, 'label': "    "+x+"   "}
#                   for x in col],
#          value=col[2],
#          labelStyle={'display': 'inline-block'}
#      ),
#
#
#      ]),
#     #add width here
#     width={'size': 3, 'offset': 0},
# ),
#     dbc.Col([
#
#         dcc.Graph(id='choropleth', figure={})
#
#     ])
#     ]))

layout.append(dcc.Tab(label='MAP', children=[dbc.Row([dbc.Col(dbc.Card(dd2,body=True, color="light"
                              ),width={'size': 4, 'offset': 0},xs=10, sm=10, md=10, lg=4, xl=4,),
               dbc.Col([

                   dbc.Card([html.Br(), dcc.Graph(id='choropleth',figure={}),html.Br()],body=True, color="secondary")

                    ],width={'size': 8, 'offset': 0},xs=10, sm=10, md=10, lg=8, xl=8,)
                       ])]))
#########GRAPH STARTS HERE##############


# layout.append(dbc.Row(dbc.Col([
#                         html.Br(),
#                         html.Hr(),
# ],
#                         width={'size': 12, 'offset': 0},
#                         ),
#                 ))
############# GRAPH STARTS HERE###########################
# layout.append(dbc.Row(dbc.Col([
#
#                         html.Br(),
#                         #html.Hr(),
#                         html.H2("DAILY WASTE COLLECTION"),
#                         html.Br(),
#                             ],
#                         width={'size': 7, 'offset': 4},
#                         ),
#                 ))

# adding radio buttons

# layout.append(dbc.Row(dbc.Col((html.P("Select Waste Type:"))
#                               ,width={'size': 8, 'offset': 1})))
# layout.append(dbc.Row([
#     dbc.Col([
#
#     dcc.RadioItems(
#         id='waste_type',
#         options=[{'value': x, 'label': x}
#                  for x in radio],
#         value=radio[0],
#         labelStyle={'display': 'inline-block'}
#     )
#     ], width={'size': 8, 'offset': 1})
# ]
#
# ))
#
# layout.append(dbc.Row(dbc.Col((html.P("Select Area:"))
#                               ,width={'size': 8, 'offset': 1})))
# layout.append(dbc.Row([
#     dbc.Col([
#
#     dcc.RadioItems(
#         id='area',
#         options=[{'value': x, 'label': x}
#                  for x in col],
#         value=col[2],
#         labelStyle={'display': 'inline-block'}
#     )
#     ], width={'size': 8, 'offset': 1})
# ]
#
# ))

# layout.append(dbc.Row([
#     dbc.Col([
#
#         dcc.Graph(id='choropleth',figure={})
#
#     ])
# ]))


# rad_graph=[]
# for i in range(2,len(col)):
#     rad_graph.append(col[i])
layout.append(dcc.Tab(label='GRAPH',children=[dbc.Row(dbc.Col([

                        html.Br(),
                        #html.Hr(),
                        html.H2("DAILY WASTE COLLECTION"),
                        html.Br(),
                            ],
                        width={'size': 7, 'offset': 4},
                        ),
                ),
    dbc.Row([
    dbc.Col([ dbc.Card([
        html.Div([

                html.H5("Select Area"),
                dcc.RadioItems(
                    id='graph_radio',
                    options=[{'value': x, 'label':"        " +x+ "          "}
                             for x in rad_graph],
                    value=rad_graph[0],
                    labelStyle={'display':'block'}
                ),

       ]),

        html.Div([
                html.H5(""),
                html.H5("Select Name"),
                dcc.Dropdown(
                    id='graph_op',
                    options=[],
                    multi=True
                )]
        ),
        html.Div([
            html.H5(""),
            html.H5("Select Date Range"),
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=min_d,
                max_date_allowed=max_d,
                initial_visible_month=min_d,
                end_date=max_d,
                start_date=min_d
            ),

        ]),

        html.Div([
            html.H5(""),
            html.H5("Select Waste Type"),
            dcc.RadioItems(
                id='waste_t',
                options=[{'value': x, 'label':"   "+ x+"    "}
                             for x in radio],
                value=radio[0],
                labelStyle={'display': 'block'}
          )
        ])

    ],body=True, color="light")
    ],width={'size': 4, 'offset': 0},xs=10, sm=10, md=10, lg=4, xl=4,),
    dbc.Col(
        dcc.Graph(id="line-chart"),
    width={'size': 8, 'offset': 0},xs=10, sm=10, md=10, lg=8, xl=8,)
              ])]))
# layout.append(html.P(col[0]))           #topmost dropdown
# layout.append(dcc.Dropdown(
#     id=col[0],
#     options=[{"label":x,"value":x} for x in df[col[0]].unique()]
# ))
# for i in range(1,len(col)):             #remaining dropdowns
#     layout.append(html.P(col[i]))
#     layout.append(dcc.Dropdown(
#         id=col[i],
#         options=[]
#     ))

#input list for app callback

for i in range(0,len(col)-1):
    input.append(Input(col[i],'value'))
#print(input)

#output list for app callback

for i in range(1,len(col)):
    output.append(Output(col[i],'options'))
#print(output)

#passing layout list with all components to app layout
app.layout=html.Div([dbc.Row(dbc.Col([html.Br(),html.H1("DASHBOARD"),html.Br()],
                        width={'size': 8, 'offset': 5},
                        ),
                ),
                     dcc.Tabs(layout)])

#app call back to connect input and output components here diff dropdowns
@app.callback(
    output,
    input
)
def drop(*args):
    arg=[]
    op=[]
    dff=df.copy()
    for x in args:
        arg.append(x)
    for i in range(0,len(col)-1):
        dff=dff[dff[col[i]]==arg[i]]
      #  lists.append(dff[col[i]].unique())
        op.append([{"label":k,"value":k} for k in dff[col[i+1]].unique()])
    return tuple(op)


# @app.callback(
#     Output('slider-output-container','children'),
#     Input('my-slider','value')
# )
# def date_selected(date):
#     return "date selected is: "+str(dat[date])



# @app.callback(
#     Output('choropleth','figure'),
#     [Input('waste_type','value'),
#      ]
# )
# def show_map(val):
#     fig = px.choropleth(
#         dfd,
#         locations="id",
#         geojson=ward_61,
#         color=val,
#     )
#     fig.update_geos(fitbounds="locations", visible=False)
#     return fig
data=dfd
geo=regions
ip=[]
ip.append(Input('waste_type','value'))
ip.append(Input('area','value'))
for i in range(3,len(col)):
    ip.append(Input(col[i],'value'))
@app.callback(
    Output('choropleth','figure'),
    ip
)
def show_map(*args):
    arg=[]
    col_name='region'
    for x in args:
        arg.append(x)
    if arg[1]=='Ward':
        geo=regions
        col_name = 'region'
        ##CREATING DATAFRAME FOR REGIONS

        # print(dfd)

        reg = dfd['region'].unique()

        dat = []

        fields = ['region']
        for i in radio:
            fields.append(i)
        for i in reg:
            l = []
            l.append(i)
            for i in range(len(radio)):
                l.append(0)
            dat.append(l)

        for ind in dfd.index:
            for li in dat:
                if li[0] == dfd['region'][ind]:
                    j=1
                    for i in radio:
                        li[j] += dfd[i][ind]
                        j+=1


        data = pd.DataFrame(dat, columns=fields)
        i=0
        map={}
        for feature in geo["features"]:
            # feature["properties"]["oid"]=i
            # feature["id"] = feature["properties"]["osm_id"]
            feature["id"] = i
            i += 1
            map[feature["properties"]["region_nam"]] = feature["id"]

        data["id"] = data["region"].apply(lambda x: map[x])
    elif arg[1]=='Region':
        geo=ward_61.copy()
        col_name = 'building_cluster'
        ##CREATING DATAFRAME FOR BUILDING CLUSTERS

        # print(dfd)

        # reg = dfd['building_cluster']
        # bn = dfd['name']
        dat = []

        fields = ['building_cluster', 'name']
        for i in radio:
            fields.append(i)
       # dfr=dfd.groupby(['building_cluster','name'], as_index=False)['name'].
        dfc=dfd.copy()
        dfr = dfc.drop_duplicates(['name', 'building_cluster'])[['name', 'building_cluster']]

        for i in dfr.index:
            l = []
            l.append(dfr['building_cluster'][i])
            l.append(dfr['name'][i])
            for j in range(len(radio)):
                l.append(0)
            dat.append(l)

        for ind in dfd.index:
            for li in dat:
                if li[0] == dfd['building_cluster'][ind]:
                    j=2
                    for i in radio:
                        li[j] += dfd[i][ind]
                        j+=1

        data = pd.DataFrame(dat, columns=fields)
       # print(data)
        i=0
        map={}
        for feature in geo["features"]:
            # feature["properties"]["oid"]=i
            # feature["id"] = feature["properties"]["osm_id"]
            feature["id"] = i
            i+=1

            map[feature["properties"]["name"]] = feature["id"]

        data["id"] = data["name"].apply(lambda x: map[x])
       # PREPARING GEOJSON
        feat = []
        for i in ward_61['features']:
            if (i['properties']['region'] == arg[2]):
                feat.append(i)
        mody = ward_61.copy()
        mody['features'] = feat
        geo=mody
    if arg[1]=='Building_Cluster':
        feat = []
        col_name = 'name'
        for i in ward_61['features']:
            if (i['properties']['building_cluster'] == arg[3]):
                feat.append(i)
        mody = ward_61.copy()
        mody['features'] = feat
        data=dfd
        geo=mody
    fig = px.choropleth(
        data,
        locations="id",
        geojson=geo,
        color=arg[0],
        hover_name=col_name,
        hover_data=[arg[0],col_name]
    )
    fig.update_geos(fitbounds="locations", visible=False)
    return fig

@app.callback(
    [Output('graph_op','options'),
    Output('graph_op','value')],
    Input('graph_radio','value')
)
def populate(sel):
    op=[]
    #if sel=='Ward':
    dff=df.copy()
    li=list(dff[sel].unique())
    for k in li:
        op.append({'label':k,'value':k})
    return op,li

@app.callback(
    Output("line-chart", "figure"),
    [
        Input('graph_op','value'),
        Input('graph_radio','value'),
        Input('waste_t','value'),
        Input('my-date-picker-range','start_date'),
        Input('my-date-picker-range','end_date')
    ]
)
def draw_graph(col,val,wt,sd,ed):
    dft=dfd.copy()


    dft['coll_date'] = pd.to_datetime(dft['coll_date'])
    dft['col_date']=dft['coll_date']
   # dft = dft[dft['coll_date'].loc[2021-10-1:2021-10-31]]
    #dft['coll_date'] = pd.to_datetime(df['coll_date'])
   # dft = dft.set_index('col_date')
    v=str(val)
    date=[]
    # sd=datetime.date(sd)
    # ed=datetime.date(ed)
    print(sd)
    print(ed)

    # for i in range(sd,ed):
    #     date.append(i)
    dft = dft.groupby([v.lower(),'coll_date'], as_index=False)[wt].sum()
    dft = dft[dft[v.lower()].isin(col)]
    # dft = dft[dft['coll_date'].isin(date)]
    #dft = dft.loc[sd:ed]
    #dft = dft.set_index('coll_date')
    print(dft)
    waste=str(wt).upper()
    fig = px.line(dft,
                  x="coll_date", y=wt, color=v.lower())
    fig.update_layout(yaxis={'title': waste},
                      xaxis={'title': 'COLLECTION DATE'},
                      title={'text': waste+" COLLECTION",
                             'font': {'size': 20}, 'x': 0.5, 'xanchor': 'center'}
)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)