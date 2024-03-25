from pymatgen.io.vasp import Poscar
from pymatgen.analysis.local_env import VoronoiNN
import numpy as np
import os

def find_nearest_or_farthest_atom_indices(structure, center_point, farthest=False):
    nn = VoronoiNN()
    distances = {}
    for i, site in enumerate(structure):
        dist = nn.get_nn_info(structure, i)[0]['weight']
        distances[i] = dist
    if farthest:
        nearest_atom_index = max(distances, key=distances.get)
    else:
        nearest_atom_index = min(distances, key=distances.get)
    return nearest_atom_index

def calculate_center_of_mass(structure):
    total_mass = sum(site.specie.atomic_mass for site in structure)
    center_of_mass = np.array([0.0, 0.0, 0.0])
    for site in structure:
        center_of_mass += site.coords * site.specie.atomic_mass
    return center_of_mass / total_mass

def create_random_vacancy_based_on_distance(poscar_file, vacancy_count=1, farthest=False):
    # Baca file POSCAR
    poscar = Poscar.from_file(poscar_file)
    structure = poscar.structure
    
    # Hitung pusat massa
    center_point = calculate_center_of_mass(structure)
    
    # Dapatkan indeks atom untuk setiap vacancy
    vacancy_indices = []
    for _ in range(vacancy_count):
        atom_index = find_nearest_or_farthest_atom_indices(structure, center_point, farthest=farthest)
        vacancy_indices.append(atom_index)
        structure.remove_sites([atom_index])
    
    # Hitung presentase vacancy
    total_atoms = len(poscar.structure)  # Menggunakan len(structure) sebagai jumlah total atom
    vacancy_percentage = (vacancy_count / total_atoms) * 100
    vacancy_type = "Nearest" if not farthest else "Farthest"
    # Dapatkan nama material dari nama file atau dari data struktur
    material_name = os.path.splitext(os.path.basename(poscar_file))[0]  # Ambil nama file tanpa ekstensi
    
    # Simpan presentase vacancy dan nama material dalam nama file POSCAR
    vacancy_percentage_str = "{:.2f}".format(vacancy_percentage)  # Batasi angka desimal menjadi dua digit
    # output_filename = f"VAC_POSCAR_{material_name}_{vacancy_percentage_str.replace('.', '_')}%.vasp"
    output_filename = f"VAC_POSCAR_{material_name}_{vacancy_type}_{vacancy_percentage_str.replace('.', '_')}%.vasp"
    
    # Simpan struktur atom setelah vacancy dihilangkan
    with open(output_filename, "w") as f:
        f.write(f"Material: {material_name}\n")
        f.write(f"Presentase vacancy: {vacancy_percentage:.2f}%\n")
        f.write(structure.to(fmt="poscar"))  # Menyimpan struktur atom setelah vacancy dihilangkan
        
    # Simpan struktur atom asli sebelum vacancy dihilangkan
    original_output_filename = f"ORI_POSCAR_{material_name}.vasp"
    with open(original_output_filename, "w") as f:
        f.write(f"Material: {material_name}\n")
        f.write(f"Original Structure\n")
        f.write(poscar.structure.to(fmt="poscar"))  # Menyimpan struktur atom asli sebelum vacancy dihilangkan

# Contoh penggunaan untuk vacancy berdasarkan jarak terdekat
poscar_file = "data/data_nita/supercell-FeS/FeS_Hexagonal.vasp"  # Ganti dengan nama file POSCAR Anda
create_random_vacancy_based_on_distance(poscar_file, vacancy_count=3)

# Contoh penggunaan untuk vacancy berdasarkan jarak terjauh
create_random_vacancy_based_on_distance(poscar_file, vacancy_count=5, farthest=True)
