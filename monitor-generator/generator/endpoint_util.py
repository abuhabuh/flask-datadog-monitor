def clean_endpoint_for_naming(endpoint: str) -> str:
    """Convert endpoints like '/' and '/page/one' to 'root' and 'page_one'
    """
    if endpoint == '/':
        endpoint = 'root'
    else:
        endpoint = endpoint.replace('/', '_')
        if endpoint.startswith('_'):
            endpoint = endpoint[1:]
    return endpoint

