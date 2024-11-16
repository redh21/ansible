# -*- coding: utf-8 -*-
from pyzabbix import ZabbixAPI, ZabbixAPIException

zabbix_server   = 'http://10.118.220.36/zabbix'
zabbix_user     = 'Admin'
zabbix_password = 'P@ssw0rd!23'

try:
    zapi = ZabbixAPI(zabbix_server)
    zapi.login(zabbix_user, zabbix_password)

    host_name = input('Enter host name: ')
    host_ip   = input('Enter host ip: ')

    # Получаем идентификатор группы хостов
    groups = zapi.hostgroup.get(filter={'name': 'Windows servers'})
    if not groups:
        raise ZabbixAPIException("Host group 'Windows servers' not found.")
    group_id = groups[0]['groupid']

    # Получаем идентификатор шаблона
    templates = zapi.template.get(filter={'name': 'Template OS Windows by Zabbix agent'})
    if not templates:
        raise ZabbixAPIException("Template 'OS Windows by Zabbix agent' not found.")
    template_id = templates[0]['templateid']

    # Создание нового хоста
    host_create_result = zapi.host.create(
        host=host_name,
        interfaces=[{
            'type': 1,
            'main': 1,
            'useip': 1,
            'ip': host_ip,
            'dns': '',
            'port': '10050'
        }],
        groups=[{'groupid': group_id}],
        templates=[{'templateid': template_id}]
    )

    print(f"Host '{host_name}' created successfully. Host ID: {host_create_result['hostids']}")

except ZabbixAPIException as e:
    print(f"Zabbix API Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    # Важно всегда закрывать соединение
    if 'zapi' in locals():
        zapi.logout()
