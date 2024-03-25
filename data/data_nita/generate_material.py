import requests
import json
from pymatgen.ext.matproj import MPRester
from pymatgen.core.structure import Structure

# Replace "YOUR_API_KEY" with your Material Project API key
api_key = "20l2L2OC4j9vuWM2DWNb3MPgkFMdRpIh"

# Initialize MPRester with the API key
mpr = MPRester(api_key)

# Material ID for the initial structure
material_id = "mp-1522"

# Get information about the initial structure from Material Project API
structure = mpr.get_structure_by_material_id(material_id)

# Create an expanded unit cell (2x2x2)
expanded_structure = structure * [2, 2, 2]

# Create a dictionary with the material ID and structure data
material_data = {
    "material_id": material_id,
    "structure": expanded_structure.as_dict()
}

# Save the structure and material ID to a JSON file with pretty formatting
with open("expanded_structure-mp-1522_2x2.json", "w") as json_file:
    json.dump(material_data, json_file, indent=4)

