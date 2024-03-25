import pandas as pd
import json
from periodictable import elements

# Baca data dari file JSON
with open('expanded_structure-mp-1522_2x2.json', 'r') as json_file:
    data = json.load(json_file)

# Ekstrak data yang diperlukan
material_id = data['material_id']
element_symbols = [site['species'][0]['element'] for site in data['structure']['sites']]
numbers = [elements.symbol(element_symbol).number for element_symbol in element_symbols]
positions = [site['xyz'] for site in data['structure']['sites']]
cell = data['structure']['lattice']['matrix']
pbc = data['structure']['lattice']['pbc']
energies = [float(i) for i in range(0, 1001, 20)]  # Generate energy array
phdos = [0.0 for _ in range(len(energies))]  # PHDOS filled with 0.0
pdos = {element_symbol: [0.0 for _ in range(len(energies))] for element_symbol in element_symbols}  # PDOS for each element filled with 0.0

# Buat DataFrame baru
df = pd.DataFrame({
    'material_id': [material_id],
    'structure': [f"{{'numbers': {numbers}, 'positions': {positions}, 'cell': {cell}, 'pbc': {pbc}}}"],
    'energies': [energies],  # Tambahkan array energi ke dalam DataFrame
    'phdos': [phdos],  # Tambahkan PHDOS ke dalam DataFrame
    'pdos': [pdos]  # Tambahkan PDOS ke dalam DataFrame
})

# Simpan DataFrame ke dalam file CSV
df.to_csv('output_mp-1522_2x2.csv', index=False)
