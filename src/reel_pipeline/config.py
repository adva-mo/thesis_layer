from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

DEFAULT_MODEL = "fal-ai/kling-video/v1/standard/image-to-video"
ASPECT_RATIO  = "9:16"
CACHE_DIR     = REPO_ROOT / ".cache" / "kling"

LOGO_PATH    = REPO_ROOT / "assets" / "branding" / "logo-wide.png"
LOGO_WIDTH   = 200   # px at 1080-wide frame
LOGO_PADDING = 36    # px from top-right edges


def _load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip()
    return env


_env = _load_env(REPO_ROOT / ".env")
FAL_KEY = _env.get("FAL_KEY", "")
