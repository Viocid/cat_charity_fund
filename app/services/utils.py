def replace_privat_key(private_key):
    """Форматирование приватного ключа."""
    if private_key is not None:
        return private_key.replace("\\n", "\n")
    return private_key
