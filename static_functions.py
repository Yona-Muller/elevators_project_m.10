import json
import re

def update_general_settings(json_path='data.json', config_path='config.py'):
    """
    Reads general settings from a flat JSON and updates constants in config.py.
    If constants are missing in config.py, they will be added.

    Args:
        json_path (str): Path to the JSON file containing the general settings.
        config_path (str): Path to the config.py file to be updated.
    """
    # Load the general settings from the JSON file
    with open(json_path, 'r') as file:
        general = json.load(file)  # The JSON is now a flat dictionary

    # Read current config file
    with open(config_path, 'r') as f:
        config_lines = f.readlines()

    # Prepare key-value pairs for constants (uppercase)
    general_keys = {key.upper(): repr(value) for key, value in general.items()}
    pattern = re.compile(r"^([A-Z_]+)\s*=\s*(.+)$")  # Pattern to match constants

    updated_lines = []
    for line in config_lines:
        match = pattern.match(line)
        if match:
            var_name = match.group(1)
            if var_name in general_keys:
                # Update existing constants in config.py
                updated_lines.append(f"{var_name} = {general_keys.pop(var_name)}\n")
                continue
        updated_lines.append(line)

    # Add any missing constants to the config
    if general_keys:
        updated_lines.append("\n# Added missing general settings\n")
        for key, value in general_keys.items():
            updated_lines.append(f"{key} = {value}\n")

    # Write the updated content back to config.py
    with open(config_path, 'w') as f:
        f.writelines(updated_lines)

    print(f"✅ General settings updated in: {config_path}")


def load_buildings_array(json_path='buildings.json'):
    """
    Reads a buildings JSON file and returns an array of tuples with (num_floors, num_elevators).
    
    Args:
        json_path (str): Path to the JSON file containing building data.
        
    Returns:
        List[Tuple[int, int]]: A list of tuples with (number_of_floors, number_of_elevators).
    """
    # Load the building data from the JSON file
    with open(json_path, 'r') as file:
        buildings = json.load(file).get("buildings", {})

    building_list = []
    i = 0
    while f"building_{i}" in buildings:
        b = buildings[f"building_{i}"]
        # Append the building info as a tuple (number_of_floors, number_of_elevators)
        building_list.append((b['number_of_floors'], b['number_of_elevators']))
        i += 1

    return building_list
