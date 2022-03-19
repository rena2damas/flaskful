def url_parse(path):
    path = path.strip("/")
    return f"/{path}/" if path else "/"
