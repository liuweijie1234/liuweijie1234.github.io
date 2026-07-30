

认证与权限

使用API Key或JWT（FastAPI内置支持）：

```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def validate_api_key(api_key: str = Depends(api_key_header)):
    if api_key != "valid_key":
        raise HTTPException(status_code=403, detail="Invalid API Key")
```