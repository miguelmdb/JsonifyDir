import os
import json

# Function to convert directory structure to JSON
def directory_to_json(dir_path):
    directory_dict = {}
    for root, dirs, files in os.walk(dir_path):
        relative_path = os.path.relpath(root, dir_path)
        sub_dirs = relative_path.split(os.sep)
        current = directory_dict
        for sub_dir in sub_dirs:
            if sub_dir != ".":
                current = current.setdefault(sub_dir, {})
        current['files'] = {}
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    current['files'][file] = f.read()
            except UnicodeDecodeError:
                current['files'][file] = None  # Skip files that can't be decoded
    return directory_dict

# Function to reconstruct directories and files from JSON
def json_to_directory(json_object, output_path):
    for key, value in json_object.items():
        if key == 'files':
            for file_name, file_content in value.items():
                file_path = os.path.join(output_path, file_name)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure directory exists before creating file
                if file_content is not None:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(file_content)
        else:
            sub_dir_path = os.path.join(output_path, key)
            os.makedirs(sub_dir_path, exist_ok=True)
            json_to_directory(value, sub_dir_path)

# Set up the library for pip
class DirJson:
    @staticmethod
    def directory_to_json(dir_path):
        return directory_to_json(dir_path)

    @staticmethod
    def json_to_directory(json_object, output_path):
        json_to_directory(json_object, output_path)


# Example usage
if __name__ == "__main__":
    # Convert directory to JSON
    dir_path = "example_directory"
    dir_path = "/Users/miguel/Documents/GitHub/cryptazon"
    directory_structure = DirJson.directory_to_json(dir_path)
    
    # Save JSON representation
    with open("directory_structure.json", "w") as json_file:
        json.dump(directory_structure, json_file, indent=4)
    
    # Reconstruct directories and files from JSON
    output_path = "output_directory"
    with open("directory_structure.json", "r", encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        DirJson.json_to_directory(json_data, output_path)

