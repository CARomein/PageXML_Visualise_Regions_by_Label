# Region Visualisation Tool Suite

A collection of Python tools for creating schematic overviews of PageXML text region annotations. These tools generate single overview images showing all pages from a collection, with regions colour-coded by their structural label. The suite includes three complementary scripts for different analytical purposes: basic region visualisation, textline crossing detection, and duplicate sentence identification.

## Purpose

During annotation projects with historical documents, it is essential to monitor both progress and quality across the entire collection. These tools address different analytical needs:

- **Basic visualisation**: Monitor annotation progress and structural patterns
- **Crossing detection**: Identify layout recognition issues where textlines cross region boundaries
- **Duplicate detection**: Find repeated sentences in transcriptions that may indicate OCR or transcription errors

All tools create schematic representations using only the coordinates from PageXML files, making them extremely efficient compared to image-based approaches. All pages are combined into single overview images, making it easy to assess entire collections at a glance.

## The Three Scripts

### 1. region_visualizer.py (Prefix: v)

The **basic visualisation tool** creates schematic overviews with colour-coded regions.

**Use cases:**
- Monitor annotation progress across collections
- Assess distribution of document types
- Identify pages requiring annotation
- Verify structural labelling patterns

**Output example:** `overview_v_20251018_143022_0018.png`

**Visual markers:** Colour-coded regions only

### 2. region_visualizer_crossings.py (Prefix: vc)

The **crossing detection tool** identifies textlines that physically extend into regions other than those to which they are assigned.

**Use cases:**
- Detect layout recognition errors
- Identify problematic textline assignments
- Find overlapping regions requiring correction
- Quality control for automated layout analysis

**Output example:** `overview_vc_20251018_143022_0018.png`

**Visual markers:** Colour-coded regions + red crosses (✗) at crossing points

**What constitutes a crossing:**
A crossing occurs when a textline assigned to Region A has coordinate points that fall within the boundaries of Region B. This indicates a mismatch between the logical assignment and the physical location of the textline.

### 3. visualize_double_lines.py (Prefix: vd)

The **duplicate detection tool** identifies repeated sentences in the transcription.

**Use cases:**
- Detect OCR errors causing duplicate output
- Find transcription mistakes where text was entered twice
- Identify pages where textlines were incorrectly duplicated
- Quality control for transcription accuracy

**Output example:** `overview_vd_20251018_143022_0018.png`

**Visual markers:** Colour-coded regions + purple asterisks (*) at duplicate locations

**How duplicates are detected:**
The tool normalises all transcribed text (lowercasing, removing punctuation, normalising whitespace) and identifies any sentences appearing more than once within a page. The second and subsequent occurrences are marked as duplicates. Very short texts (fewer than 5 characters) are ignored to avoid false positives.

## Common Features

All three scripts share these characteristics:

- **Efficient processing**: Uses only PageXML coordinates, no image loading required
- **Single overview per archief**: All pages combined in one grid layout
- **Automatic label detection**: Identifies all structure types present in the collection
- **Configurable colours**: Define custom colours for each label type via JSON
- **Theme support**: Light theme (white background) or dark theme (black background)
- **Integrated legend**: Colour scheme and region counts displayed at the bottom
- **Automatic output management**: Creates timestamped files in a standardised `visualizer` folder
- **Adjustable scale**: Control the size of individual pages in the overview
- **Fast processing**: Processes hundreds of pages in seconds

## Key Advantages

Unlike image-based visualisation approaches that require loading, processing, and saving large image files for each page, these tools simply draw schematic representations based on coordinates from the PageXML. This makes them:

- **Much faster**: Process entire collections in seconds rather than minutes
- **More efficient**: Lower memory usage and disk I/O
- **More practical**: Single overview file per archief instead of hundreds of separate images
- **Energy-conscious**: Significantly lower computational requirements

## Requirements

- Python 3.7 or higher
- Pillow (PIL) for drawing

Install dependencies:
```bash
pip install Pillow
```

## Installation

Download the scripts or place them in your working directory:
- `region_visualizer.py`
- `region_visualizer_crossings.py`
- `visualize_double_lines.py`

## PageXML Folder Structure

The tools expect Transkribus-style export structures:

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

Note: No image files are required. The tools use only the PageXML files with their coordinate information.

## Usage

All three scripts follow the same basic usage pattern. They automatically create a `visualizer` folder in the script's directory and generate timestamped output files.

### Basic Region Visualisation

Create standard overviews with colour-coded regions:

```bash
python region_visualizer.py <input_dir>
```

Example:
```bash
python region_visualizer.py pagexml_v3_with_continuations_positions
```

This creates files like `overview_v_20251018_143022_0018.png` in the `visualizer` folder.

