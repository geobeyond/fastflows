"""Authn and Authz module."""
from fastflows.config.app import settings
from fastapi_opa import OPAConfig
from fastapi_opa.auth import OIDCAuthentication
from fastapi_opa.auth import OIDCConfig


# The hostname of your Open Policy Agent instance
opa_host = settings.AUTH.OPA_URL
if opa_host:
    # In this example we use OIDC authentication flow (using Keycloak)
    oidc_config = OIDCConfig(
        well_known_endpoint=settings.AUTH.OIDC_WELL_KNOWN_ENDPOINT,
        # well known endpoint
        app_uri=settings.UVICORN.HOST,  # host where this app is running
        # client id of your app configured in the identity provider
        client_id=settings.AUTH.OIDC_CLIENT_ID,
        # the client secret retrieved from your identity provider
        client_secret=settings.AUTH.OIDC_CLIENT_SECRET,
    )
    oidc_auth = OIDCAuthentication(oidc_config)
    opa_config = OPAConfig(authentication=oidc_auth, opa_host=opa_host)
else:
    opa_config = None
