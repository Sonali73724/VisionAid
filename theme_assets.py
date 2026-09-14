import os
import math
from PIL import Image, ImageDraw

ICONS_DIR = os.path.join(os.path.dirname(__file__), "assets", "icons")
TEXTURES_DIR = os.path.join(os.path.dirname(__file__), "assets", "textures")

os.makedirs(ICONS_DIR, exist_ok=True)
os.makedirs(TEXTURES_DIR, exist_ok=True)

# -------------------------------------------------------------
# LILAC & PINK PALETTE
# -------------------------------------------------------------
COLOR_LILAC = (192, 132, 252, 255)       # #C084FC Soft radiant lilac
COLOR_LILAC_LIGHT = (233, 213, 255, 255) # #E9D5FF
COLOR_PINK = (244, 114, 182, 255)        # #F472B6 Vibrant blossom pink
COLOR_PINK_LIGHT = (252, 231, 243, 255)  # #FCE7F3
COLOR_ROSE = (251, 113, 133, 255)        # #FB7185 Coral rose
COLOR_MAGENTA = (232, 121, 249, 255)     # #E879F9 Orchid fuchsia
COLOR_CRIMSON = (244, 63, 94, 255)       # #F43F5E Soft crimson
COLOR_WHITE = (253, 244, 255, 255)       # #FDF4FF Warm lilac-white


def create_settings_icon(path):
    """Draw a clean, beautiful lilac/pink gear cog icon."""
    size = (128, 128)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = 64, 64
    r_outer = 48
    r_hole = 18

    # 8 gear teeth
    num_teeth = 8
    for i in range(num_teeth):
        angle = i * (2 * math.pi / num_teeth)
        tx = cx + math.cos(angle) * (r_outer - 4)
        ty = cy + math.sin(angle) * (r_outer - 4)
        draw.ellipse([tx - 12, ty - 12, tx + 12, ty + 12], fill=COLOR_PINK)

    # Outer gear ring
    draw.ellipse([cx - r_outer + 6, cy - r_outer + 6, cx + r_outer - 6, cy + r_outer - 6], fill=COLOR_LILAC)
    # Inner cutout hole
    draw.ellipse([cx - r_hole, cy - r_hole, cx + r_hole, cy + r_hole], fill=(0, 0, 0, 0))
    # Subtle inner pink border ring
    draw.arc([cx - r_hole - 3, cy - r_hole - 3, cx + r_hole + 3, cy + r_hole + 3], start=0, end=360, fill=COLOR_PINK, width=3)
    img.save(path, "PNG")


def create_camera_icon(path):
    """Draw a modern camera with lens."""
    size = (128, 128)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Top flash notch
    draw.rounded_rectangle([48, 22, 80, 38], radius=6, fill=COLOR_PINK)
    # Main camera body
    draw.rounded_rectangle([20, 34, 108, 104], radius=18, fill=COLOR_LILAC)
    # Lens outer
    draw.ellipse([42, 48, 86, 92], fill=COLOR_WHITE)
    # Lens pupil
    draw.ellipse([52, 58, 76, 82], fill=(42, 23, 62, 255))
    # Lens glint
    draw.ellipse([66, 62, 72, 68], fill=COLOR_PINK)
    img.save(path, "PNG")


def create_eye_icon(path):
    """Draw a stylized vision eye with glowing pupil."""
    size = (128, 128)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Eyeball curve
    draw.chord([16, 28, 112, 100], start=0, end=180, fill=COLOR_LILAC)
    draw.chord([16, 28, 112, 100], start=180, end=360, fill=COLOR_LILAC)
    # Iris
    draw.ellipse([42, 42, 86, 86], fill=(48, 24, 72, 255))
    # Pupil
    draw.ellipse([52, 52, 76, 76], fill=COLOR_PINK)
    # Eye sparkle
    draw.ellipse([64, 54, 72, 62], fill=COLOR_WHITE)
    img.save(path, "PNG")


