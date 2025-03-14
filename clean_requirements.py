import yaml
import re
import os


def get_conda_packages(yaml_file='environment.yml'):
    """Get package names and versions from environment.yml."""
    packages = {}
    try:
        with open(yaml_file, 'r') as f:
            env_data = yaml.safe_load(f)
        
        # Extract dependencies
        dependencies = env_data.get('dependencies', [])
        for dep in dependencies:
            if isinstance(dep, str):  # Conda-installed packages
                # Match package==version or just package
                match = re.match(r'^([^=]+)=([\d\.]+)=([\w\d_]+)$', dep)
                if match:
                    name, version, _ = match.groups()
                    if version:  # Only include if version is specified
                        packages[name] = version
            elif isinstance(dep, dict) and 'pip' in dep:  # Pip-installed packages
                for pip_dep in dep['pip']:
                    match = re.match(r'^([^=]+)=([\d\.]+)=([\w\d_]+)$', pip_dep)
                    if match:
                        name, version = match.groups()
                        if version:
                            packages[name] = version
    except FileNotFoundError:
        print(f"Error: {yaml_file} not found.")
    except Exception as e:
        print(f"Error parsing {yaml_file}: {e}")
    return packages


def clean_requirements(input_file='requirements.txt', output_file='requirements_clean.txt', yaml_file='environment.yml'):
    """Clean pip freeze output using versions from environment.yml."""
    conda_packages = get_conda_packages(yaml_file)
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        # Match file URI pattern
        if '@ file://' in line:
            package_name = line.split(' @ ')[0].strip()
            version = conda_packages.get(package_name.lower())
            if version:
                cleaned_lines.append(f"{package_name}=={version}")
            else:
                print(f"Warning: No version found for {package_name} in {yaml_file}, keeping original: {line}")
                cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)
    
    with open(output_file, 'w') as f:
        f.write('\n'.join(cleaned_lines))
    print(f"Cleaned requirements written to {output_file}")


if __name__ == '__main__':
    dep_dir = 'dependencies'
    os_list = ['macos', 'win11']
    for os_name in os_list:
        input_file = os.path.join(dep_dir, f'requirements_{os_name}.txt')
        output_file = os.path.join(dep_dir, f'requirements_{os_name}_clean.txt')
        yaml_file = os.path.join(dep_dir, f'environment_{os_name}.yml')
        clean_requirements(input_file, output_file, yaml_file)
