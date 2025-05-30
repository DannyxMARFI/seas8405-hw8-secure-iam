import jwt
import os
from jwt import PyJWKClient

OIDC_ISSUER = os.getenv("OIDC_ISSUER")
CLIENT_ID = os.getenv("CLIENT_ID")

def verify_token(token):
    jwks_url = f"{OIDC_ISSUER}/protocol/openid-connect/certs"
    jwk_client = PyJWKClient(jwks_url)

    try:
        signing_key = jwk_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=CLIENT_ID,
            issuer=OIDC_ISSUER
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError as e:
        raise Exception(f"Invalid token: {e}")
