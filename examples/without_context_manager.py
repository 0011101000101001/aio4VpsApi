from FourVps.api import FourVpsClient
import asyncio


API_KEY = "YOR_API_KEY"
client = FourVpsClient(API_KEY)


async def main():
    balance = await client.user_balance()
    print(balance)  # 11205.9
    """be sure to close the connection"""
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
