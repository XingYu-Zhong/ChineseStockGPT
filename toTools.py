import yaml
import json
import os
output_dir = 'tmp'
yaml_file_path = 'StockMarketAsisstant-master/openapi.yaml'
def convert_parameter_type(openapi_type):
    """Convert OpenAPI parameter types to the expected format."""
    if openapi_type == "string":
        return "string"
    elif openapi_type == "integer":
        return "integer"
    elif openapi_type == "number":
        return "number"
    else:
        return "string"  # Default to string if type is unknown

def convert_openapi_to_tools(openapi_file_path):
    """Convert OpenAPI paths to tools format."""
    tools = []

    with open(openapi_file_path, 'r', encoding='utf-8') as file:
        openapi_data = yaml.safe_load(file)

    for path, methods in openapi_data['paths'].items():
        for method, details in methods.items():
            tool = {
                "type": "function",
                "function": {
                    "name": details.get("operationId", ""),
                    "description": details.get("summary", ""),
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
            for param in details.get("parameters", []):
                param_name = param["name"]
                param_type = param["schema"]["type"]
                param_description = param.get("description", "")
                param_required = param.get("required", False)

                tool["function"]["parameters"]["properties"][param_name] = {
                    "type": convert_parameter_type(param_type),
                    "description": param_description
                }
                if param_required:
                    tool["function"]["parameters"]["required"].append(param_name)
            tools.append(tool)
    
    return tools



def extract_paths_and_operation_ids(openapi_file_path):
    """Extract paths and corresponding operationIds from an OpenAPI YAML file."""
    path_operation_id_map = {}

    with open(openapi_file_path, 'r', encoding='utf-8') as file:
        openapi_data = yaml.safe_load(file)

    for path, methods in openapi_data['paths'].items():
        for method, details in methods.items():
            operation_id = details.get("operationId")
            if operation_id:
                path_operation_id_map[operation_id] = path

    return path_operation_id_map

# Replace 'openapi.yaml' with the path to your OpenAPI YAML file
path_operation_id_map = extract_paths_and_operation_ids(yaml_file_path)


if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the path_operation_id_map to a JSON file in the tmp directory
path_operation_id_map_file = os.path.join(output_dir, 'path_operation_id_map.json')
with open(path_operation_id_map_file, 'w', encoding='utf-8') as f:
    json.dump(path_operation_id_map, f, ensure_ascii=False, indent=4)

print(path_operation_id_map)

# Replace 'openapi.yaml' with the path to your OpenAPI YAML file
tools = convert_openapi_to_tools(yaml_file_path)

# Save the tools list to a JSON file in the tmp directory
tools_file = os.path.join(output_dir, 'tools.json')
with open(tools_file, 'w', encoding='utf-8') as f:
    json.dump(tools, f, ensure_ascii=False, indent=4)

print(tools)