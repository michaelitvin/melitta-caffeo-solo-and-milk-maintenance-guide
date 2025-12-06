#!/usr/bin/env python3
"""Extract PDF content using docling to markdown with referenced images."""

from pathlib import Path
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import PdfFormatOption
from docling_core.types.doc import ImageRefMode

# Paths
PDF_PATH = Path("MelittaCaffeoSoloAndMilkManual.pdf")
OUTPUT_DIR = Path("extracted")

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Configure pipeline for image extraction
    pipeline_options = PdfPipelineOptions()
    pipeline_options.images_scale = 2.0  # Higher resolution images
    pipeline_options.generate_picture_images = True

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    print(f"Converting {PDF_PATH}...")
    result = converter.convert(PDF_PATH)
    doc = result.document

    # Save images first and build a mapping
    images_dir = OUTPUT_DIR / "images"
    images_dir.mkdir(exist_ok=True)

    image_map = {}
    for picture_ix, picture in enumerate(doc.pictures):
        if picture.image:
            image_filename = f"picture_{picture_ix}.png"
            image_path = images_dir / image_filename
            picture.image.pil_image.save(image_path, "PNG")
            # Map picture self_ref to image path
            if hasattr(picture, 'self_ref') and picture.self_ref:
                image_map[picture.self_ref] = f"images/{image_filename}"
            print(f"Saved image: {image_path}")

    # Export markdown with referenced images
    content_md = doc.export_to_markdown(image_mode=ImageRefMode.REFERENCED)

    # Replace image placeholders with actual image references
    # docling uses <!-- image --> as placeholder, we need to inject proper markdown images
    lines = content_md.split('\n')
    new_lines = []
    image_counter = 0

    for line in lines:
        if line.strip() == '<!-- image -->':
            if image_counter < len(doc.pictures):
                image_path = f"images/picture_{image_counter}.png"
                new_lines.append(f"![Image {image_counter}]({image_path})")
                image_counter += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    content_md = '\n'.join(new_lines)

    # Save markdown
    md_path = OUTPUT_DIR / "manual.md"
    md_path.write_text(content_md)
    print(f"Markdown saved to {md_path}")

    # Also save page images if available
    for page_no, page in doc.pages.items():
        if page.image:
            page_path = images_dir / f"page_{page_no}.png"
            page.image.pil_image.save(page_path, "PNG")
            print(f"Saved page image: {page_path}")

    print(f"\nExtraction complete! Files saved to {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
