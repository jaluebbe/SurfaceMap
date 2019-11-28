import os
import json
import pandas as pd

path = 'surface_map/maps/globcover2009'
data = pd.read_excel(os.path.join(path, 'Globcover2009_Legend.xls'))
legend = {}
for value, content in data.set_index('Value').to_dict('index').items():
    legend[value] = {'value': value, 'label': content['Label'],
        'color': (content['Red'], content['Green'], content['Blue'])}
with open(os.path.join(path, 'globcover2009_legend.json'), 'w') as f:
    json.dump(legend, f)

