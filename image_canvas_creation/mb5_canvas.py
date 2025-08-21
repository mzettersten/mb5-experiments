#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path
from PIL import Image

REQUIRED_COLS = {
    "left_image_path_1", "right_image_path_1",
    "left_image_path_2", "right_image_path_2"
}

def make_boxed_image(img_path, max_w, max_h, box_color, box_pad):
    """
    Matte image to the box color (prevents dark halos), resize with aspect,
    then place on a tight colored box (+uniform padding).
    """
    im = Image.open(img_path).convert("RGBA")

    # Matte to box color before resize -> eliminates black halos
    bg = Image.new("RGBA", im.size, box_color)
    matted = Image.alpha_composite(bg, im)  # opaque RGBA

    w, h = matted.size
    scale = min(max_w / w, max_h / h)
    new_w = max(1, int(round(w * scale)))
    new_h = max(1, int(round(h * scale)))
    im_resized = matted.resize((new_w, new_h), Image.LANCZOS)

    box_w = new_w + 2 * box_pad
    box_h = new_h + 2 * box_pad
    box = Image.new("RGBA", (box_w, box_h), box_color)
    box.paste(im_resized, (box_pad, box_pad))  # opaque, no mask
    return box

def compose_pair(left_path, right_path, *, canvas_w, canvas_h, bg, rel_size,
                 box_colors=("white", "white"), box_pad=0,
                 left_xy=None, right_xy=None):
    """
    Place left/right images (each in a tight colored box) on the canvas.
    left_xy/right_xy are CENTER pixel coords of the box. Defaults to half-centers.
    """
    max_w = (canvas_w // 2) * rel_size
    max_h = canvas_h * rel_size

    canvas = Image.new("RGBA", (canvas_w, canvas_h), bg)

    left_img  = make_boxed_image(left_path,  max_w, max_h, box_colors[0], box_pad)
    right_img = make_boxed_image(right_path, max_w, max_h, box_colors[1], box_pad)

    if left_xy is None:
        left_xy = (canvas_w // 4, canvas_h // 2)
    if right_xy is None:
        right_xy = (3 * canvas_w // 4, canvas_h // 2)

    # center -> top-left
    lx = int(left_xy[0]  - left_img.width  / 2)
    ly = int(left_xy[1]  - left_img.height / 2)
    rx = int(right_xy[0] - right_img.width / 2)
    ry = int(right_xy[1] - right_img.height / 2)

    canvas.paste(left_img,  (lx, ly), left_img)
    canvas.paste(right_img, (rx, ry), right_img)

    # Flatten to RGB
    flattened = Image.new("RGB", (canvas_w, canvas_h), bg)
    flattened.paste(canvas, mask=canvas.split()[-1])
    return flattened

def process_csv(csv_path: Path, out_base: Path, *, canvas_w, canvas_h, bg,
                rel_size, box_colors, box_pad, left_xy, right_xy, name_prefix):
    out_subdir = out_base / csv_path.stem
    out_subdir.mkdir(parents=True, exist_ok=True)

    with csv_path.open(newline="") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{csv_path}: missing required columns: {', '.join(sorted(missing))}")

        for idx, row in enumerate(reader, start=1):
            try:
                img1 = compose_pair(
                    row["left_image_path_1"], row["right_image_path_1"],
                    canvas_w=canvas_w, canvas_h=canvas_h, bg=bg, rel_size=rel_size,
                    box_colors=box_colors, box_pad=box_pad,
                    left_xy=left_xy, right_xy=right_xy
                )
                out1 = out_subdir / f"{name_prefix}_{idx}_test1.png"
                img1.save(out1)
                print(f"[{csv_path.name}] Saved {out1}")

                img2 = compose_pair(
                    row["left_image_path_2"], row["right_image_path_2"],
                    canvas_w=canvas_w, canvas_h=canvas_h, bg=bg, rel_size=rel_size,
                    box_colors=box_colors, box_pad=box_pad,
                    left_xy=left_xy, right_xy=right_xy
                )
                out2 = out_subdir / f"{name_prefix}_{idx}_test2.png"
                img2.save(out2)
                print(f"[{csv_path.name}] Saved {out2}")

            except FileNotFoundError as e:
                print(f"[{csv_path.name} | Row {idx}] Skipped (missing file): {e}")
            except Exception as e:
                print(f"[{csv_path.name} | Row {idx}] Skipped (error): {e}")

def main():
    ap = argparse.ArgumentParser(
        description="Read all CSVs in a folder; write outputs to per-CSV subfolders under --outdir."
    )
    ap.add_argument("--csv_dir", required=True,
                    help="Directory containing CSV files.")
    ap.add_argument("--pattern", default="*.csv",
                    help="Glob pattern for CSVs inside --csv_dir (default: *.csv).")
    ap.add_argument("--recursive", action="store_true",
                    help="Recurse into subdirectories when searching for CSVs.")
    ap.add_argument("--outdir", default="outputs",
                    help="Base output folder; each CSV gets a subfolder named after its filename stem.")
    ap.add_argument("--name_prefix", default="trial",
                    help="Filename prefix inside each subfolder (trial_<n>_testX.png).")

    # Canvas & placement
    ap.add_argument("--canvas_w", type=int, default=1600, help="Canvas width (px).")
    ap.add_argument("--canvas_h", type=int, default=900, help="Canvas height (px).")
    ap.add_argument("--bg", default="#FFFFFF", help="Canvas background color.")
    ap.add_argument("--rel_size", type=float, default=0.9,
                    help="Relative size (0–1) per image vs its half-canvas area.")
    ap.add_argument("--box_colors", nargs=2, default=["white", "white"],
                    help="Two colors for left/right image boxes (e.g., 'lightblue lightgreen').")
    ap.add_argument("--box_pad", type=int, default=0,
                    help="Uniform padding (px) inside each colored box around the image.")
    ap.add_argument("--left_xy", nargs=2, type=int, default=None,
                    help="CENTER pixel coords (x y) for LEFT image. Applies to both arrangements.")
    ap.add_argument("--right_xy", nargs=2, type=int, default=None,
                    help="CENTER pixel coords (x y) for RIGHT image. Applies to both arrangements.")
    args = ap.parse_args()

    out_base = Path(args.outdir); out_base.mkdir(parents=True, exist_ok=True)
    left_xy  = tuple(args.left_xy)  if args.left_xy  else None
    right_xy = tuple(args.right_xy) if args.right_xy else None
    box_colors = tuple(args.box_colors)

    csv_root = Path(args.csv_dir)
    if not csv_root.is_dir():
        raise SystemExit(f"--csv_dir not found or not a directory: {csv_root}")

    # Collect CSVs
    candidates = (
        sorted(csv_root.rglob(args.pattern)) if args.recursive
        else sorted(csv_root.glob(args.pattern))
    )
    if not candidates:
        print(f"No CSVs matched {args.pattern} in {csv_root} (recursive={args.recursive}).")
        return

    for csv_path in candidates:
        try:
            process_csv(
                csv_path, out_base,
                canvas_w=args.canvas_w, canvas_h=args.canvas_h, bg=args.bg,
                rel_size=args.rel_size, box_colors=box_colors, box_pad=args.box_pad,
                left_xy=left_xy, right_xy=right_xy, name_prefix=args.name_prefix
            )
        except Exception as e:
            print(f"[{csv_path.name}] Error: {e}")

if __name__ == "__main__":
    main()

#Example Usage:
#python mb5_canvas.py --csv ./trial_lists --outdir arranged --canvas_w 1920 --canvas_h 1200 --rel_size 0.6 --bg "#000000"  --box_pad 12 --box_colors "#FFFFFF" "#FFFFFF" --left_xy 460 600 --right_xy 1460 600