### Crossing Detection

Detect and visualise textline crossings:

```bash
python region_visualizer_crossings.py <input_dir>
```

Example:
```bash
python region_visualizer_crossings.py pagexml_v3_with_continuations_positions
```

This creates files like `overview_vc_20251018_143022_0018.png` showing red crosses at crossing points.

### Duplicate Sentence Detection

Identify repeated sentences in transcriptions:

```bash
python visualize_double_lines.py <input_dir>
```

Example:
```bash
python visualize_double_lines.py pagexml_v3_with_continuations_positions
```

This creates files like `overview_vd_20251018_143022_0018.png` showing purple asterisks at duplicate locations.

### Command-Line Options

All three scripts support the same optional arguments:

**--colour-config**: Specify a JSON file with custom colour definitions

```bash
python region_visualizer.py <input_dir> --colour-config my_colours.json
```

**--dark-theme**: Use dark theme with black background and white outlines

```bash
python region_visualizer.py <input_dir> --dark-theme
```

**--scale**: Adjust the scale of individual pages (default: 0.15 = 15% of original size)

```bash
python region_visualizer.py <input_dir> --scale 0.2
```

**--columns**: Set the number of columns in the grid layout (default: 2)

```bash
python region_visualizer.py <input_dir> --columns 4
```

### Complete Examples

```bash
# Basic visualisation with custom colours and dark theme
python region_visualizer.py pagexml_collection --colour-config colours.json --dark-theme

# Crossing detection with larger scale
python region_visualizer_crossings.py pagexml_collection --scale 0.2

# Duplicate detection with 4 columns
python visualize_double_lines.py pagexml_collection --columns 4
```

## Output Structure

All scripts create output in a `visualizer` folder located in the same directory as the script:

```
your_project/
├── region_visualizer.py
├── region_visualizer_crossings.py
├── visualize_double_lines.py
└── visualizer/
    ├── overview_v_20251018_143022_0018.png
    ├── overview_v_20251018_143022_0019.png
    ├── overview_vc_20251018_150315_0018.png
    ├── overview_vc_20251018_150315_0019.png
    ├── overview_vd_20251018_152045_0018.png
    └── overview_vd_20251018_152045_0019.png
```

### Filename Format

All output files follow this pattern:

```
overview_[prefix]_[timestamp]_[archief].png
```

Where:
- **prefix**: `v` (visualizer), `vc` (visualizer crossings), or `vd` (visualizer duplicates)
- **timestamp**: `YYYYMMDD_HHMMSS` format
- **archief**: The archief directory name

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

If no configuration file is provided, the tools use default colours:

**Light theme**:
- prop_request_rekest: Light red
- attendance_list: Light green
- prop_decission: Light blue
- marginalia: Light yellow
- catch_word: Light orange
- header: Light purple
- page-number: Light cyan
- signature: Light pink

**Dark theme**: Darker variants suitable for black backgrounds.

Labels not in the configuration receive automatically generated colours based on their name, ensuring consistency across runs.

## Output Details

### Overview Images (One per Archief)

Each tool creates separate PNG images for each archief directory, with each image containing:

- **Grid layout**: All pages arranged in a configurable grid (default: 2 columns)
- **Page schematics**: Each page shown as a scaled rectangle with exact dimensions from PageXML
- **Coloured regions**: Regions filled with semi-transparent colours based on their labels
- **Unlabelled regions**: Shown with outlines only (no fill)
- **Page identifiers**: Each page labelled with archief and page number
- **Integrated legend**: Colour scheme and region counts displayed at the bottom
- **Special markers**: 
  - Red crosses (✗) for textline crossings (vc script only)
  - Purple asterisks (*) for duplicate sentences (vd script only)

### File Size

Output file size depends on the number of pages per archief and scale factor. Typical examples per archief:

- 20-50 pages at 15% scale: ~2-5 MB per archief
- 50-100 pages at 15% scale: ~5-10 MB per archief
- 100+ pages at 15% scale: ~10-20 MB per archief

Reducing the scale factor (`--scale 0.1`) creates smaller files. Using the default 2 columns produces manageable file sizes.

## How the Scripts Work

### Common Processing Workflow

1. **Directory scanning**: Identifies all PageXML files grouped by archief directory
2. **Label discovery**: Scans all files across entire collection to identify unique label types and ensure consistent colour scheme
3. **Colour scheme generation**: Loads custom colours or generates default scheme applicable to all archiefs
4. **Per-archief processing**: For each archief directory:
   - Extracts page dimensions and region coordinates from PageXML files
   - Counts label occurrences in this archief
   - Performs script-specific analysis (crossings or duplicates)
   - Creates scaled schematic drawings with coloured regions and markers
   - Assembles pages in grid layout with title and legend
   - Saves timestamped overview image
