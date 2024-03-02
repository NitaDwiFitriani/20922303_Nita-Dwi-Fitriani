import json
from collections import Counter
from periodictable import elements

# Baca data dari file JSON
with open('expanded_structure-mp-1522_5x5.json', 'r') as json_file:
    data = json.load(json_file)

# Ekstrak data yang diperlukan
material_id = data['material_id']
element_symbols = [site['species'][0]['element'] for site in data['structure']['sites']]
positions = [site['xyz'] for site in data['structure']['sites']]
cell = data['structure']['lattice']['matrix']

# Hitung jumlah atom masing-masing elemen
element_counts = Counter(element_symbols)

# Buat file POSCAR baru
with open('POSCAR-mp-1522_5x5', 'w') as poscar_file:
    poscar_file.write(f"{material_id}\n")
    poscar_file.write("1.0\n")
    for row in cell:
        poscar_file.write(f"{row[0]:20.10f} {row[1]:20.10f} {row[2]:20.10f}\n")
    poscar_file.write(' '.join(map(str, element_counts.values())) + '\n')
    poscar_file.write(' '.join(element_counts.keys()) + '\n')
    poscar_file.write("Direct\n")
    for row in positions:
        poscar_file.write(f"{row[0]:20.10f} {row[1]:20.10f} {row[2]:20.10f}\n")

print("File POSCAR-mp-1522_5x5 telah berhasil dibuat.")
print("Jumlah atom masing-masing elemen:", element_counts)
