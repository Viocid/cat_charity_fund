from app.core.config import settings

JWT_TOKEN_URL = "auth/jwt/login"
JWT_AUTH_BACKEND_NAME = "jwt"
NAME_MIN_LEN = 1
NAME_MAX_LEN = 100
PREFIX = "/charity_project"
TAGS = ("charity_projects",)
DONATION_PREFIX = "/donation"
DONATION_TAGS = ("donations",)
ZERO = 0
ONE = 1
GOOGLE_PREFIX = "/google"
GOOGLE_TAGS = ("Google",)
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
DOCS_URL = "https://docs.google.com/spreadsheets/d/"

def replace_privat_key(private_key):
    if private_key is not None:
        return private_key.replace("\\n", "\n")
    return private_key
INFO = {
    "type": settings.type,
    "project_id": settings.project_id,
    "private_key_id": settings.private_key_id,
    "private_key": replace_privat_key(settings.private_key),
    "client_email": settings.client_email,
    "client_id": settings.client_id,
    "auth_uri": settings.auth_uri,
    "token_uri": settings.token_uri,
    "auth_provider_x509_cert_url": settings.auth_provider_x509_cert_url,
    "client_x509_cert_url": settings.client_x509_cert_url,
}
FORMAT = "%Y/%m/%d %H:%M:%S"
