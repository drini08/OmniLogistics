from fastapi import Header, HTTPException, status

# This is your Master Key for the Prishtina Hub
MASTER_API_KEY = "OmniPrishtina2026"

def get_api_key(access_token: str = Header(None)):
    """
    Checks the 'access-token' header sent by the Streamlit app.
    """
    if access_token != MASTER_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Security Key"
        )
    return access_token