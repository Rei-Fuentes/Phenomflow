import json

with open('/Users/reinerfuentesferrada/ONLINE_DS_THEBRIDGE_Rei/PhenomFlow/Proyecto_Data_Engineering_vlc.ipynb', 'r') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'markdown':
        print(''.join(cell['source']))
        print('-' * 20)
