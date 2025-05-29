import jwt
import requests
import os
from jwt.algorithms import RSAAlgorithm

OIDC_ISSUER = os.getenv("OIDC_ISSUER")
CLIENT_ID = os.getenv("CLIENT_ID")

jwks_cache = None

def get_jwks():
    global jwks_cache
    if jwks_cache:
        return jwks_cache
    jwks_uri = f"{OIDC_ISSUER}/protocol/openid-connect/certs"
    response = requests.get(jwks_uri)
    if response.status_code != 200:
        raise Exception("Unable to fetch JWKS keys from Keycloak")
    jwks_cache = response.json()
    return jwks_cache

def verify_token(token):
    jwks = get_jwks()
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = None

    for key in jwks["keys"]:
        if key["kid"] == unverified_header.get("kid"):
            rsa_key = RSAAlgorithm.from_jwk(
                {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
            )
            break

    if rsa_key is None:
        raise Exception("Public key not found in JWKS")

    try:
        payload = jwt.decode(
            token,
            key=rsa_key,
            algorithms=["RS256"],
            audience=CLIENT_ID,
            issuer=OIDC_ISSUER
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError as e:
        raise Exception(f"Invalid token: {e}")
