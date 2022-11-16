from django import template
from colorsys import rgb_to_hls, hls_to_rgb

register = template.Library()


@register.simple_tag
def darken(hex, rate):
    """Returns a darkened (or lightened if rate is negative) color"""

    if len(hex) != 7:
        raise ValueError("Color must be in hexadecimal format.")

    # Convert hexadecimal value to a tuple of rgb values between 0 and 1
    rgb = [int(hex[x:x + 2], 16) / 255.0 for x in (1, 3, 5)]

    # Apply rate to lightness value, make sure it stays within [0,1] boundaries
    h, l, s = rgb_to_hls(*rgb)
    new_l = max(0, min(1, l * (1 - (rate / 100))))

    # Convert value back to hexadecimal
    new_rgb = hls_to_rgb(h, new_l, s)
    new_hex = "".join("{:02X}".format(int(n * 255)) for n in new_rgb)
    return f"#{new_hex}"
