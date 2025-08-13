import re
import os
from packaging import version    # For version comparison


def parse_requirements(file_path):
    """Parse a requirements file into a dict of package:version."""
    packages = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):    # Skip empty lines and comments
                    match = re.match(r'^([^=]+)==([\d\.]+)$', line)
                    if match:
                        name, ver = match.groups()
                        packages[name] = ver
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    return packages


def merge_requirements(win_file, mac_file, output_file='requirements.txt'):
    """Merge two requirements files, using latest version for conflicts."""
    win_packages = parse_requirements(win_file)
    mac_packages = parse_requirements(mac_file)
    
    # Combine all package names
    all_packages = set(win_packages.keys()).union(mac_packages.keys())
    
    merged = {}
    for pkg in all_packages:
        win_ver = win_packages.get(pkg)
        mac_ver = mac_packages.get(pkg)
        
        if win_ver and mac_ver:    # Package in both files
            if win_ver == mac_ver:
                merged[pkg] = win_ver
            else:    # Compare versions and take the minimum
                try:
                    min_ver = min(version.parse(win_ver), version.parse(mac_ver))
                    merged[pkg] = str(min_ver)
                    print(f"Warning: Version conflict for {pkg} - Win11: {win_ver}, macOS: {mac_ver}. Using {min_ver}.")
                except version.InvalidVersion:
                    print(f"Error: Invalid version for {pkg}. Win11: {win_ver}, macOS: {mac_ver}. Skipping.")
        elif win_ver:    # Only in Win11
            merged[pkg] = win_ver
        elif mac_ver:    # Only in macOS
            merged[pkg] = mac_ver
    
    # Write merged requirements
    with open(output_file, 'w') as f:
        for pkg, ver in sorted(merged.items()):
            f.write(f"{pkg}=={ver}\n")
    print(f"Merged requirements written to {output_file}")


if __name__ == '__main__':
    win_file = os.path.join('dependencies', 'requirements_win11.txt')
    mac_file = os.path.join('dependencies', 'requirements_macos.txt')
    merge_requirements(win_file, mac_file)
