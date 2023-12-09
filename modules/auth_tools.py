from fastapi.security import APIKeyHeader

secret = "SECRET_TOKEN"
api_key_token = APIKeyHeader(name='Token')
    

