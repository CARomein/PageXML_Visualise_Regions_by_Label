# Region Visualisation Tool

A Python tool for creating schematic overviews of PageXML text region annotations. This tool generates a single overview image showing all pages from a collection, with regions colour-coded by their structural label. This approach is efficient, fast, and provides an excellent bird's-eye view of annotation progress across entire document collections.

## Purpose

During annotation projects with historical documents, it is essential to monitor both progress and quality across the entire collection. This tool addresses these needs by creating a single comprehensive overview that shows:

- The spatial layout of all text regions on every page
- Which regions have been labelled with structural types
- Which regions still require annotation
- The distribution of different document types across the collection
- Potential layout recognition issues (overlapping regions, missing regions)

The tool creates schematic representations using only the coordinates from PageXML files, making it extremely efficient compared to image-based approaches. All pages are combined into a single overview image, making it easy to assess the entire collection at a glance.

## Features

- **Efficient processing**: Uses only PageXML coordinates, no image loading required
- **Single overview**: All pages combined in one grid layout
- **Automatic label detection**: Identifies all structure types present in the collection
- **Configurable colours**: Define custom colours for each label type via JSON
- **Theme support**: Light theme (white background) or dark theme (black background)
- **Integrated legend**: Colour scheme and region counts displayed at the bottom

Output filenames follow the pattern: `overview_[archief_name].png` (e.g., `overview_0018.png`, `overview_0019.png`)
- **Adjustable scale**: Control the size of individual pages in the overview
- **Fast processing**: Processes hundreds of pages in seconds

## Key Advantage

Unlike image-based visualisation approaches that require loading, processing, and saving large image files for each page, this tool simply draws schematic representations based on coordinates from the PageXML. This makes it:

- **Much faster**: Processes entire collections in seconds rather than minutes
- **More efficient**: Lower memory usage and disk I/O
- **More practical**: Single overview file instead of hundreds of separate images
- **Energy-conscious**: Significantly lower computational requirements

## Requirements

- Python 3.7 or higher
- Pillow (PIL) for drawing

Install dependencies:
```bash
pip install Pillow
```

## Installation

Download the script or place `visualise_regions_by_label.py` in your working directory.

## PageXML Folder Structure

The tool expects Transkribus-style export structures:

```
pagexml_collection/
├── 0018/
│   └── page/
│       ├── 0001.xml
│       ├── 0002.xml
│       └── 0003.xml
├── 0019/
│   └── page/
│       ├── 0001.xml
│       └── 0002.xml
└── 0020/
    └── page/
        └── ...
```

Note: No image files are required. The tool uses only the PageXML files with their coordinate information.

## Usage

### Basic Usage

Create an overview of all pages in a collection:

```bash
python visualise_regions_by_label.py <input_dir> <output_dir>
```

Example:
```bash
python visualise_regions_by_label.py pagexml_v3_with_continuations_positions visualisations
```

This creates separate PNG files in the `visualisations` directory, one for each archief, showing all pages in that archief arranged in a grid layout with regions colour-coded by label.

### Command-Line Options

**--colour-config**: Specify a JSON file with custom colour definitions

```bash
python visualise_regions_by_label.py <input_dir> <output_file> --colour-config my_colours.json
```

**--dark-theme**: Use dark theme with black background and white outlines

```bash
python visualise_regions_by_label.py <input_dir> <output_file> --dark-theme
```

**--scale**: Adjust the scale of individual pages (default: 0.15 = 15% of original size)

```bash
python visualise_regions_by_label.py <input_dir> <output_file> --scale 0.2
```

**--columns**: Set the number of columns in the grid layout (default: 4)

```bash
python visualise_regions_by_label.py <input_dir> <output_file> --columns 6
```

### Complete Example

```bash
python visualise_regions_by_label.py pagexml_v3_with_continuations_positions visualisations --colour-config custom_colours.json --dark-theme
```

## Colour Configuration

Define custom colours for each label type using a JSON file.

### Format

Create a JSON file (e.g., `custom_colours.json`) with RGB colour values:

```json
{
  "prop_request_rekest": [255, 200, 200],
  "attendance_list": [200, 255, 200],
  "resolution": [200, 200, 255],
  "marginalia": [255, 255, 200],
  "catch_word": [255, 220, 180],
  "header": [220, 180, 255],
  "footer": [180, 220, 255],
  "signature": [255, 180, 220]
}
```

### Default Colours

If no configuration file is provided, the tool uses default colours:

