#!/usr/bin/env python3
"""
Detect JavaScript project type (client-side or server-side) and return appropriate security prompt file.
"""

import os
import json
import sys
from pathlib import Path


def detect_project_type(project_dir):
    """
    Detect if the project is client-side or server-side based on package.json and file structure.
    
    Returns:
        tuple: (project_type, confidence, indicators)
        - project_type: 'client', 'server', 'both', or 'unknown'
        - confidence: float between 0.0 and 1.0
        - indicators: dict with detected indicators
    """
    indicators = {
        'client_signals': [],
        'server_signals': [],
        'package_json': None,
        'directory_structure': {}
    }
    
    project_path = Path(project_dir)
    package_json_path = project_path / 'package.json'
    
    # Check package.json
    if package_json_path.exists():
        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                pkg_data = json.load(f)
                indicators['package_json'] = pkg_data
                
                deps = {**pkg_data.get('dependencies', {}), **pkg_data.get('devDependencies', {})}
                
                # Client-side frameworks/libraries
                client_packages = [
                    'vue', 'react', 'angular', '@angular/core',
                    'vuex', 'redux', 'vue-router', 'react-router',
                    'webpack', 'vite', 'parcel', 'rollup',
                    'vuetify', '@mui/material', 'antd',
                    'axios', 'vue-axios'
                ]
                
                # Server-side frameworks/libraries
                server_packages = [
                    'express', 'koa', 'fastify', 'hapi',
                    'pg', 'mysql', 'mongodb', 'sequelize',
                    'jsonwebtoken', 'bcrypt', 'bcryptjs',
                    'passport', 'cors', 'helmet',
                    'multer', 'body-parser'
                ]
                
                for pkg in client_packages:
                    if pkg in deps:
                        indicators['client_signals'].append(f"package: {pkg}")
                
                for pkg in server_packages:
                    if pkg in deps:
                        indicators['server_signals'].append(f"package: {pkg}")
                        
        except Exception as e:
            print(f"Warning: Could not parse package.json: {e}", file=sys.stderr)
    
    # Check directory structure
    client_dirs = ['src/components', 'src/views', 'public', 'dist', 'build']
    server_dirs = ['routes', 'models', 'controllers', 'middleware', 'config']
    
    for dir_name in client_dirs:
        dir_path = project_path / dir_name
        if dir_path.exists() and dir_path.is_dir():
            indicators['client_signals'].append(f"directory: {dir_name}")
            indicators['directory_structure'][dir_name] = True
    
    for dir_name in server_dirs:
        dir_path = project_path / dir_name
        if dir_path.exists() and dir_path.is_dir():
            indicators['server_signals'].append(f"directory: {dir_name}")
            indicators['directory_structure'][dir_name] = True
    
    # Check for specific files
    if (project_path / 'index.html').exists():
        indicators['client_signals'].append("file: index.html")
    
    if (project_path / 'server.js').exists() or (project_path / 'app.js').exists():
        indicators['server_signals'].append("file: server.js or app.js")
    
    # Determine project type
    client_score = len(indicators['client_signals'])
    server_score = len(indicators['server_signals'])
    
    if client_score == 0 and server_score == 0:
        return 'unknown', 0.0, indicators
    
    total_score = client_score + server_score
    confidence = max(client_score, server_score) / total_score if total_score > 0 else 0.0
    
    if client_score > server_score * 2:
        return 'client', confidence, indicators
    elif server_score > client_score * 2:
        return 'server', confidence, indicators
    elif client_score > 0 and server_score > 0:
        return 'both', confidence, indicators
    else:
        return 'unknown', 0.0, indicators


def get_prompt_file(project_type):
    """
    Get the appropriate security prompt file based on project type.
    
    Returns:
        str: relative path to the prompt file
    """
    if project_type == 'client':
        return 'references/cli-security-prompt.md'
    elif project_type == 'server':
        return 'references/sv-security-prompt.md'
    elif project_type == 'both':
        return 'references/both'  # Will be handled specially
    else:
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: detect_project_type.py <project_directory>", file=sys.stderr)
        sys.exit(1)
    
    project_dir = sys.argv[1]
    
    if not os.path.isdir(project_dir):
        print(f"Error: {project_dir} is not a directory", file=sys.stderr)
        sys.exit(1)
    
    project_type, confidence, indicators = detect_project_type(project_dir)
    
    result = {
        'project_type': project_type,
        'confidence': confidence,
        'indicators': indicators,
        'prompt_file': get_prompt_file(project_type)
    }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
