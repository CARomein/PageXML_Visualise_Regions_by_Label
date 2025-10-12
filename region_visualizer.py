import os
import re
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
import argparse
from collections import Counter, defaultdict
import math

# Default colour scheme for labels
DEFAULT_COLOURS = {
    'prop_request_rekest': (255, 200, 200),
    'attendance_list': (200, 255, 200),
    'prop_decission': (200, 200, 255),
    'marginalia': (255, 255, 200),
    'catch_word': (255, 220, 180),
    'header': (220, 180, 255),
    'page-number': (180, 220, 255),
    'signature': (255, 180, 220),
    'prop_missive': (255, 210, 210),
    'prop_plakkaat': (210, 255, 210),
    'prop_remonstrantie': (210, 210, 255),
    'prop_klacht': (255, 255, 210),
    'prop_instructie': (255, 230, 200),
    'prop_goetgevonden': (230, 200, 255),
    'TOC-entry': (200, 255, 255),
    'paragraph': (240, 240, 240),
    'heading': (200, 200, 200),
    'date': (255, 200, 255),
}

# Dark theme colours
DARK_THEME_COLOURS = {
    'prop_request_rekest': (100, 0, 0),
    'attendance_list': (0, 100, 0),
    'prop_decission': (0, 0, 100),
    'marginalia': (100, 100, 0),
    'catch_word': (100, 50, 0),
    'header': (50, 0, 100),
    'page-number': (0, 50, 100),
    'signature': (100, 0, 50),
    'prop_missive': (120, 30, 30),
    'prop_plakkaat': (30, 120, 30),
    'prop_remonstrantie': (30, 30, 120),
    'prop_klacht': (120, 120, 30),
    'prop_instructie': (120, 70, 30),
    'prop_goetgevonden': (70, 30, 120),
    'TOC-entry': (30, 120, 120),
    'paragraph': (80, 80, 80),
    'heading': (60, 60, 60),
    'date': (120, 30, 120),
}


def load_colour_config(config_file: Optional[str]) -> Dict[str, Tuple[int, int, int]]:
    """Load colour configuration from JSON file."""
    if config_file and os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return {label: tuple(colour) for label, colour in config.items()}
    return DEFAULT_COLOURS


def extract_structure_type(custom_str: str) -> Optional[str]:
    """Extract structure type from custom attribute."""
    if not custom_str:
        return None
    
    structure_match = re.search(r'structure\s*\{[^}]*type:([^;}]+)', custom_str)
    if structure_match:
        return structure_match.group(1).strip()
    
    return None