def create_text_icon(path):
    """Draw a clean document page with lines."""
    size = (128, 128)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Sheet background
    draw.rounded_rectangle([30, 18, 98, 110], radius=14, fill=COLOR_PINK)
    # Folded corner
    draw.polygon([(78, 18), (98, 38), (78, 38)], fill=(255, 205, 230, 255))
    # Document lines
    draw.rounded_rectangle([42, 46, 86, 54], radius=4, fill=COLOR_WHITE)
    draw.rounded_rectangle([42, 62, 86, 70], radius=4, fill=COLOR_WHITE)
    draw.rounded_rectangle([42, 78, 76, 86], radius=4, fill=COLOR_WHITE)
    draw.rounded_rectangle([42, 94, 64, 102], radius=4, fill=COLOR_WHITE)
    img.save(path, "PNG")


def create_shield_icon(path):
    """Draw a safety shield outline with inner star."""
    size = (128, 128)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    pts = [(64, 18), (102, 32), (102, 74), (64, 110), (26, 74), (26, 32)]
    draw.polygon(pts, fill=COLOR_ROSE)
    inner_pts = [(64, 28), (92, 40), (92, 70), (64, 98), (36, 70), (36, 40)]
    draw.polygon(inner_pts, fill=(54, 20, 44, 255))
    draw.ellipse([54, 52, 74, 72], fill=COLOR_WHITE)
    img.save(path, "PNG")


def create_mic_icon(path):
    """Draw a modern podcast microphone."""
    size = (128, 128)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Capsule
    draw.rounded_rectangle([48, 20, 80, 72], radius=16, fill=COLOR_MAGENTA)
    # Stand arc
    draw.arc([36, 42, 92, 88], start=0, end=180, fill=COLOR_WHITE, width=6)
    # Stand pole & base
    draw.line([(64, 88), (64, 106)], fill=COLOR_WHITE, width=6)
    draw.line([(44, 106), (84, 106)], fill=COLOR_WHITE, width=6)
    img.save(path, "PNG")


def create_stop_icon(path):
    """Draw a rounded stop square."""
    size = (128, 128)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outer pill
    draw.rounded_rectangle([20, 20, 108, 108], radius=26, fill=COLOR_CRIMSON)
    # Inner stop mark
    draw.rounded_rectangle([44, 44, 84, 84], radius=10, fill=COLOR_WHITE)
    img.save(path, "PNG")


def create_back_icon(path):
    """Draw a left chevron arrow."""
    size = (128, 128)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.line([(78, 34), (46, 64), (78, 94)], fill=COLOR_WHITE, width=12, joint="curve")
    img.save(path, "PNG")


def create_find_icon(path):
    """Draw a modern target finder / radar crosshair icon."""
    size = (128, 128)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = 64, 64

    # Outer target ring
    draw.arc([cx - 48, cy - 48, cx + 48, cy + 48], start=0, end=360, fill=COLOR_LILAC, width=6)
    # Mid radar ring
    draw.arc([cx - 30, cy - 30, cx + 30, cy + 30], start=0, end=360, fill=COLOR_PINK, width=4)
    # Crosshair ticks
    draw.line([(cx, cy - 56), (cx, cy - 38)], fill=COLOR_WHITE, width=4)
    draw.line([(cx, cy + 38), (cx, cy + 56)], fill=COLOR_WHITE, width=4)
    draw.line([(cx - 56, cy), (cx - 38, cy)], fill=COLOR_WHITE, width=4)
    draw.line([(cx + 38, cy), (cx + 56, cy)], fill=COLOR_WHITE, width=4)
    # Center target bullseye
    draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=COLOR_PINK)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=COLOR_WHITE)
    img.save(path, "PNG")


def create_radar_icon(path):
    """Draw a 3D spatial audio wave radar icon."""
    size = (128, 128)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = 64, 64

    # Sound wave arcs radiating outward
    draw.arc([cx - 46, cy - 46, cx + 46, cy + 46], start=300, end=60, fill=COLOR_LILAC, width=7)
    draw.arc([cx - 30, cy - 30, cx + 30, cy + 30], start=290, end=70, fill=COLOR_PINK, width=6)
    draw.arc([cx - 16, cy - 16, cx + 16, cy + 16], start=280, end=80, fill=COLOR_WHITE, width=5)

    # Left sound wave arcs
    draw.arc([cx - 46, cy - 46, cx + 46, cy + 46], start=120, end=240, fill=COLOR_LILAC, width=7)
    draw.arc([cx - 30, cy - 30, cx + 30, cy + 30], start=110, end=250, fill=COLOR_PINK, width=6)
    draw.arc([cx - 16, cy - 16, cx + 16, cy + 16], start=100, end=260, fill=COLOR_WHITE, width=5)

    # Center sound emitter beacon
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=COLOR_WHITE)
    img.save(path, "PNG")


