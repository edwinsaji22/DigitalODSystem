import os
import math
from PIL import Image, ImageDraw, ImageFont

def draw_rounded_rectangle(draw, xy, radius, fill, outline, width=3):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def draw_pill(draw, xy, fill, outline, width=3):
    x0, y0, x1, y1 = xy
    radius = (y1 - y0) // 2
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def draw_diamond(draw, cx, cy, w, h, fill, outline, width=3):
    points = [
        (cx, cy - h // 2),  # Top
        (cx + w // 2, cy),  # Right
        (cx, cy + h // 2),  # Bottom
        (cx - w // 2, cy)   # Left
    ]
    draw.polygon(points, fill=fill, outline=outline)
    if width > 1:
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            draw.line([p1, p2], fill=outline, width=width)

def draw_arrow(draw, start, end, color=(0, 0, 0), width=3, arrow_size=14):
    x0, y0 = start
    x1, y1 = end
    draw.line([start, end], fill=color, width=width)
    
    dx = x1 - x0
    dy = y1 - y0
    angle = math.atan2(dy, dx)
    
    a1 = angle + math.pi * 5 / 6
    a2 = angle - math.pi * 5 / 6
    p1 = (x1 + arrow_size * math.cos(a1), y1 + arrow_size * math.sin(a1))
    p2 = (x1 + arrow_size * math.cos(a2), y1 + arrow_size * math.sin(a2))
    draw.polygon([end, p1, p2], fill=color)

def draw_centered_text(draw, cx, cy, text, font, fill=(0, 0, 0), line_spacing=6):
    lines = text.split("\n")
    line_heights = []
    line_widths = []
    for l in lines:
        bbox = draw.textbbox((0, 0), l, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        line_widths.append(w)
        line_heights.append(h)
    
    total_h = sum(line_heights) + (len(lines) - 1) * line_spacing
    cur_y = cy - total_h / 2
    
    for i, l in enumerate(lines):
        lx = cx - line_widths[i] / 2
        draw.text((lx, cur_y), l, font=font, fill=fill)
        cur_y += line_heights[i] + line_spacing

def create_workflow_diagram(num_roles=3, filename="workflow_diagram.png"):
    W = 1400 if num_roles == 3 else 1200
    H = 1580
    img = Image.new("RGB", (W, H), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Fonts
    title_font = ImageFont.truetype("C:\\Windows\\Fonts\\timesbd.ttf", 36)
    node_font_bold = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 22)
    node_font_regular = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 18)
    label_font = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 20)

    # Title Top Left
    draw.text((60, 45), "6.2 Workflow Diagram", font=title_font, fill=(0, 0, 0))

    CX = 500 if num_roles == 2 else 580

    # Colors
    c_purple_fill = (226, 218, 252)
    c_purple_bdr  = (126, 96, 232)
    c_blue_fill   = (198, 222, 253)
    c_blue_bdr    = (75, 137, 230)
    c_green_fill  = (190, 243, 212)
    c_green_bdr   = (48, 168, 102)
    c_yellow_fill = (254, 236, 172)
    c_yellow_bdr  = (226, 174, 42)
    c_pink_fill   = (254, 210, 218)
    c_pink_bdr    = (214, 68, 90)
    c_cyan_fill   = (182, 243, 243)
    c_cyan_bdr    = (36, 178, 178)
    c_orange_fill = (254, 218, 182)
    c_orange_bdr  = (232, 134, 58)

    # 1. Start Pill
    y_start = 120
    h_pill = 60
    w_pill = 180
    draw_pill(draw, (CX - w_pill//2, y_start, CX + w_pill//2, y_start + h_pill), fill=c_purple_fill, outline=c_purple_bdr, width=3)
    draw_centered_text(draw, CX, y_start + h_pill//2, "Start", node_font_bold)

    # 2. Home Page
    y_home = y_start + h_pill + 40
    w_rect = 340
    h_rect = 64
    draw_arrow(draw, (CX, y_start + h_pill), (CX, y_home), width=3, arrow_size=12)
    draw_rounded_rectangle(draw, (CX - w_rect//2, y_home, CX + w_rect//2, y_home + h_rect), radius=14, fill=c_blue_fill, outline=c_blue_bdr, width=3)
    draw_centered_text(draw, CX, y_home + h_rect//2, "Home Page", node_font_bold)

    # 3. Register / Login
    y_login = y_home + h_rect + 40
    draw_arrow(draw, (CX, y_home + h_rect), (CX, y_login), width=3, arrow_size=12)
    draw_rounded_rectangle(draw, (CX - w_rect//2, y_login, CX + w_rect//2, y_login + h_rect), radius=14, fill=c_green_fill, outline=c_green_bdr, width=3)
    draw_centered_text(draw, CX, y_login + h_rect//2, "Register / Login", node_font_bold)

    # 4. Validation (Servlet)
    y_val = y_login + h_rect + 40
    h_val = 74
    draw_arrow(draw, (CX, y_login + h_rect), (CX, y_val), width=3, arrow_size=12)
    draw_rounded_rectangle(draw, (CX - w_rect//2, y_val, CX + w_rect//2, y_val + h_val), radius=14, fill=c_yellow_fill, outline=c_yellow_bdr, width=3)
    draw_centered_text(draw, CX, y_val + h_val//2, "Validation\n(Servlet)", node_font_bold)

    # 5. Diamond: Valid Credentials?
    y_diam_cy = y_val + h_val + 95
    diam_w = 260
    diam_h = 120
    draw_arrow(draw, (CX, y_val + h_val), (CX, y_diam_cy - diam_h//2), width=3, arrow_size=12)
    draw_diamond(draw, CX, y_diam_cy, diam_w, diam_h, fill=c_pink_fill, outline=c_pink_bdr, width=3)
    draw_centered_text(draw, CX, y_diam_cy, "Valid\nCredentials?", node_font_bold)

    # Error Box (Branch "No")
    x_err_w = 280
    x_err_h = 80
    x_err_left = CX + diam_w//2 + 140
    x_err_cx = x_err_left + x_err_w//2
    y_err_top = y_diam_cy - x_err_h//2

    draw_arrow(draw, (CX + diam_w//2, y_diam_cy), (x_err_left, y_diam_cy), width=3, arrow_size=12)
    draw.text((CX + diam_w//2 + 45, y_diam_cy - 32), "No", font=label_font, fill=(0, 0, 0))

    draw_rounded_rectangle(draw, (x_err_left, y_err_top, x_err_left + x_err_w, y_err_top + x_err_h), radius=14, fill=c_pink_fill, outline=c_pink_bdr, width=3)
    draw_centered_text(draw, x_err_cx, y_diam_cy, "Show Error Message\n(Back to Login)", node_font_bold)

    # Loop back to Register / Login
    y_loop_target = y_login + h_rect//2
    draw.line([(x_err_cx, y_err_top), (x_err_cx, y_loop_target)], fill=(0, 0, 0), width=3)
    draw_arrow(draw, (x_err_cx, y_loop_target), (CX + w_rect//2, y_loop_target), width=3, arrow_size=12)

    # "Yes" branch down -> Create Session
    y_sess = y_diam_cy + diam_h//2 + 60
    draw_arrow(draw, (CX, y_diam_cy + diam_h//2), (CX, y_sess), width=3, arrow_size=12)
    draw.text((CX + 12, y_diam_cy + diam_h//2 + 18), "Yes", font=label_font, fill=(0, 0, 0))

    # 6. Create Session
    h_sess = 64
    draw_rounded_rectangle(draw, (CX - w_rect//2, y_sess, CX + w_rect//2, y_sess + h_sess), radius=14, fill=c_cyan_fill, outline=c_cyan_bdr, width=3)
    draw_centered_text(draw, CX, y_sess + h_sess//2, "Create Session", node_font_bold)

    # 7. Dashboard
    y_dash = y_sess + h_sess + 40
    draw_arrow(draw, (CX, y_sess + h_sess), (CX, y_dash), width=3, arrow_size=12)
    draw_rounded_rectangle(draw, (CX - w_rect//2, y_dash, CX + w_rect//2, y_dash + h_rect), radius=14, fill=c_purple_fill, outline=c_purple_bdr, width=3)
    draw_centered_text(draw, CX, y_dash + h_rect//2, "Dashboard", node_font_bold)

    # 8. Portal Router
    y_router = y_dash + h_rect + 40
    w_router = 380
    draw_arrow(draw, (CX, y_dash + h_rect), (CX, y_router), width=3, arrow_size=12)
    router_text = "Student / Staff / HOD Portal" if num_roles == 3 else "User / Admin Portal"
    draw_rounded_rectangle(draw, (CX - w_router//2, y_router, CX + w_router//2, y_router + h_rect), radius=14, fill=c_blue_fill, outline=c_blue_bdr, width=3)
    draw_centered_text(draw, CX, y_router + h_rect//2, router_text, node_font_bold)

    # Portals Branching
    y_branch = y_router + h_rect + 35
    y_portals = y_branch + 35
    h_pbox = 84

    if num_roles == 3:
        w_pbox = 320
        cx_s = 220
        cx_m = CX
        cx_h = CX + (CX - cx_s)

        # Bus line
        draw.line([(CX, y_router + h_rect), (CX, y_branch)], fill=(0, 0, 0), width=3)
        draw.line([(cx_s, y_branch), (cx_h, y_branch)], fill=(0, 0, 0), width=3)
        draw_arrow(draw, (cx_s, y_branch), (cx_s, y_portals), width=3, arrow_size=12)
        draw_arrow(draw, (cx_m, y_branch), (cx_m, y_portals), width=3, arrow_size=12)
        draw_arrow(draw, (cx_h, y_branch), (cx_h, y_portals), width=3, arrow_size=12)

        # 3 Boxes
        draw_rounded_rectangle(draw, (cx_s - w_pbox//2, y_portals, cx_s + w_pbox//2, y_portals + h_pbox), radius=14, fill=c_green_fill, outline=c_green_bdr, width=3)
        draw_centered_text(draw, cx_s, y_portals + h_pbox//2, "Student Portal\n(Access student features)", node_font_regular)

        draw_rounded_rectangle(draw, (cx_m - w_pbox//2, y_portals, cx_m + w_pbox//2, y_portals + h_pbox), radius=14, fill=c_orange_fill, outline=c_orange_bdr, width=3)
        draw_centered_text(draw, cx_m, y_portals + h_pbox//2, "Staff Portal\n(Verify / Reject requests)", node_font_regular)

        draw_rounded_rectangle(draw, (cx_h - w_pbox//2, y_portals, cx_h + w_pbox//2, y_portals + h_pbox), radius=14, fill=c_blue_fill, outline=c_blue_bdr, width=3)
        draw_centered_text(draw, cx_h, y_portals + h_pbox//2, "HOD Portal\n(Executive Sanction)", node_font_regular)

        # Merge down
        y_merge = y_portals + h_pbox + 35
        draw.line([(cx_s, y_portals + h_pbox), (cx_s, y_merge)], fill=(0, 0, 0), width=3)
        draw.line([(cx_m, y_portals + h_pbox), (cx_m, y_merge)], fill=(0, 0, 0), width=3)
        draw.line([(cx_h, y_portals + h_pbox), (cx_h, y_merge)], fill=(0, 0, 0), width=3)
        draw.line([(cx_s, y_merge), (cx_h, y_merge)], fill=(0, 0, 0), width=3)

    else:
        # 2 Roles matching the exact friend's layout
        w_pbox = 360
        cx_s = CX - 220
        cx_h = CX + 220

        # Bus line
        draw.line([(CX, y_router + h_rect), (CX, y_branch)], fill=(0, 0, 0), width=3)
        draw.line([(cx_s, y_branch), (cx_h, y_branch)], fill=(0, 0, 0), width=3)
        draw_arrow(draw, (cx_s, y_branch), (cx_s, y_portals), width=3, arrow_size=12)
        draw_arrow(draw, (cx_h, y_branch), (cx_h, y_portals), width=3, arrow_size=12)

        draw_rounded_rectangle(draw, (cx_s - w_pbox//2, y_portals, cx_s + w_pbox//2, y_portals + h_pbox), radius=14, fill=c_green_fill, outline=c_green_bdr, width=3)
        draw_centered_text(draw, cx_s, y_portals + h_pbox//2, "Student Portal\n(Access user features)", node_font_regular)

        draw_rounded_rectangle(draw, (cx_h - w_pbox//2, y_portals, cx_h + w_pbox//2, y_portals + h_pbox), radius=14, fill=c_orange_fill, outline=c_orange_bdr, width=3)
        draw_centered_text(draw, cx_h, y_portals + h_pbox//2, "Staff / HOD Portal\n(Access admin features)", node_font_regular)

        # Merge down
        y_merge = y_portals + h_pbox + 35
        draw.line([(cx_s, y_portals + h_pbox), (cx_s, y_merge)], fill=(0, 0, 0), width=3)
        draw.line([(cx_h, y_portals + h_pbox), (cx_h, y_merge)], fill=(0, 0, 0), width=3)
        draw.line([(cx_s, y_merge), (cx_h, y_merge)], fill=(0, 0, 0), width=3)

    # Final Arrow to Log Out
    y_logout = y_merge + 35
    draw_arrow(draw, (CX, y_merge), (CX, y_logout), width=3, arrow_size=12)

    # Log Out Pill
    draw_pill(draw, (CX - w_pill//2, y_logout, CX + w_pill//2, y_logout + h_pill), fill=c_purple_fill, outline=c_purple_bdr, width=3)
    draw_centered_text(draw, CX, y_logout + h_pill//2, "Log Out", node_font_bold)

    # Crop to content height
    final_h = y_logout + h_pill + 60
    img_cropped = img.crop((0, 0, W, final_h))
    
    out_path = os.path.join(r"c:\Users\ivins\Desktop\MCA\DigitalODSystem", filename)
    img_cropped.save(out_path, quality=95)
    print(f"Saved: {out_path} ({W}x{final_h})")

if __name__ == "__main__":
    create_workflow_diagram(num_roles=3, filename="workflow_diagram.png")
    create_workflow_diagram(num_roles=2, filename="workflow_diagram_exact_match.png")
