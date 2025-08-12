
def test_json():
    import json
    import numpy as np
    from pathlib import Path

    # Load the JSON file
    json_file_path = str(Path(__file__).parent.parent) + "/labs/labsConfig.json"
    
    # Check if the file exists
    assert Path(json_file_path).is_file(), f"JSON file not found at {json_file_path}"

    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Check if the data is a dictionary
    assert isinstance(data, dict), "JSON data should be a dictionary"
    assert "labs" in data, "JSON data should contain a 'labs' key"
    labs = data["labs"]

    # Check for required keys
    required_keys = ["name"]
    for key in required_keys:
        for lab in labs:
            assert key in lab, f"Missing required key '{key}' in lab: {lab}"

    # Check for required labs
    required_labs = ["introduction", "lab_models", "lab_inversekinematics", "project_pickandplace", "lab_design", "lab_closedloop", "sandbox"]
    for lab in labs:
        assert lab["name"] in required_labs, f"Unexpected lab found: {lab}"
    for required_lab in required_labs:
        assert any(lab["name"] == required_lab for lab in labs), f"Required lab '{required_lab}' not found in JSON data"