**Light theme**:
- prop_request_rekest: Light red
- attendance_list: Light green
- resolution: Light blue
- marginalia: Light yellow
- catch_word: Light orange
- header: Light purple
- footer: Light cyan
- signature: Light pink

**Dark theme**: Darker variants suitable for black backgrounds.

Labels not in the configuration receive automatically generated colours based on their name, ensuring consistency across runs.

## Output

### Overview Images (One per Archief)

The tool creates separate PNG images for each archief directory, with each image containing:

- **Grid layout**: All pages arranged in a configurable grid
- **Page schematics**: Each page shown as a scaled rectangle with exact dimensions from PageXML
- **Coloured regions**: Regions filled with semi-transparent colours based on their labels
- **Unlabelled regions**: Shown with outlines only (no fill)
- **Page identifiers**: Each page labelled with archief and page number
- **Integrated legend**: Colour scheme and region counts displayed at the bottom

### File Size

Output file size depends on the number of pages per archief and scale factor. Typical examples per archief:

- 20-50 pages at 15% scale: ~2-5 MB per archief
- 50-100 pages at 15% scale: ~5-10 MB per archief
- 100+ pages at 15% scale: ~10-20 MB per archief

Reducing the scale factor (`--scale 0.1`) creates smaller files. Using 2 columns (default) produces manageable file sizes.

## How It Works

### Processing Workflow

1. **Directory scanning**: Identifies all PageXML files grouped by archief directory
2. **Label discovery**: Scans all files across entire collection to identify unique label types and ensure consistent colour scheme
3. **Colour scheme generation**: Loads custom colours or generates default scheme applicable to all archiefs
4. **Per-archief processing**: For each archief directory:
   - Extracts page dimensions and region coordinates from PageXML files
   - Counts label occurrences in this archief
   - Creates scaled schematic drawings with coloured regions
   - Assembles pages in grid layout with title and legend
   - Saves separate overview image
5. **Output**: Multiple PNG files, one per archief directory

### Efficiency

The tool achieves high efficiency by:
- Processing only XML text files (no image loading)
- Drawing simple vector graphics (no complex image manipulation)
- Creating a single output file (no file I/O overhead)
- Using minimal memory (processes pages sequentially)

## Use Cases

### Progress Monitoring

Generate an overview at regular intervals to track annotation progress. The visual contrast between coloured (labelled) and unfilled (unlabelled) regions immediately reveals which documents require attention.

### Quality Control

Examine the overview to identify patterns or anomalies:
- Are marginalia consistently identified at page edges?
- Do headers appear at the top of pages?
- Are there unexpected label distributions?

### Presentations

Include the overview in project presentations to demonstrate:
- The scale of the document collection
- The variety of document types
- The progress of annotation efforts

### Comparative Analysis

Generate overviews for different document collections or project stages:
- Compare label distributions across collections
- Track changes in layout patterns over time
- Identify differences between annotators or annotation phases

### Layout Verification

Quickly identify potential layout recognition issues:
- Missing regions (empty pages in the overview)
- Overlapping regions (visible in the schematic)
- Unusual region shapes or sizes

## Troubleshooting

### No XML files found

**Problem**: "Found 0 XML files"

**Solutions**:
- Verify folder structure matches `[archief]/page/*.xml` pattern
- Check file extensions are `.xml` (lowercase)
- Ensure correct root directory is specified

### Output file too large

**Problem**: PNG file is very large

**Solutions**:
- Reduce scale factor: `--scale 0.1` instead of default 0.15
- Keep default 2 columns or reduce to 1: `--columns 1`
- Process subset of collection for initial testing
- Consider splitting collection into multiple overview images

### Cannot see small regions

**Problem**: Small regions not visible in overview

**Solutions**:
- Increase scale factor: `--scale 0.2` or `--scale 0.25`
- Keep default 2 columns or use 1 column: `--columns 1` for larger individual pages
- For detailed inspection, process smaller batches with larger scale

### Colours difficult to distinguish

**Problem**: Similar colours for different labels

**Solutions**:
- Create custom colour configuration with high-contrast colours
- Try dark theme if light theme is unclear (or vice versa)
- Ensure sufficient difference between RGB values for adjacent labels

### Memory errors

**Problem**: Out of memory when processing large collection

**Solutions**:
- Reduce scale factor to decrease memory usage
- Process collection in batches
- Close other memory-intensive applications

## Performance

