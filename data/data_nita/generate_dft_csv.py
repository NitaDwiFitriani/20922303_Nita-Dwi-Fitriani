import pandas as pd

# Baca data dari file POSCAR
with open('POSCAR_VFe_8_33%.vasp', 'r') as poscar_file:
    poscar_data = poscar_file.readlines()

# Ekstrak data yang diperlukan dari POSCAR
material_id = poscar_data[0].strip()
scaling_factor = float(poscar_data[1])
lattice_matrix = [list(map(float, line.split())) for line in poscar_data[2:5]]
element_symbols = poscar_data[5].split()
atom_counts = [int(count) for count in poscar_data[6].split()]

# Menentukan jumlah total atom
total_atoms = sum(atom_counts)

# Mencari indeks awal dari bagian posisi atom dalam file POSCAR
start_index = 8  # Indeks baris setelah baris jumlah atom per simbol

# Menyimpan posisi atom dalam list positions
positions = []
for i in range(total_atoms):
    line = poscar_data[start_index + i].split()[:3]  # Hanya menggunakan tiga koordinat pertama
    positions.append([float(coord) for coord in line])

# Ambil informasi tentang lattice
lattice_pbc = [True, True, True]  # Asumsikan selalu menggunakan periode berulang (periodic boundary conditions)

# Persiapkan data dalam bentuk dictionary untuk DataFrame
data_dict = {
    'material_id': [material_id],
    'scaling_factor': [scaling_factor],
    'structure': [{
        'numbers': atom_counts,
        'positions': positions,
        'cell': lattice_matrix,
        'pbc': lattice_pbc
    }],
}

# Buat DataFrame baru
df = pd.DataFrame(data_dict)

# Simpan DataFrame ke dalam file CSV
df.to_csv('OUTPUT_POSCAR_CSV.csv', index=False)
