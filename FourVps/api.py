import aiohttp
from typing import Optional, Union

from FourVps.types.BackupPeriods import BackupPeriods
from FourVps.types.DataCenters import DataCenter, Period
from FourVps.exceptions.WorkWithErrors import create_exception_by_api_message
from FourVps.types.Ips import ServerIP
from FourVps.types.Messages import Message
from FourVps.types.Servers import ServerCreated, ServerInfo, AdditionalServerInfo
from FourVps.types.Tariffs import ClusterInfo, Tariff, Preset, AvailableUpgradePreset, OsInfo, TariffPreset, \
    GetAvailableUpgradePresets



class FourVpsClient:
    def __init__(self, token: str, base_url: str = "https://4vps.su", timeout: int = 15):
        self.token = token
        self.base_url = base_url
        self.headers = {'Authorization': f"Bearer {self.token}",
                        'User-Agent': 'FourVpsPythonApi'}
        self.timeout = timeout
        self.session = None

    async def _get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(base_url=self.base_url,
                                                 timeout=aiohttp.ClientTimeout(total=self.timeout),
                                                 headers=self.headers)
        return self.session

    async def __get(self, endpoint: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> dict:
        session = await self._get_session()

        async with session.get(endpoint, params=params, headers=headers) as response:
            response_result = await response.json()

            if response_result.get('error', False):
                create_exception_by_api_message(response_result)

            return response_result

    async def __post(self, endpoint: str, json: Optional[dict] = None, headers: Optional[dict] = None) -> dict:
        session = await self._get_session()

        async with session.post(endpoint, json=json, headers=headers) as response:
            response_result = await response.json()

        if response_result.get('error', False):
            create_exception_by_api_message(response_result)

        return response_result

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def __aenter__(self):
        await self._get_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def user_balance(self) -> Union[int, float]:
        result = await self.__get('/api/userBalance')

        return result.get('data').get('userBalance')

    async def get_dc_list(self) -> Optional[list[DataCenter]]:
        """Return list of DataCenter object FourVps.types.DataCenter.DataCenter"""
        result = await self.__get('/api/getDcList')
        data = result.get('data')

        if not data.get('dcList', False):
            return None

        dc_list_data = data.get('dcList')
        dc_list = []

        for dc_id in dc_list_data:
            dc_info = dc_list_data.get(dc_id)
            data_center = DataCenter(dc_info.get('id'),
                                     dc_info.get('city'),
                                     float(dc_info.get('core_price')),
                                     dc_info.get('country'),
                                     dc_info.get('cpu_name'),
                                     dc_info.get('dc_name'),
                                     dc_info.get('description'),
                                     float(dc_info.get('disk_price')),
                                     dc_info.get('eth'),
                                     dc_info.get('flag'),
                                     dc_info.get('frequency'),
                                     dc_info.get('info_name'),
                                     float(dc_info.get('ip_price')),
                                     bool(dc_info.get('ipv6id', False)),
                                     int(dc_info.get('max_core')),
                                     int(dc_info.get('max_disk')),
                                     int(dc_info.get('max_ram')),
                                     dc_info.get('name'),
                                     [Period(period.get('discount'), period.get('period'))
                                      for period in dc_info.get('periods')] if dc_info.get('periods') else None,
                                     dc_info.get('pingdomain'),
                                     dc_info.get('presets'),
                                     float(dc_info.get('ram_price')),
                                     dc_info.get('title'),
                                     dc_info.get('type_ram', None),
                                     bool(dc_info.get('verif', False)))

            dc_list.append(data_center)

        return dc_list

    async def get_tariff_list(self) -> Optional[list[Tariff]]:
        """Return list of Tariffs object FourVps.types.Tariffs.Tariff"""
        result = await self.__get('/api/getTarifList')
        result_list = []

        tariff_list = result.get('data').get('tarifList')

        if not tariff_list:
            return None

        for cluster_id in tariff_list:
            cluster_info = tariff_list.get(cluster_id).get('clusterInfo')
            presets = tariff_list.get(cluster_id).get('presets')

            _cluster_info = ClusterInfo(cluster_info.get('id'),
                                        cluster_info.get('city'),
                                        float(cluster_info.get('core_price')),
                                        cluster_info.get('country'),
                                        cluster_info.get('cpu_name'),
                                        cluster_info.get('dc_name'),
                                        cluster_info.get('description'),
                                        float(cluster_info.get('disk_price')),
                                        cluster_info.get('eth'),
                                        cluster_info.get('flag'),
                                        cluster_info.get('frequency'),
                                        cluster_info.get('info_name'),
                                        float(cluster_info.get('ip_price')),
                                        bool(cluster_info.get('ipv6id', False)),
                                        int(cluster_info.get('max_core')),
                                        int(cluster_info.get('max_disk')),
                                        int(cluster_info.get('max_ram')),
                                        cluster_info.get('name'),
                                        [Period(period.get('discount'), period.get('period'))
                                         for period in cluster_info.get('periods')]
                                        if cluster_info.get('periods') else None,
                                        cluster_info.get('pingdomain'),
                                        cluster_info.get('presets'),
                                        float(cluster_info.get('ram_price')),
                                        cluster_info.get('title'),
                                        cluster_info.get('type_ram', None),
                                        bool(cluster_info.get('verif', False)))
            presets_list = []
            for preset in presets:
                preset = presets.get(preset)
                available_presets = preset.get('getAvailableUpgradePresets', None)

                if available_presets:
                    temp_list = []
                    for key, value in available_presets.items():
                        temp_list.append(AvailableUpgradePreset(
                            value.get('cpu_number'),
                            value.get('id'),
                            value.get('name'),
                            value.get('nameFull'),
                            value.get('price'),
                            value.get('ram'),
                            value.get('ram_mib'),
                            value.get('rom'),
                            value.get('rom_mib')
                        ))
                    available_presets = temp_list

                one_preset = Preset(
                    preset.get('id'),
                    preset.get('name'),
                    preset.get('nameFull'),
                    preset.get('commentParsed').get('cpu_name'),
                    preset.get('commentParsed').get('eth'),
                    preset.get('commentParsed').get('frequency'),
                    preset.get('commentParsed').get('price'),
                    preset.get('cpu_number'),
                    preset.get('dc_id'),
                    available_presets,
                    [OsInfo(int(key), value) for key, value in preset.get('osNames').items()],
                    preset.get('ram_mib'),
                    preset.get('rom'))

                presets_list.append(one_preset)

            result_list.append(Tariff(_cluster_info, presets_list))

        return result_list

    async def buy_server(self,
                         tariff_id: int,
                         datacenter_id: int,
                         ostempl_id: int,
                         server_name: str,
                         domain: Optional[str] = None,
                         period: int = 720) -> ServerCreated:

        additional_options = {}

        if domain:
            additional_options['domain'] = domain

        result = await self.__post('/api/action/buyServer', json={'tarif': tariff_id,
                                                                  'datacenter': datacenter_id,
                                                                  'ostempl': ostempl_id,
                                                                  'name': server_name,
                                                                  'period': period,
                                                                  **additional_options})
        data = result.get('data')

        return ServerCreated(data.get('serverid'), data.get('password'))

    async def buy_ip(self, server_id: int, count: int = 1) -> bool:
        result = await self.__post('/api/action/buyIp', json={'serverid': server_id, 'count': count})

        return bool(result.get('data'))

    async def power_on(self, server_id) -> bool:
        result = await self.__post('/api/action/power_on', json={'serverid': server_id})

        return bool(result.get('data'))

    async def shutdown(self, server_id) -> bool:
        result = await self.__post('/api/action/shutdown', json={'serverid': server_id})

        return bool(result.get('data'))

    async def reboot(self, server_id) -> bool:
        result = await self.__post('/api/action/reboot', json={'serverid': server_id})

        return bool(result.get('data'))

    async def get_vm_link(self, server_id, domain: Optional[str] = None) -> str:
        additional_options = {}

        if domain:
            additional_options['domain'] = domain

        result = await self.__post('/api/action/getVmLink', json={'serverid': server_id, **additional_options})

        return result.get('data').get('redirect')

    async def continue_server(self, server_id: int) -> bool:
        result = await self.__post('/api/action/continueServer', json={'serverid': server_id})

        return bool(result.get('data'))

    async def delete_server(self, server_id: int) -> bool:
        result = await self.__post('/api/action/deleteServer', json={'serverid': server_id})

        return bool(result.get('data'))

    async def reinstall(self, server_id: int, os_id: int, new_password: str) -> bool:
        result = await self.__post('/api/action/reinstall', json={'serverid': server_id,
                                                                  'ostempl': os_id,
                                                                  'password': new_password})

        return bool(result.get('data'))

    # TODO: Проверить работоспособность, доебать разраба пока не пофиксит
    async def change_tariff(self, server_id: int, preset_id: int) -> bool:
        result = await self.__post('/api/action/changeTarif', json={'serverid': server_id,
                                                                    'preset': preset_id})

        return bool(result.get('data'))

    async def change_spec(self, server_id: int, cpu_count: int, ram_count: int, rom_count: int) -> bool:
        result = await self.__post('/api/action/changeSpec', json={'serverid': server_id,
                                                                   'cpu_count': cpu_count,
                                                                   'ram_count': ram_count,
                                                                   'rom_count': rom_count})

        return bool(result.get('data'))

    async def buy_backup(self, server_id: int, period: Union[int]) -> bool:
        result = await self.__post('/api/action/buyBackup', json={'serverid': server_id,
                                                                  'period': period})

        return bool(result.get('data'))

    async def my_servers(self) -> Optional[list[ServerInfo]]:
        result = await self.__get('/api/myservers')

        servers_list = []

        for server in result.get('data').get('serverlist'):
            servers_list.append(ServerInfo(server.get('id'),
                                           server.get('tid'),
                                           server.get('name'),
                                           float(server.get('price')),
                                           server.get('dc'),
                                           server.get('image'),
                                           server.get('mem'),
                                           server.get('cpu'),
                                           server.get('disk'),
                                           server.get('ipv4', None),
                                           server.get('status'),
                                           server.get('tname'),
                                           server.get('time'),
                                           server.get('expired'),
                                           server.get('autoprolong'),
                                           server.get('period'),
                                           server.get('api_order')))

        return servers_list or None

    async def get_tariff_info(self, tariff_id: int, dc_id: int) -> Optional[list[TariffPreset]]:
        result = await self.__get(f'/api/getTarifInfo/{tariff_id}/{dc_id}')

        ready_list_of_tariff_preset = []

        tariff = result.get('data').get('tarifInfo')

        if not tariff:
            return None

        available_presets = tariff.get('getAvailableUpgradePresets', None)

        if available_presets:
            temp_list = []
            for key, value in available_presets.items():
                temp_list.append(AvailableUpgradePreset(
                    value.get('cpu_number'),
                    value.get('id'),
                    value.get('name'),
                    value.get('nameFull'),
                    value.get('price'),
                    value.get('ram'),
                    value.get('ram_mib'),
                    value.get('rom'),
                    value.get('rom_mib')
                ))
            available_presets = temp_list

        t = TariffPreset(tariff.get('id'),
                         tariff.get('name'),
                         tariff.get('nameFull'),
                         tariff.get('commentParsed').get('cpu_name'),
                         tariff.get('commentParsed').get('eth'),
                         tariff.get('commentParsed').get('frequency'),
                         float(tariff.get('commentParsed').get('price')),
                         tariff.get('cpu_number'),
                         tariff.get('dc_id'),
                         available_presets,
                         [OsInfo(int(key), value) for key, value in tariff.get('osNames').items()],
                         tariff.get('ram_mib'),
                         tariff.get('rom'))

        ready_list_of_tariff_preset.append(t)

        return ready_list_of_tariff_preset

    async def get_images(self, tariff_id: int, dc_id: int) -> Optional[list[OsInfo]]:
        result = await self.__get(f'/api/getImages/{tariff_id}/{dc_id}')

        images = result.get('data').get('images')

        if not images:
            return None

        ready_list_of_tariff_preset = [OsInfo(int(key), value) for key, value in images.items()]

        return ready_list_of_tariff_preset

    async def ip_list(self, server_id: int) -> Optional[list[ServerIP]]:
        result = await self.__get(f'/api/iplist/{server_id}')

        ips = result.get('data').get('iplist')

        if not ips:
            return None

        ips_list = []
        for ip in ips:
            ips_list.append(ServerIP(ip.get('id'),
                                     ip.get('name'),
                                     ip.get('ip'),
                                     ip.get('ptr')))

        return ips_list

    async def delete_ip(self, server_id: int, ip_id: int) -> bool:
        result = await self.__post('/api/action/deleteIp', json={'serverid': server_id,
                                                                 'ipid': ip_id})

        return bool(result.get('data'))

    async def get_messages(self) -> Optional[list[Message]]:
        result = await self.__get('/api/getMessages')
        messages = result.get('data').get('messagesList')

        if not messages:
            return None

        _messages = []
        for message in messages:
            _messages.append(Message(message.get('id'),
                                     message.get('title'),
                                     message.get('content'),
                                     message.get('time')))

        return _messages

    async def get_server_info(self, server_id: int) -> Optional[AdditionalServerInfo]:
        result = await self.__get(f'/api/getServerInfo/{server_id}')
        server_info = result.get('data').get('serverInfo')
        dc_info = result.get('data').get('dcInfo')

        if not result.get('data') or not server_info or not dc_info:
            return None

        _server_info = ServerInfo(server_info.get('id'),
                                  server_info.get('tid'),
                                  server_info.get('name'),
                                  float(server_info.get('price')),
                                  server_info.get('dc'),
                                  server_info.get('image'),
                                  server_info.get('mem'),
                                  server_info.get('cpu'),
                                  server_info.get('disk'),
                                  server_info.get('ipv4'),
                                  server_info.get('status'),
                                  server_info.get('tname'),
                                  server_info.get('time'),
                                  server_info.get('expired'),
                                  server_info.get('autoprolong'),
                                  server_info.get('period'),
                                  server_info.get('api_order'))

        _dc_info = DataCenter(dc_info.get('id'),
                              dc_info.get('city'),
                              float(dc_info.get('core_price')),
                              dc_info.get('country'),
                              dc_info.get('cpu_name'),
                              dc_info.get('dc_name'),
                              dc_info.get('description'),
                              float(dc_info.get('disk_price')),
                              dc_info.get('eth'),
                              dc_info.get('flag'),
                              dc_info.get('frequency'),
                              dc_info.get('info_name'),
                              float(dc_info.get('ip_price')),
                              bool(dc_info.get('ipv6id', False)),
                              int(dc_info.get('max_core')),
                              int(dc_info.get('max_disk')),
                              int(dc_info.get('max_ram')),
                              dc_info.get('name'),
                              [Period(period.get('discount'), period.get('period'))
                               for period in dc_info.get('periods')] if dc_info.get('periods') else None,
                              dc_info.get('pingdomain'),
                              dc_info.get('presets'),
                              float(dc_info.get('ram_price')),
                              dc_info.get('title'),
                              dc_info.get('type_ram', None),
                              bool(dc_info.get('verif', False)))

        return AdditionalServerInfo(_server_info, _dc_info)

    async def auto_prolong(self, server_id: int) -> bool:
        result = await self.__post('/api/action/autoprolong', json={'serverid': server_id})

        return bool(result.get('data'))

    async def get_available_upgrade_presets(self, server_id: int) -> list[GetAvailableUpgradePresets]:
        result = await self.__post('/api/action/getAvailableUpgradePresets', json={'serverid': server_id})

        available_upgrade_list = []

        for key, value in result.get('data').items():
            temp = GetAvailableUpgradePresets(value.get('id'),
                                              value.get('name'),
                                              value.get('nameFull'),
                                              float(value.get('price')),
                                              value.get('cpu_number'),
                                              value.get('ram_mib'),
                                              value.get('rom_mib'),
                                              value.get('ram'),
                                              value.get('rom'))

            available_upgrade_list.append(temp)

        return available_upgrade_list

    async def get_backup_periods(self) -> list[BackupPeriods]:
        result = await self.__get('/api/action/getBackupPeriods')

        return [BackupPeriods(int(key), float(value)) for key, value in result.get('data').items()]

    async def delete_backup(self, server_id: int, period: int) -> bool:
        result = await self.__post('/api/action/deleteBackup', json={'serverid': server_id,
                                                                     'period': period})

        return bool(result.get('data'))