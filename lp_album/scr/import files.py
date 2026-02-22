from pathlib import Path
from datetime import datetime

PROJECT_NAME = "LP Album · Memory Wall 💛"

BASE_DIR = Path(r"E:\lp\lp_album")
INPUT_DIR = BASE_DIR / "raw"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_FILE = OUTPUT_DIR / "index.html"

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}


def get_images(folder: Path) -> list[Path]:
    """Collect images (non-recursive) and sort by modified time (newest first)."""
    if not folder.exists():
        return []

    imgs = [
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in VALID_EXTENSIONS
    ]
    imgs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return imgs


def esc(s: str) -> str:
    """Basic HTML escaping."""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


def build_html(images: list[Path]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    cards = []
    for img in images:
        # Use relative path so the HTML is portable
        src = f"../raw/{img.name}"
        alt = esc(img.name)
        cards.append(
            f"""
            <a class="card" href="{src}" target="_blank" title="{alt}">
              <img loading="lazy" src="{src}" alt="{alt}">
              <div class="name">{alt}</div>
            </a>
            """
        )

    cards_html = "\n".join(cards) if cards else "<div class='empty'>No images found in /raw</div>"

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{esc(PROJECT_NAME)}</title>
<style>
  :root {{
    --bg: #f6f6f6;
    --card: #ffffff;
    --text: #222;
    --muted: #777;
    --shadow: rgba(0,0,0,.06);
    --radius: 16px;
  }}

  body {{
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Noto Sans",Arial,sans-serif;
  }}

  .wrap {{
    max-width: 1100px;
    margin: 0 auto;
    padding: 28px 18px 40px;
  }}

  .header {{
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 10px 14px;
    justify-content: space-between;
    margin-bottom: 14px;
  }}

  h1 {{
    font-size: 22px;
    margin: 0;
    letter-spacing: .2px;
  }}

  .meta {{
    color: var(--muted);
    font-size: 13px;
  }}

  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
    gap: 14px;
    margin-top: 14px;
  }}

  .card {{
    display: block;
    background: var(--card);
    border-radius: var(--radius);
    padding: 10px;
    text-decoration: none;
    color: inherit;
    box-shadow: 0 1px 2px var(--shadow);
    transition: transform .08s ease, box-shadow .08s ease;
  }}

  .card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0,0,0,.10);
  }}

  img {{
    width: 100%;
    height: 210px;
    object-fit: cover;
    border-radius: 12px;
    display: block;
  }}

  .name {{
    margin-top: 8px;
    font-size: 12px;
    color: var(--muted);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}

  .footer {{
    margin-top: 18px;
    color: var(--muted);
    font-size: 12px;
    text-align: center;
  }}

  .empty {{
    background: white;
    padding: 16px;
    border-radius: var(--radius);
    box-shadow: 0 1px 2px var(--shadow);
    color: var(--muted);
  }}
</style>
</head>
<body>
  <div class="wrap">
    <div class="header">
      <h1>{esc(PROJECT_NAME)}</h1>
      <div class="meta">Images: {len(images)} · Generated: {now}</div>
    </div>

    <div class="grid">
      {cards_html}
    </div>

    <div class="footer">
      Offline gallery · Click any image to open full size
    </div>
  </div>
</body>
</html>
"""


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    images = get_images(INPUT_DIR)
    html = build_html(images)
    OUTPUT_FILE.write_text(html, encoding="utf-8")

    print("✅ Done!")
    print(f"Open this file in your browser:\n{OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()