def parse_pagexml(xml_file: str) -> Tuple[List[Dict], int, int, str]:
    """
    Parse PageXML file and extract region information.
    
    Returns:
        Tuple of (regions_list, image_width, image_height, page_name)
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    ns = {'ns': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'}
    
    # Get page dimensions
    page = root.find('.//ns:Page', ns)
    image_width = int(page.attrib.get('imageWidth', 2000))
    image_height = int(page.attrib.get('imageHeight', 3000))
    
    # Get page name
    page_name = os.path.splitext(os.path.basename(xml_file))[0]
    
    # Extract all text regions
    regions = []
    text_regions = root.findall('.//ns:TextRegion', ns)
    
    for region in text_regions:
        region_id = region.attrib.get('id', '')
        custom_str = region.attrib.get('custom', '')
        
        # Extract structure type
        label = extract_structure_type(custom_str)
        
        # Extract coordinates
        coords_elem = region.find('ns:Coords', ns)
        if coords_elem is not None:
            points_str = coords_elem.attrib.get('points', '')
            points = [tuple(map(int, point.split(','))) for point in points_str.split()]
            
            regions.append({
                'id': region_id,
                'label': label,
                'points': points
            })
    
    return regions, image_width, image_height, page_name


def generate_colour_scheme(labels: List[str], dark_theme: bool = False) -> Dict[str, Tuple[int, int, int]]:
    """Generate a colour scheme for all labels found in the dataset."""
    base_colours = DARK_THEME_COLOURS if dark_theme else DEFAULT_COLOURS
    colour_scheme = {}
    
    for label in labels:
        if label in base_colours:
            colour_scheme[label] = base_colours[label]
        else:
            # Generate a pseudo-random colour based on label name
            hash_value = hash(label)
            if dark_theme:
                r = (hash_value % 100) + 50
                g = ((hash_value >> 8) % 100) + 50
                b = ((hash_value >> 16) % 100) + 50
            else:
                r = (hash_value % 100) + 150
                g = ((hash_value >> 8) % 100) + 150
                b = ((hash_value >> 16) % 100) + 150
            colour_scheme[label] = (r, g, b)
    
    return colour_scheme


def draw_page_schematic(
    regions: List[Dict],
    page_width: int,
    page_height: int,
    page_name: str,
    colour_scheme: Dict[str, Tuple[int, int, int]],
    dark_theme: bool = False,
    scale: float = 0.15
) -> Image.Image:
    """
    Draw a schematic representation of a page with coloured regions.
    """
    # Calculate scaled dimensions
    scaled_width = int(page_width * scale)
    scaled_height = int(page_height * scale)
    
    # Create image
    bg_colour = (0, 0, 0) if dark_theme else (255, 255, 255)
    outline_colour = (255, 255, 255) if dark_theme else (0, 0, 0)
    
    img = Image.new('RGB', (scaled_width, scaled_height), bg_colour)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Draw border around page
    draw.rectangle([(0, 0), (scaled_width-1, scaled_height-1)], 
                   outline=outline_colour, width=2)
    
    # Draw each region
    for region in regions:
        points = region['points']
        label = region['label']
        
        if len(points) < 3:
            continue
        
        # Scale coordinates
        scaled_points = [(int(x * scale), int(y * scale)) for x, y in points]
        
        # Get colour for this label
        if label and label in colour_scheme:
            fill_colour = colour_scheme[label] + (180,)  # Add alpha
            draw.polygon(scaled_points, fill=fill_colour, outline=outline_colour, width=1)
        else:
            # Unlabelled regions: only draw outline
            draw.polygon(scaled_points, fill=None, outline=outline_colour, width=1)
    
    return img


def create_overview_grid(
    page_images: List[Tuple[Image.Image, str]],
    colour_scheme: Dict[str, Tuple[int, int, int]],
    label_counts: Dict[str, int],
    archief_name: str,
    dark_theme: bool = False,
    columns: int = 2
) -> Image.Image:
    """
    Create a grid overview of all pages with a legend.
    """
    if not page_images:
        return None
    
    # Calculate grid dimensions
    n_pages = len(page_images)
    rows = math.ceil(n_pages / columns)
    
    # Get maximum dimensions for uniform grid
    max_width = max(img.width for img, _ in page_images)
    max_height = max(img.height for img, _ in page_images)
    
    # Add padding
    padding = 20
    label_height = 30
    title_height = 60
    cell_width = max_width + padding * 2
    cell_height = max_height + padding * 2 + label_height
    
    # Create legend
    legend_height = max(400, len(colour_scheme) * 30 + 100)
    
    # Calculate total dimensions
    grid_width = columns * cell_width
    grid_height = rows * cell_height
    total_height = grid_height + legend_height + title_height
    
    # Create canvas
    bg_colour = (0, 0, 0) if dark_theme else (255, 255, 255)
    text_colour = (255, 255, 255) if dark_theme else (0, 0, 0)
    
    canvas = Image.new('RGB', (grid_width, total_height), bg_colour)
    draw = ImageDraw.Draw(canvas)
    
    # Load font
    try:
        font = ImageFont.truetype("arial.ttf", 14)
        title_font = ImageFont.truetype("arial.ttf", 28)
        legend_title_font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
        legend_title_font = ImageFont.load_default()
    
    # Draw main title
    title_text = f"Collection Overview: {archief_name} ({n_pages} pages)"
    draw.text((padding, padding), title_text, fill=text_colour, font=title_font)
    
    # Place pages in grid
    for idx, (img, page_id) in enumerate(page_images):
        row = idx // columns
        col = idx % columns
        
        x = col * cell_width + padding
        y = row * cell_height + padding + title_height
        
        # Paste image
        canvas.paste(img, (x, y))
        
        # Draw label
        label_y = y + img.height + 5
        draw.text((x, label_y), page_id, fill=text_colour, font=font)
    
    # Draw legend at bottom
    legend_y = grid_height + title_height + 20
    draw.text((padding, legend_y), "Label Colour Scheme", fill=text_colour, font=legend_title_font)
    
    legend_y += 40
    box_size = 20
    
    # Sort labels by count
    sorted_labels = sorted(colour_scheme.items(), key=lambda x: label_counts.get(x[0], 0), reverse=True)
    
    for label, colour in sorted_labels:
        count = label_counts.get(label, 0)
        
        if count == 0:  # Skip labels not present in this archief
            continue
        
        # Draw colour box
        draw.rectangle([(padding, legend_y), (padding + box_size, legend_y + box_size)],
                      fill=colour, outline=text_colour, width=1)
        
        # Draw label text
        text = f"{label}: {count} regions"
        draw.text((padding + box_size + 10, legend_y + 2), text, fill=text_colour, font=font)
        
        legend_y += 28
    
    # Add unlabelled count
    if 'unlabeled' in label_counts and label_counts['unlabeled'] > 0:
        legend_y += 10
        draw.text((padding, legend_y), 
                 f"Unlabelled: {label_counts['unlabeled']} regions", 
                 fill=text_colour, font=font)
    
    return canvas


def process_directory(
    input_dir: str,
    output_dir: str,
    colour_config: Optional[str] = None,
    dark_theme: bool = False,
    scale: float = 0.15,
    columns: int = 2
) -> None:
    """
    Process all PageXML files and create overview images per archief.
    
    Args:
        input_dir: Directory containing PageXML files
        output_dir: Directory for output images (one per archief)
        colour_config: Optional path to colour configuration JSON
        dark_theme: Whether to use dark theme
        scale: Scale factor for individual pages
        columns: Number of columns in grid layout
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Collect all XML files grouped by archief
    archief_files = defaultdict(list)
    
    for archief_dir in os.listdir(input_dir):
        archief_path = os.path.join(input_dir, archief_dir)
        if not os.path.isdir(archief_path):
            continue
        
        page_dir = os.path.join(archief_path, 'page')
        if not os.path.isdir(page_dir):
            continue
        
        for page_file in os.listdir(page_dir):
            if page_file.endswith('.xml'):
                xml_path = os.path.join(page_dir, page_file)
                archief_files[archief_dir].append(xml_path)
    
    if not archief_files:
        print(f"No XML files found in {input_dir}")
        return
    
    total_files = sum(len(files) for files in archief_files.values())
    print(f"Found {total_files} PageXML files in {len(archief_files)} archief directories")
    
    # First pass: collect all unique labels across entire collection
    print("\nScanning for labels across entire collection...")
    all_labels = set()
    
    for archief_dir, xml_files in archief_files.items():
        for xml_file in xml_files:
            try:
                regions, _, _, _ = parse_pagexml(xml_file)
                for region in regions:
                    if region['label']:
                        all_labels.add(region['label'])
            except Exception as e:
                print(f"Error parsing {xml_file}: {e}")
    
    print(f"Found {len(all_labels)} unique labels: {', '.join(sorted(all_labels))}")
    
    # Load or generate colour scheme (consistent across all archiefs)
    if colour_config:
        colour_scheme = load_colour_config(colour_config)
    else:
        colour_scheme = generate_colour_scheme(list(all_labels), dark_theme)
    
    # Process each archief separately
    print(f"\nProcessing {len(archief_files)} archief directories...")
    
    for archief_idx, (archief_dir, xml_files) in enumerate(sorted(archief_files.items())):
        print(f"\n[{archief_idx + 1}/{len(archief_files)}] Processing archief: {archief_dir} ({len(xml_files)} pages)")
        
        # Sort files for consistent ordering
        xml_files.sort()
        
        # Count labels in this archief
        archief_label_counts = Counter()
        archief_unlabeled = 0
        
        # Create page schematics for this archief
        page_images = []
        
        for idx, xml_file in enumerate(xml_files):
            try:
                regions, page_width, page_height, page_name = parse_pagexml(xml_file)
                
                # Count labels
                for region in regions:
                    if region['label']:
                        archief_label_counts[region['label']] += 1
                    else:
                        archief_unlabeled += 1
                
                # Create schematic
                img = draw_page_schematic(
                    regions,
                    page_width,
                    page_height,
                    page_name,
                    colour_scheme,
                    dark_theme,
                    scale
                )
                
                page_images.append((img, page_name))
                
                if (idx + 1) % 50 == 0 or (idx + 1) == len(xml_files):
                    print(f"  Processed {idx + 1}/{len(xml_files)} pages...", end='\r')
            
            except Exception as e:
                print(f"\n  Error processing {xml_file}: {e}")
        
        print(f"\n  Generated {len(page_images)} page schematics")
        
        archief_label_counts['unlabeled'] = archief_unlabeled
        
        # Create overview grid for this archief
        print(f"  Creating overview grid...")
        overview = create_overview_grid(
            page_images,
            colour_scheme,
            archief_label_counts,
            archief_dir,
            dark_theme,
            columns
        )
        
        if overview:
            # Save overview
            output_filename = f"overview_{archief_dir}.png"
            output_path = os.path.join(output_dir, output_filename)
            overview.save(output_path, quality=95)
            print(f"  Saved: {output_filename} ({overview.width} x {overview.height} pixels)")
        else:
            print(f"  Error: Could not create overview for {archief_dir}")
    
    print(f"\n{'='*60}")
    print(f"Processing complete!")
    print(f"Created {len(archief_files)} overview images in: {output_dir}")
    print(f"Total pages processed: {total_files}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create schematic overviews of PageXML regions per archief'
    )
    parser.add_argument('input_dir', type=str,
                       help='Input directory containing PageXML files')
    parser.add_argument('output_dir', type=str,
                       help='Output directory for overview images')
    parser.add_argument('--colour-config', type=str, default=None,
                       help='JSON file with custom colour configuration')
    parser.add_argument('--dark-theme', action='store_true',
                       help='Use dark theme (black background, white outlines)')
    parser.add_argument('--scale', type=float, default=0.15,
                       help='Scale factor for pages (default: 0.15)')
    parser.add_argument('--columns', type=int, default=2,
                       help='Number of columns in grid (default: 2)')
    
    args = parser.parse_args()
    
    process_directory(
        args.input_dir,
        args.output_dir,
        args.colour_config,
        args.dark_theme,
        args.scale,
        args.columns
    )