- **Processing speed**: ~100-500 pages per second
- **Memory usage**: Low (minimal, processes sequentially)
- **Output creation**: <1 second for final image assembly

Typical processing times:
- 100 pages: ~2-5 seconds
- 500 pages: ~5-10 seconds
- 1,000 pages: ~10-20 seconds

Performance is excellent because the tool only processes text (XML) and draws simple vector graphics, avoiding expensive image operations.

## Limitations

- **No original images**: Shows schematic representations, not actual document scans
- **Fixed scale**: All pages scaled uniformly (though individual scale is configurable)
- **Single output**: Creates one overview file, not individual page images
- **PNG format**: Output is raster image (though at configurable resolution)
- **Text visibility**: No document text visible, only region layout

These limitations are intentional trade-offs for efficiency. For detailed inspection of individual pages with original images, consider complementary tools.

## Best Practices

1. **Start with default settings**: Generate overview with defaults first to assess results
2. **Adjust scale as needed**: Use `--scale 0.1` for large collections, `--scale 0.2` for smaller ones
3. **Choose appropriate columns**: Default is 2 for comfortable viewing; use 1 for even larger pages or 3-4 for more compact overviews
4. **Create custom colours**: Define colour scheme that matches your label taxonomy
5. **Use for iterative review**: Generate new overview after each annotation phase
6. **Document colours**: Keep colour configuration under version control
7. **Combine with statistics**: Use alongside region calculator tool for comprehensive analysis
8. **Archive overviews**: Save overview images with timestamps for progress documentation

## Advanced Usage

### Batch Processing Different Collections

Process multiple collections with consistent settings:

```bash
for collection in collection1 collection2 collection3; do
    python visualise_regions_by_label.py $collection ${collection}_output --colour-config colours.json
done
```

### Creating Multiple Views

Generate different views of the same collection:

```bash
# Compact overview (more pages per row, smaller scale)
python visualise_regions_by_label.py data output_compact --scale 0.08 --columns 4

# Detailed overview (larger individual pages, single column)
python visualise_regions_by_label.py data output_detailed --scale 0.25 --columns 1

# Dark theme version
python visualise_regions_by_label.py data output_dark --dark-theme
```

### Integration with Analysis Pipeline

Combine with other tools in automated workflow:

```bash
# Run annotation
python auto_label_attendance_batch.py input output

# Generate statistics
python region_calculator_tool.py output --output stats.csv

# Create visualisations
python visualise_regions_by_label.py output visualisations

# Package results
mkdir results_$(date +%Y%m%d)
mv stats.csv results_$(date +%Y%m%d)/
mv visualisations results_$(date +%Y%m%d)/
```

## Technical Details

The tool uses Pillow (PIL) for drawing operations. It creates an RGB image canvas with dimensions calculated from the grid layout (2 columns by default × rows needed) and individual page scale factors.

For each page, it extracts coordinates from PageXML Coords elements and scales them down by the specified scale factor (default 15%). These scaled coordinates are used to draw polygons with semi-transparent fills and solid outlines.

The legend is drawn at the bottom of the canvas with colour boxes, label names, and region counts extracted during the initial scanning phase.

Label extraction uses regular expressions matching `structure\s*\{[^}]*type:([^;}]+)` in TextRegion custom attributes.

## Notes

- The tool processes only PageXML files; no image files required
- Original PageXML files are never modified
- Page dimensions come from imageWidth and imageHeight attributes in PageXML
- Region coordinates are scaled proportionally to fit the overview
- Output consists of multiple PNG files (one per archief), each a manageable size
- Default grid layout uses 2 columns for comfortable viewing without excessive horizontal scrolling
- All archiefs use a consistent colour scheme based on the complete collection

## Licence

This project is licensed under the MIT Licence.

## Contact

- Email: c.a.romein@utwente.nl

## Acknowledgements

This Region Visualisation Tool was developed within the context of the [HAICu project](https://haicu.science) on the Resoluties van de Staten van Overijssel (Resolutions of the States of Overijssel), funded by the Dutch Research Council/Nederlandse Organisatie voor Wetenschappelijk Onderzoek/Nationale Wetenschapsagenda [NWA.1518.22.105].

Development was assisted by Claude (Anthropic) for code implementation and documentation.

## Version History

**Version 2.0** (2025): Efficient schematic overview approach using only PageXML coordinates, single overview image for entire collections, integrated legend, configurable grid layout.

**Version 1.0** (2025): Initial release with image-based visualisation (superseded by v2.0).