def create_face_icon(path):
    """Draw a friendly smiling face accessibility icon."""
    size = (128, 128)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = 64, 64

    # Head circle
    draw.ellipse([cx - 48, cy - 48, cx + 48, cy + 48], fill=COLOR_LILAC)
    # Inner face mask
    draw.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], fill=(46, 24, 68, 255))
    # Glowing eyes
    draw.ellipse([cx - 24, cy - 16, cx - 12, cy - 4], fill=COLOR_PINK)
    draw.ellipse([cx + 12, cy - 16, cx + 24, cy - 4], fill=COLOR_PINK)
    draw.ellipse([cx - 20, cy - 14, cx - 16, cy - 10], fill=COLOR_WHITE)
    draw.ellipse([cx + 16, cy - 14, cx + 20, cy - 10], fill=COLOR_WHITE)
    # Smiling mouth arc
    draw.arc([cx - 26, cy - 6, cx + 26, cy + 28], start=20, end=160, fill=COLOR_WHITE, width=6)
    # Rosy cheeks
    draw.ellipse([cx - 32, cy + 6, cx - 22, cy + 16], fill=(244, 114, 182, 180))
    draw.ellipse([cx + 22, cy + 6, cx + 32, cy + 16], fill=(244, 114, 182, 180))
    img.save(path, "PNG")


def create_status_icon(path):
    """Draw a clean, vibrant glowing status beacon dot icon."""
    size = (128, 128)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = 64, 64

    # Outer soft ambient glow ring
    draw.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], fill=(192, 132, 252, 60))
    # Mid glow aura
    draw.ellipse([cx - 38, cy - 38, cx + 38, cy + 38], fill=(233, 213, 255, 120))
    # Bright radiant core
    draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(255, 255, 255, 255))
    # Inner accent ring
    draw.arc([cx - 24, cy - 24, cx + 24, cy + 24], start=0, end=360, fill=(192, 132, 252, 255), width=4)
    img.save(path, "PNG")


def create_globe_icon(path):
    """Draw a 3D international language globe icon."""
    size = (128, 128)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = 64, 64

    # Outer globe sphere
    draw.ellipse([cx - 48, cy - 48, cx + 48, cy + 48], outline=COLOR_LILAC, width=6)
    # Equator horizontal line
    draw.line([(cx - 48, cy), (cx + 48, cy)], fill=COLOR_PINK, width=5)
    # Latitude arcs
    draw.arc([cx - 44, cy - 26, cx + 44, cy + 26], start=0, end=360, fill=COLOR_WHITE, width=4)
    # Meridian longitude ellipse
    draw.ellipse([cx - 24, cy - 48, cx + 24, cy + 48], outline=COLOR_LILAC, width=5)
    # Center axis
    draw.line([(cx, cy - 48), (cx, cy + 48)], fill=COLOR_WHITE, width=4)
    img.save(path, "PNG")


def create_user_icon(path):
    """Draw a modern user profile avatar icon."""
    size = (128, 128)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = 64, 64

    # Head circle
    draw.ellipse([cx - 22, 18, cx + 22, 62], fill=COLOR_LILAC)
    # Shoulders arc
    draw.chord([cx - 44, 56, cx + 44, 116], start=0, end=180, fill=COLOR_PINK)
    # Inner neck collar
    draw.ellipse([cx - 14, 52, cx + 14, 70], fill=(42, 24, 62, 255))
    img.save(path, "PNG")


