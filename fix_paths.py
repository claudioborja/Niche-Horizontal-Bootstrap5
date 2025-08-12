#!/usr/bin/env python3
"""
Script mejorado para corregir TODAS las rutas después de la reorganización
"""
import os
import re

def fix_navigation_paths(file_path):
    """Corrige las rutas de navegación en un archivo HTML según su ubicación"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        base_dir = '/var/www/html/niche_horizontal'
        
        # Calcular la profundidad del archivo (cuántos niveles está del raíz)
        relative_path = file_path.replace(base_dir + '/', '')
        depth = relative_path.count('/')
        
        if depth > 0:  # Archivo está en subdirectorio
            # Prefijo para volver al directorio raíz
            prefix = '../' * depth
            
            # 1. Corregir rutas a archivos index
            content = re.sub(r'href="(index\.html)"', f'href="{prefix}\\1"', content)
            content = re.sub(r'href="(index2\.html)"', f'href="{prefix}\\1"', content)
            content = re.sub(r'href="(index3\.html)"', f'href="{prefix}\\1"', content)
            content = re.sub(r'href="(index4\.html)"', f'href="{prefix}\\1"', content)
            
            # 2. Corregir rutas a carpetas organizacionales (que deben ir desde la raíz)
            content = re.sub(r'href="(apps/[^"]*)"', f'href="{prefix}\\1"', content)
            content = re.sub(r'href="(charts/[^"]*)"', f'href="{prefix}\\1"', content)
            content = re.sub(r'href="(forms/[^"]*)"', f'href="{prefix}\\1"', content)
            content = re.sub(r'href="(icons/[^"]*)"', f'href="{prefix}\\1"', content)
            content = re.sub(r'href="(maps/[^"]*)"', f'href="{prefix}\\1"', content)
            content = re.sub(r'href="(pages/[^"]*)"', f'href="{prefix}\\1"', content)
            content = re.sub(r'href="(tables/[^"]*)"', f'href="{prefix}\\1"', content)
            content = re.sub(r'href="(ui/[^"]*)"', f'href="{prefix}\\1"', content)
            content = re.sub(r'href="(widgets/[^"]*)"', f'href="{prefix}\\1"', content)
            
            # 3. Evitar dobles prefijos (limpiar si ya existen)
            content = re.sub(f'{re.escape(prefix)}{re.escape(prefix)}', prefix, content)
            
        else:  # Archivo está en la raíz
            # Los archivos en la raíz deben apuntar directamente a las carpetas
            # No necesitan prefijo, las rutas ya están correctas
            pass
        
        # Solo escribir si hay cambios
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error procesando {file_path}: {e}")
        return False

def find_html_files(directory):
    """Encuentra todos los archivos HTML en el directorio y subdirectorios"""
    html_files = []
    for root, dirs, files in os.walk(directory):
        # Excluir .git
        if '.git' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def main():
    base_dir = '/var/www/html/niche_horizontal'
    html_files = find_html_files(base_dir)
    
    updated_files = 0
    
    print("🔗 CORRIGIENDO RUTAS DE NAVEGACIÓN")
    print("==================================")
    print()
    
    for file_path in html_files:
        if fix_navigation_paths(file_path):
            relative_path = file_path.replace(base_dir + '/', '')
            print(f"✅ {relative_path}")
            updated_files += 1
    
    print()
    print(f"📊 RESUMEN:")
    print(f"  📁 {len(html_files)} archivos HTML procesados")
    print(f"  ✅ {updated_files} archivos corregidos")

if __name__ == "__main__":
    main()
