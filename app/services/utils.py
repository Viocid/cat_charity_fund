from urllib.parse import urljoin


def replace_privat_key(private_key):
    """Форматирование приватного ключа."""
    if private_key is not None:
        return private_key.replace("\\n", "\n")
    return private_key


def url(docs_url, spreadsheet_id):
    return urljoin(docs_url, spreadsheet_id)