def create_lock_icon(path):
    """Draw a security padlock icon."""
    size = (128, 128)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = 64, 64

    # Shackle arch
    draw.arc([cx - 22, 18, cx + 22, 62], start=180, end=0, fill=COLOR_WHITE, width=8)
    draw.line([(cx - 22, 40), (cx - 22, 58)], fill=COLOR_WHITE, width=8)
    draw.line([(cx + 22, 40), (cx + 22, 58)], fill=COLOR_WHITE, width=8)

    # Padlock body
    draw.rounded_rectangle([cx - 36, 54, cx + 36, 110], radius=16, fill=COLOR_PINK)
    # Keyhole
    draw.ellipse([cx - 8, 70, cx + 8, 86], fill=COLOR_WHITE)
    draw.polygon([(cx - 4, 82), (cx + 4, 82), (cx + 6, 96), (cx - 6, 96)], fill=COLOR_WHITE)
    img.save(path, "PNG")


def create_check_icon(path):
    """Draw a glowing verification checkmark badge."""
    size = (128, 128)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = 64, 64

    # Outer circle badge
    draw.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], fill=COLOR_LILAC)
    # Inner fill
    draw.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(76, 28, 102, 255))
    # Checkmark line
    draw.line([(cx - 22, cy), (cx - 6, cy + 16), (cx + 24, cy - 14)], fill=COLOR_WHITE, width=8, joint="curve")
    img.save(path, "PNG")


def save_vertical_gradient(path, color_top, color_bottom, width=64, height=128):
    """Generate a vertical gradient image file."""
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        factor = y / float(height - 1)
        r = int(color_top[0] * (1 - factor) + color_bottom[0] * factor)
        g = int(color_top[1] * (1 - factor) + color_bottom[1] * factor)
        b = int(color_top[2] * (1 - factor) + color_bottom[2] * factor)
        a = int(color_top[3] * (1 - factor) + color_bottom[3] * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b, a))
    img.save(path, "PNG")


def generate_all_assets():
    """Generate all PNG icons and gradient textures."""
    create_settings_icon(os.path.join(ICONS_DIR, "icon_settings.png"))
    create_status_icon(os.path.join(ICONS_DIR, "icon_status.png"))
    create_camera_icon(os.path.join(ICONS_DIR, "icon_camera.png"))
    create_eye_icon(os.path.join(ICONS_DIR, "icon_eye.png"))
    create_text_icon(os.path.join(ICONS_DIR, "icon_text.png"))
    create_shield_icon(os.path.join(ICONS_DIR, "icon_shield.png"))
    create_mic_icon(os.path.join(ICONS_DIR, "icon_mic.png"))
    create_stop_icon(os.path.join(ICONS_DIR, "icon_stop.png"))
    create_back_icon(os.path.join(ICONS_DIR, "icon_back.png"))
    create_find_icon(os.path.join(ICONS_DIR, "icon_find.png"))
    create_radar_icon(os.path.join(ICONS_DIR, "icon_radar.png"))
    create_face_icon(os.path.join(ICONS_DIR, "icon_face.png"))
    create_globe_icon(os.path.join(ICONS_DIR, "icon_globe.png"))
    create_user_icon(os.path.join(ICONS_DIR, "icon_user.png"))
    create_lock_icon(os.path.join(ICONS_DIR, "icon_lock.png"))
    create_check_icon(os.path.join(ICONS_DIR, "icon_check.png"))

    # Generate gradients
    save_vertical_gradient(os.path.join(TEXTURES_DIR, "bg_grad.png"), (26, 15, 40, 255), (14, 8, 22, 255))
    save_vertical_gradient(os.path.join(TEXTURES_DIR, "card_grad.png"), (42, 24, 62, 255), (28, 16, 42, 255))
    save_vertical_gradient(os.path.join(TEXTURES_DIR, "card_active_grad.png"), (76, 28, 102, 255), (48, 18, 68, 255))
    save_vertical_gradient(os.path.join(TEXTURES_DIR, "hud_grad.png"), (36, 18, 54, 230), (22, 10, 34, 230))
    save_vertical_gradient(os.path.join(TEXTURES_DIR, "btn_grad.png"), (244, 114, 182, 255), (219, 39, 119, 255))
    save_vertical_gradient(os.path.join(TEXTURES_DIR, "badge_grad.png"), (192, 132, 252, 255), (147, 51, 234, 255))

    print("All Lilac & Pink icons and gradient textures created successfully!")


if __name__ == "__main__":
    generate_all_assets()
