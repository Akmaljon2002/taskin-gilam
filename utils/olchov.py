
def olchov(text):
    rest = text
    if text == 'm':
        rest = 'metr'
    if text == 'metr':
        rest = f"m²"

    return rest
