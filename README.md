# aio4vps
### Fully asynchronous API for 4vps.su. 
The API is fully implemented. You can call the client.METHOD_NAME methods you see in https://4vps.su/page/api.

### Dependencies
```
aiohttp==3.9.5
```

Example
```python
from FourVps.api import FourVpsClient
import asyncio


API_KEY = "YOR_API_KEY"
four_vps_client = FourVpsClient(API_KEY)


async def main():
    """You can use a context manager to interact with the api, this approach is most recommended."""
    async with four_vps_client as client:
        """
        obtaining balance using the user_balance method
        https://4vps.su/page/api#userBalance
        """
        balance = await client.user_balance()  # return float
        print(balance)  # 11625.9


if __name__ == "__main__":
    asyncio.run(main())

```

For more examples - go to examples folder.
