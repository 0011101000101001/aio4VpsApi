from FourVps.api import FourVpsClient
import asyncio


API_KEY = "YOR_API_KEY"
four_vps_client = FourVpsClient(API_KEY)


async def main():
    """You can use a context manager to interact with the api, this approach is most recommended."""
    async with four_vps_client as client:
        """
        https://4vps.su/page/api#buyServer
        """
        tariffs = await client.get_tariff_list()

        """
        Tariff is dataclass FourVps.types.Tariffs.Tariff
        class Tariff:
            cluster_info: ClusterInfo
            presets: list[Preset]
        
        DataCenter is dataclass FourVps.types.DataCenters.DataCenter
        class ClusterInfo(DataCenter):
            pass
            
        class DataCenter:
            id: int
            city: str
            core_price: float
            country: str
            cpu_name: str
            dc_name: str
            description: str
            disk_price: float
            eth: str
            flag: str
            frequency: str
            info_name: str
            ip_price: Union[int, float]
            ipv6: bool 
            max_core: int
            max_disk: int
            max_ram: int
            name: str
            periods: Optional[list[Period]]
            ping_domain: str 
            presets: list[int]
            ram_price: Union[int, float]
            title: str
            type_ram: Optional[str]
            need_verification: bool 
            
        Preset is a dataclass FourVps.types.Tariffs.Preset
        class Preset:
            id: int
            name: str
            name_full: str
            cpu_name: str # commentParsed[cpu_name]
            eth: str # commentParsed[eth]
            frequency: str # commentParsed[frequency]
            price: float # commentParsed[price]
            cpu_number: int
            dc_id: int
            available_upgrade_presets: Optional[list[AvailableUpgradePreset]]
            os_list: list[OsInfo]
            ram_mib: int
            rom: int
        """
        for tariff in tariffs[:1]:  # for example - take first tariff
            tariff_id = tariff.presets[0].id
            dc_id = tariff.presets[0].dc_id
            os_lists = await client.get_images(tariff_id, dc_id)  # list[OsInfo(id=22, name='Alma Linux 8'), OsInfo(id=3, name='Debian 10')]
            os_id = None

            for os in os_lists:
                if os.name == 'Debian 10':
                    os_id = os.id
                    break

            server_info = await client.buy_server(tariff_id, dc_id, os_id, 'TEST_SERVER_NAME')
            print(server_info)  # ServerCreated(server_id='98104', password='super_strong_password')



if __name__ == "__main__":
    asyncio.run(main())
