from fastapi import Header, HTTPException

# مفتاح ثابت للتجربة
VALID_API_KEY = "1234567890abcdef"

def get_api_key(x_api_key: str = Header(...)):
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API Key")
    return x_api_key