5. **Output**: Multiple PNG files in `visualizer` folder, one per archief directory

### Script-Specific Processing

**region_visualizer.py**: Draws only region boundaries and fills

**region_visualizer_crossings.py**: Additionally:
- Extracts textline coordinates (baselines or bounding boxes)
- For each textline, checks if any coordinate points fall within regions other than the assigned region
- Uses point-in-polygon algorithm and line segment intersection detection
- Marks crossing points with red crosses

**visualize_double_lines.py**: Additionally:
- Extracts transcribed text from each textline
- Normalises text (lowercasing, removing punctuation, whitespace normalisation)
- Identifies sentences appearing more than once on the same page
- Marks duplicate locations with purple asterisks

### Efficiency

All tools achieve high efficiency by:
- Processing only XML text files (no image loading)
- Drawing simple vector graphics (no complex image manipulation)
- Creating timestamped output files automatically
- Using minimal memory (processes pages sequentially)

## Use Cases

### Progress Monitoring (all scripts)

Generate overviews at regular intervals to track annotation progress. The visual contrast between coloured (labelled) and unfilled (unlabelled) regions immediately reveals which documents require attention.

### Quality Control

**Basic visualisation**: Examine the overview to identify patterns or anomalies in structural labelling.

**Crossing detection**: Identify layout recognition errors such as:
- Textlines incorrectly assigned to neighbouring regions
- Reading order problems
- Overlapping region boundaries
- Columns or margins incorrectly segmented

**Duplicate detection**: Find transcription quality issues such as:
- OCR errors producing duplicate output
- Manual transcription errors
- Incorrect textline duplication during layout analysis

### Presentations (all scripts)

Include overviews in project presentations to demonstrate:
- The scale of the document collection
- The variety of document types
- The progress of annotation efforts
- Quality metrics and error rates

### Comparative Analysis (all scripts)

Generate overviews for different document collections or project stages:
- Compare label distributions across collections
- Track changes in layout patterns over time
- Identify differences between annotators or annotation phases
- Monitor error rates across different document types

### Workflow Integration

Use the three scripts in sequence for comprehensive quality assessment:

1. **Basic visualisation**: Overview of annotation progress and structural patterns
2. **Crossing detection**: Identify and correct layout recognition errors
3. **Duplicate detection**: Find and resolve transcription quality issues

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

### Cannot see small regions or markers

**Problem**: Small regions or markers (crosses, asterisks) not visible

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

### No duplicates or crossings detected

**Problem**: Script runs but reports zero issues

**Possible explanations**:
- **Crossings script**: Layout may be very clean with no crossing issues (this is good!)
- **Duplicates script**: No duplicate sentences present, or transcriptions not yet added to PageXML
- Check that PageXML files contain expected data (textlines with coordinates for crossings, transcribed text for duplicates)

## Performance

- **Processing speed**: ~100-500 pages per second
- **Memory usage**: Low (minimal, processes sequentially)
- **Output creation**: <1 second for final image assembly

Typical processing times:
- 100 pages: ~2-5 seconds
- 500 pages: ~5-10 seconds
- 1,000 pages: ~10-20 seconds

Performance is excellent because the tools only process text (XML) and draw simple vector graphics, avoiding expensive image operations.

## Limitations

- **No original images**: Shows schematic representations, not actual document scans
- **Fixed scale**: All pages scaled uniformly (though individual scale is configurable)
- **PNG format**: Output is raster image (though at configurable resolution)
- **Text visibility**: No document text visible, only region layout and markers
- **Page-level duplicate detection**: The duplicate detection script only finds duplicates within individual pages, not across pages

These limitations are intentional trade-offs for efficiency. For detailed inspection of individual pages with original images, consider complementary tools.

## Best Practices

1. **Start with basic visualisation**: Use `region_visualizer.py` first to assess overall annotation progress
2. **Run all three scripts**: Each provides different analytical perspectives on your collection
3. **Adjust scale as needed**: Use `--scale 0.1` for large collections, `--scale 0.2` for detailed inspection
4. **Choose appropriate columns**: Default is 2 for comfortable viewing; use 1 for larger pages or 3-4 for more compact overviews
5. **Create custom colours**: Define colour scheme that matches your label taxonomy
6. **Use for iterative review**: Generate new overviews after each annotation phase
7. **Document colours**: Keep colour configuration under version control
8. **Combine with statistics**: Use alongside quantitative analysis tools for comprehensive quality assessment
9. **Archive overviews**: Timestamped filenames allow tracking progress over time
10. **Compare timestamps**: Generate overviews before and after corrections to verify improvements

## Advanced Usage

