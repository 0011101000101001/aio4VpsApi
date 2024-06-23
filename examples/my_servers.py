from FourVps.api import FourVpsClient
import asyncio

API_KEY = "YOR_API_KEY"
four_vps_client = FourVpsClient(API_KEY)


async def main():
    """You can use a context manager to interact with the api, this approach is most recommended."""
    async with four_vps_client as client:
        my_servers_list = await client.my_servers()

        for server in my_servers_list:
            print(server)  # ServerInfo dataclass
            """
            class ServerInfo:
                server_id: int
                tid: int
                name: str
                price: float
                dc_id: int
                image: str
                mem: int
                cpu: int
                disk: int
                ipv4: Optional[str]
                status: str
                tariff_name: str
                time: int
                expired: int
                autoprolong: bool
                period: int
                api_order: bool
            """


if __name__ == "__main__":
    asyncio.run(main())
