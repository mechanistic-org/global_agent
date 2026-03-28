import argparse
import json
from pathlib import Path
from PIL import Image

def slice_carousel(image_path: str, config_path: str, output_pdf: str, bg_color: str = "#0d1117"):
    print(f"Loading {image_path}...")
    try:
        source_img = Image.open(image_path).convert("RGBA")
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    canvas_size = (1080, 1080)
    slides = []

    for idx, slide in enumerate(config.get("slides", [])):
        print(f"Processing slide {idx+1}: {slide.get('comment', '')}")
        
        # We can either specify explicit box [x,y,w,h] or percent [x_pct, y_pct, w_pct, h_pct]
        if "x_pct" in slide:
            x = int(slide["x_pct"] * source_img.width)
            y = int(slide["y_pct"] * source_img.height)
            w = int(slide["w_pct"] * source_img.width)
            h = int(slide["h_pct"] * source_img.height)
            # Ensure boundaries are valid
            w = min(w, source_img.width - x)
            h = min(h, source_img.height - y)
        else:
            x = slide.get("x", 0)
            y = slide.get("y", 0)
            w = slide.get("w", source_img.width)
            h = slide.get("h", source_img.height)

        # Crop region
        cropped = source_img.crop((x, y, x + w, y + h))
        
        padding = slide.get("padding", 80)
        max_dim = 1080 - (padding * 2)
        
        ratio = min(max_dim / w, max_dim / h)
        new_size = (int(w * ratio), int(h * ratio))
        
        resized_crop = cropped.resize(new_size, Image.Resampling.LANCZOS)
        
        # Create a blank 1080x1080 canvas
        canvas = Image.new("RGBA", canvas_size, slide.get("bg", bg_color))
        
        # Paste resized crop in center
        paste_x = (1080 - new_size[0]) // 2
        paste_y = (1080 - new_size[1]) // 2
        canvas.paste(resized_crop, (paste_x, paste_y), resized_crop)
        
        # Convert to RGB for PDF export
        slides.append(canvas.convert("RGB"))

    if slides:
        output_path = Path(output_pdf)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Exporting {len(slides)} slides to {output_pdf}...")
        slides[0].save(
            output_pdf,
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=slides[1:]
        )
        print("Success! Carousel exported.")
    else:
        print("No slides found in config.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="High-res source image (PNG)")
    parser.add_argument("--config", required=True, help="JSON config defining crops")
    parser.add_argument("--out", required=True, help="Output PDF file")
    parser.add_argument("--bg", default="#0d1117", help="Background color for square canvas")
    args = parser.parse_args()
    slice_carousel(args.image, args.config, args.out, args.bg)
