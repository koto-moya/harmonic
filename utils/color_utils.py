def get_relative_luminance(r, g, b):
    """Calculate relative luminance using sRGB."""
    def to_linear(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    
    r_lin = to_linear(r)
    g_lin = to_linear(r)
    b_lin = to_linear(b)
    
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin

def get_contrast_ratio(color1, color2):
    """Calculate contrast ratio between two colors."""
    # Convert hex to RGB
    rgb1 = tuple(int(color1.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    rgb2 = tuple(int(color2.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    l1 = get_relative_luminance(*rgb1)
    l2 = get_relative_luminance(*rgb2)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)

def get_contrast_color(background_color):
    """Return white or black depending on background contrast."""
    WCAG_AA_THRESHOLD = 4.5
    
    white_contrast = get_contrast_ratio(background_color, "#ffffff")
    black_contrast = get_contrast_ratio(background_color, "#000000")
    
    return "#000000" if black_contrast >= WCAG_AA_THRESHOLD else "#ffffff"
