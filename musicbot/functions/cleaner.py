def clean_title(caption):
    words = caption.split()
    kept = [w for w in words if not w.startswith("#")]
    return " ".join(kept)