### Batch Processing with All Three Scripts

Process a collection with all three analytical approaches:

```bash
# Basic overview
python region_visualizer.py pagexml_collection --colour-config colours.json

# Crossing detection
python region_visualizer_crossings.py pagexml_collection --colour-config colours.json

# Duplicate detection
python visualize_double_lines.py pagexml_collection --colour-config colours.json
```

### Creating Multiple Views

Generate different views of the same collection:

```bash
# Compact overview (more pages per row, smaller scale)
python region_visualizer.py data --scale 0.08 --columns 4

# Detailed overview (larger individual pages, single column)
python region_visualizer.py data --scale 0.25 --columns 1

# Dark theme version for presentations
python region_visualizer.py data --dark-theme
```

### Integration with Analysis Pipeline

Combine with other tools in automated workflow:

```bash
#!/bin/bash

# Set variables
INPUT_DIR="pagexml_collection"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_DIR="results_${TIMESTAMP}"

# Run annotation or processing
python auto_label_attendance_batch.py input output

# Generate all three visualisations
python region_visualizer.py ${INPUT_DIR}
python region_visualizer_crossings.py ${INPUT_DIR}
python visualize_double_lines.py ${INPUT_DIR}

# Generate statistics
python region_calculator_tool.py ${INPUT_DIR} --output stats.csv

# Package results
mkdir ${RESULTS_DIR}
cp stats.csv ${RESULTS_DIR}/
cp -r visualizer ${RESULTS_DIR}/

echo "Analysis complete in ${RESULTS_DIR}"
```

## Technical Details

The tools use Pillow (PIL) for drawing operations. They create RGB image canvases with dimensions calculated from the grid layout (2 columns by default × rows needed) and individual page scale factors.

For each page, coordinates are extracted from PageXML Coords elements and scaled down by the specified scale factor (default 15%). These scaled coordinates are used to draw polygons with semi-transparent fills and solid outlines.

The legend is drawn at the bottom of the canvas with colour boxes, label names, and region counts extracted during the initial scanning phase.

Label extraction uses regular expressions matching `structure\s*\{[^}]*type:([^;}]+)` in TextRegion custom attributes.

**Crossing detection** uses computational geometry algorithms:
- Point-in-polygon test (ray casting algorithm)
- Line segment intersection detection

**Duplicate detection** uses text normalisation and comparison:
- Lowercase conversion
- Punctuation removal
- Whitespace normalisation
- Hash-based duplicate identification

## Choosing the Right Script

**Use `region_visualizer.py` when you want to:**
- Get a quick overview of annotation progress
- Assess structural labelling patterns
- Monitor which pages need annotation
- Create presentation materials

**Use `region_visualizer_crossings.py` when you want to:**
- Verify layout recognition quality
- Identify textlines assigned to wrong regions
- Find overlapping or problematic region boundaries
- Prepare for correction of layout errors

**Use `visualize_double_lines.py` when you want to:**
- Check transcription quality
- Find OCR or manual transcription errors
- Identify duplicated textlines
- Verify data integrity before further processing

**Run all three scripts when:**
- Performing comprehensive quality control
- Preparing final deliverables
- Documenting project status
- Beginning a new annotation phase

## Notes

- All tools process only PageXML files; no image files required
- Original PageXML files are never modified
- Page dimensions come from imageWidth and imageHeight attributes in PageXML
- Region coordinates are scaled proportionally to fit the overview
- Output consists of multiple PNG files (one per archief), each a manageable size
- Default grid layout uses 2 columns for comfortable viewing
- All archiefs use a consistent colour scheme based on the complete collection
- Timestamps ensure multiple runs can coexist without overwriting previous results

## Licence

This project is licensed under the MIT Licence.

## Contact

- Email: c.a.romein@utwente.nl

## Acknowledgements

This Region Visualisation Tool Suite was developed within the context of the [HAICu project](https://haicu.science) on the Resoluties van de Staten van Overijssel (Resolutions of the States of Overijssel), funded by the Dutch Research Council/Nederlandse Organisatie voor Wetenschappelijk Onderzoek/Nationale Wetenschapsagenda [NWA.1518.22.105].

Development was assisted by Claude (Anthropic) for code implementation and documentation.

## Version History

**Version 3.0** (2025): Added duplicate sentence detection tool (`visualize_double_lines.py`); implemented automatic output management with timestamped files in `visualizer` folder; unified command-line interface across all three scripts.

**Version 2.0** (2025): Added crossing detection tool (`region_visualizer_crossings.py`); efficient schematic overview approach using only PageXML coordinates; single overview image per archief; integrated legend; configurable grid layout.

**Version 1.0** (2025): Initial release with basic visualisation (superseded by v2.0 and v3.0).
