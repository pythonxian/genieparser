import unittest
from unittest.mock import Mock

# ATS
from ats.topology import Device

from genie.metaparser.util.exceptions import SchemaEmptyParserError, \
                                       SchemaMissingKeyError

from genie.libs.parser.iosxe.show_routing import ShowIpRoute, ShowIpv6RouteUpdated,\
                                      ShowIpRouteWord, ShowIpv6RouteWord

# ============================================
# unit test for 'show ip route'
# =============================================
class test_show_ip_route(unittest.TestCase):
    """
       unit test for show ip route
    """
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}
 
    golden_output_1 = {'execute.return_value': '''
        R1_iosv#show ip route
        Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
               D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
               N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
               E1 - OSPF external type 1, E2 - OSPF external type 2
               i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
               ia - IS-IS inter area, * - candidate default, U - per-user static route
               o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
               a - application route
               + - replicated route, % - next hop override

        Gateway of last resort is not set

              10.1.0.0/32 is subnetted, 1 subnets
        C        10.4.1.1 is directly connected, Loopback0
              10.4.0.0/32 is subnetted, 1 subnets
        S        10.16.2.2 [1/0] via 10.186.2.2, GigabitEthernet0/1
                         [1/0] via 10.1.2.2, GigabitEthernet0/0
              10.9.0.0/32 is subnetted, 1 subnets
        S        10.36.3.3 is directly connected, GigabitEthernet0/3
                         is directly connected, GigabitEthernet0/2
              10.0.0.0/8 is variably subnetted, 5 subnets, 2 masks
        C        10.1.2.0/24 is directly connected, GigabitEthernet0/0
        L        10.1.2.1/32 is directly connected, GigabitEthernet0/0
        C        10.1.3.0/24 is directly connected, GigabitEthernet0/2
        L        10.1.3.1/32 is directly connected, GigabitEthernet0/2
        O        10.2.3.0/24 [110/2] via 10.186.2.2, 06:46:59, GigabitEthernet0/1
                             [110/2] via 10.1.2.2, 06:46:59, GigabitEthernet0/0
               10.229.0.0/32 is subnetted, 1 subnets
        i L1     10.151.22.22 [115/20] via 10.186.2.2, 06:47:04, GigabitEthernet0/1
                         [115/20] via 10.1.2.2, 06:47:04, GigabitEthernet0/0
              10.4.0.0/32 is subnetted, 1 subnets
        B        10.16.32.32 [200/0] via 10.66.12.12, 1d00h
        '''}

    golden_parsed_output_1 = {
        'vrf':{
            'default':{
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '10.4.1.1/32': {
                                'route': '10.4.1.1/32',
                                'active': True,
                                'source_protocol_codes': 'C',
                                'source_protocol':'connected',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'Loopback0': {
                                            'outgoing_interface': 'Loopback0',
                                        },
                                    },
                                },
                            },
                            '10.16.2.2/32': {
                                'route': '10.16.2.2/32',
                                'active': True,
                                'route_preference': 1,
                                'metric': 0,
                                'source_protocol_codes': 'S',
                                'source_protocol': 'static',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.186.2.2',
                                            'outgoing_interface': 'GigabitEthernet0/1',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.1.2.2',
                                            'outgoing_interface': 'GigabitEthernet0/0',
                                        },
                                    },
                                },
                            },
                            '10.36.3.3/32': {
                                'route': '10.36.3.3/32',
                                'active': True,
                                'source_protocol_codes': 'S',
                                'source_protocol': 'static',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/3': {
                                            'outgoing_interface': 'GigabitEthernet0/3',
                                        },
                                        'GigabitEthernet0/2': {
                                            'outgoing_interface': 'GigabitEthernet0/2',
                                        },
                                    },
                                },
                            },
                            '10.1.2.0/24': {
                                'route': '10.1.2.0/24',
                                'active': True,
                                'source_protocol_codes': 'C',
                                'source_protocol': 'connected',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0': {
                                            'outgoing_interface': 'GigabitEthernet0/0',
                                        },
                                    },

                                },
                            },
                            '10.1.2.1/32': {
                                'route': '10.1.2.1/32',
                                'active': True,
                                'source_protocol_codes': 'L',
                                'source_protocol': 'local',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0': {
                                            'outgoing_interface': 'GigabitEthernet0/0',
                                        },
                                    },

                                },
                            },
                            '10.1.3.0/24': {
                                'route': '10.1.3.0/24',
                                'active': True,
                                'source_protocol_codes': 'C',
                                'source_protocol': 'connected',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/2': {
                                            'outgoing_interface': 'GigabitEthernet0/2',
                                        },
                                    },
                                },
                            },
                            '10.1.3.1/32': {
                                'route': '10.1.3.1/32',
                                'active': True,
                                'source_protocol_codes': 'L',
                                'source_protocol': 'local',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/2': {
                                            'outgoing_interface': 'GigabitEthernet0/2',
                                        },
                                    },
                                },
                            },
                            '10.2.3.0/24': {
                                'route': '10.2.3.0/24',
                                'active': True,
                                'route_preference': 110,
                                'metric': 2,
                                'source_protocol_codes': 'O',
                                'source_protocol': 'ospf',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.186.2.2',
                                            'updated': '06:46:59',
                                            'outgoing_interface': 'GigabitEthernet0/1',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.1.2.2',
                                            'updated': '06:46:59',
                                            'outgoing_interface': 'GigabitEthernet0/0',
                                        },
                                    },
                                },
                            },
                            '10.151.22.22/32': {
                                'route': '10.151.22.22/32',
                                'active': True,
                                'route_preference': 115,
                                'metric': 20,
                                'source_protocol_codes': 'i L1',
                                'source_protocol': 'isis',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.186.2.2',
                                            'updated': '06:47:04',
                                            'outgoing_interface': 'GigabitEthernet0/1',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.1.2.2',
                                            'updated': '06:47:04',
                                            'outgoing_interface': 'GigabitEthernet0/0',
                                        },
                                    },
                                },
                            },
                            '10.16.32.32/32': {
                                'route': '10.16.32.32/32',
                                'active': True,
                                'route_preference': 200,
                                'metric': 0,
                                'source_protocol_codes': 'B',
                                'source_protocol': 'bgp',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.66.12.12',
                                            'updated': '1d00h',
                                        },
                                    },
                                },
                            },

                        },
                    },
                },
            },
        },
    }

    golden_output_2_with_vrf = {'execute.return_value':'''
        PE1#sh ip route vrf VRF1
        Routing Table: VRF1
        Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
               D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
               N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
               E1 - OSPF external type 1, E2 - OSPF external type 2
               i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
               ia - IS-IS inter area, * - candidate default, U - per-user static route
               o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
               a - application route
               + - replicated route, % - next hop override, p - overrides from PfR

        Gateway of last resort is not set

              10.0.0.0/24 is subnetted, 50 subnets
        O        10.0.0.0 [110/1] via 10.81.1.2, 01:02:20, GigabitEthernet0/0/2.100
        O        10.0.1.0 [110/1] via 10.81.1.2, 01:02:20, GigabitEthernet0/0/2.100
        O        10.0.2.0 [110/1] via 10.81.1.2, 01:02:20, GigabitEthernet0/0/2.100
              10.145.0.0/24 is subnetted, 50 subnets
        B        10.145.0.0 [200/1] via 192.168.51.1, 01:01:10
        B        10.145.1.0 [200/1] via 192.168.51.1, 01:01:10
        B        10.145.2.0 [200/1] via 192.168.51.1, 01:01:10
              10.81.0.0/8 is variably subnetted, 2 subnets, 2 masks
        C        10.81.1.0/24 is directly connected, GigabitEthernet0/0/2.100
        L        10.81.1.1/32 is directly connected, GigabitEthernet0/0/2.100
        B     192.168.4.0/24 [200/0] via 192.168.51.1, 01:01:10
        '''}

    golden_parsed_output_2_with_vrf = {
        'vrf': {
            'VRF1': {
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '10.0.0.0/24': {
                                'route': '10.0.0.0/24',
                                'active': True,
                                'route_preference': 110,
                                'metric': 1,
                                'source_protocol_codes': 'O',
                                'source_protocol': 'ospf',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.81.1.2',
                                            'updated': '01:02:20',
                                            'outgoing_interface': 'GigabitEthernet0/0/2.100',
                                        },
                                    },
                                },
                            },
                            '10.0.1.0/24': {
                                'route': '10.0.1.0/24',
                                'active': True,
                                'route_preference': 110,
                                'metric': 1,
                                'source_protocol_codes': 'O',
                                'source_protocol': 'ospf',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.81.1.2',
                                            'updated': '01:02:20',
                                            'outgoing_interface': 'GigabitEthernet0/0/2.100',
                                        },
                                    },
                                },
                            },
                            '10.0.2.0/24': {
                                'route': '10.0.2.0/24',
                                'active': True,
                                'route_preference': 110,
                                'metric': 1,
                                'source_protocol_codes': 'O',
                                'source_protocol': 'ospf',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.81.1.2',
                                            'updated': '01:02:20',
                                            'outgoing_interface': 'GigabitEthernet0/0/2.100',
                                        },
                                    },
                                },
                            },
                            '10.145.0.0/24': {
                                'route': '10.145.0.0/24',
                                'active': True,
                                'route_preference': 200,
                                'metric': 1,
                                'source_protocol_codes': 'B',
                                'source_protocol': 'bgp',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '192.168.51.1',
                                            'updated': '01:01:10',
                                        },
                                    },
                                },
                            },
                            '10.145.1.0/24': {
                                'route': '10.145.1.0/24',
                                'active': True,
                                'route_preference': 200,
                                'metric': 1,
                                'source_protocol_codes': 'B',
                                'source_protocol': 'bgp',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '192.168.51.1',
                                            'updated': '01:01:10',
                                        },
                                    },
                                },
                            },
                            '10.145.2.0/24': {
                                'route': '10.145.2.0/24',
                                'active': True,
                                'route_preference': 200,
                                'metric': 1,
                                'source_protocol_codes': 'B',
                                'source_protocol': 'bgp',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '192.168.51.1',
                                            'updated': '01:01:10',
                                        },
                                    },
                                },
                            },
                            '10.81.1.0/24': {
                                'route': '10.81.1.0/24',
                                'active': True,
                                'source_protocol_codes': 'C',
                                'source_protocol': 'connected',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/2.100': {
                                            'outgoing_interface': 'GigabitEthernet0/0/2.100',
                                        },
                                    },
                                },
                            },
                            '10.81.1.1/32': {
                                'route': '10.81.1.1/32',
                                'active': True,
                                'source_protocol_codes': 'L',
                                'source_protocol': 'local',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/2.100': {
                                            'outgoing_interface': 'GigabitEthernet0/0/2.100',
                                        },
                                    },
                                },
                            },
                            '192.168.4.0/24': {
                                'route': '192.168.4.0/24',
                                'active': True,
                                'route_preference':200,
                                'metric':0,
                                'source_protocol_codes': 'B',
                                'source_protocol': 'bgp',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '192.168.51.1',
                                            'updated': '01:01:10'},
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }

    golden_parsed_output3 = {
        'vrf': 
            {'OOB_Mgmt': 
                {'address_family': 
                    {'ipv4': 
                        {'routes': 
                            {'10.50.15.0/25': 
                                {'active': True,
                                'next_hop': 
                                    {'outgoing_interface': 
                                        {'FastEthernet0/0': 
                                            {'outgoing_interface': 'FastEthernet0/0'}}},
                                'route': '10.50.15.0/25',
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C'},
                            '10.50.15.12/32': 
                                {'active': True,
                                'next_hop': 
                                    {'outgoing_interface': 
                                        {'FastEthernet0/0': 
                                            {'outgoing_interface': 'FastEthernet0/0'}}},
                                'route': '10.50.15.12/32',
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L'}}}}}}}

    golden_output3 = {'execute.return_value': '''
        Router#show ip route vrf OOB_Mgmt

        Routing Table: OOB_Mgmt
        Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
               D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
               N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
               E1 - OSPF external type 1, E2 - OSPF external type 2
               i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
               ia - IS-IS inter area, * - candidate default, U - per-user static route
               o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
               a - application route
               + - replicated route, % - next hop override, p - overrides from PfR

        Gateway of last resort is 10.50.15.1 to network 0.0.0.0

        S*    0.0.0.0/0 [1/0] via 10.50.15.1
              10.0.0.0/8 is variably subnetted, 2 subnets, 2 masks
        C        10.50.15.0/25 is directly connected, FastEthernet0/0
        L        10.50.15.12/32 is directly connected, FastEthernet0/0
        '''}

    golden_parsed_output4 = {
        'vrf': 
            {'default': 
                {'address_family': 
                    {'ipv4': 
                        {'routes': 
                            {'0.0.0.0/0': 
                                {'active': True,
                                'metric': 100,
                                'next_hop': 
                                    {'next_hop_list': 
                                        {1: 
                                            {'index': 1,
                                            'next_hop': '10.12.7.37',
                                            'outgoing_interface': 'Vlan101',
                                            'updated': '3w6d'},
                                        2: 
                                            {'index': 2,
                                            'next_hop': '10.12.7.33',
                                            'outgoing_interface': 'Vlan100',
                                            'updated': '3w6d'}}},
                                    'route': '0.0.0.0/0',
                                    'route_preference': 115,
                                    'source_protocol': 'isis',
                                    'source_protocol_codes': 'i*L1'},
                            '10.12.6.1/32': 
                                {'active': True,
                                'metric': 200,
                                'next_hop': 
                                    {'next_hop_list': 
                                        {1: 
                                            {'index': 1,
                                            'next_hop': '10.12.7.33',
                                            'outgoing_interface': 'Vlan100',
                                            'updated': '1w1d'}}},
                                'route': '10.12.6.1/32',
                                'route_preference': 115,
                                'source_protocol': 'isis',
                                'source_protocol_codes': 'i ia'},
                            '10.12.6.10/32': 
                                {'active': True,
                                'metric': 200,
                                'next_hop': 
                                    {'next_hop_list': 
                                        {1: 
                                            {'index': 1,
                                            'next_hop': '10.12.7.33',
                                            'outgoing_interface': 'Vlan100',
                                            'updated': '2w1d'}}},
                                    'route': '10.12.6.10/32',
                                    'route_preference': 115,
                                    'source_protocol': 'isis',
                                    'source_protocol_codes': 'i ia'},
                            '10.12.6.13/32': 
                                {'active': True,
                                'metric': 250,
                                'next_hop': 
                                    {'next_hop_list': 
                                        {1: 
                                            {'index': 1,
                                            'next_hop': '10.12.7.33',
                                            'outgoing_interface': 'Vlan100',
                                            'updated': '2w1d'}}},
                                'route': '10.12.6.13/32',
                                'route_preference': 115,
                                'source_protocol': 'isis',
                                'source_protocol_codes': 'i ia'},
                            '10.12.6.14/32': 
                                {'active': True,
                                'metric': 300,
                                'next_hop': 
                                    {'next_hop_list': 
                                        {1: 
                                            {'index': 1,
                                            'next_hop': '10.12.7.37',
                                            'outgoing_interface': 'Vlan101',
                                            'updated': '2w1d'},
                                        2: 
                                            {'index': 2,
                                            'next_hop': '10.12.7.33',
                                            'outgoing_interface': 'Vlan100',
                                            'updated': '2w1d'}}},
                                'route': '10.12.6.14/32',
                                'route_preference': 115,
                                'source_protocol': 'isis',
                                'source_protocol_codes': 'i ia'},
                            '10.12.6.15/32': 
                                {'active': True,
                                'metric': 250,
                                'next_hop': 
                                    {'next_hop_list': 
                                        {1: 
                                            {'index': 1,
                                            'next_hop': '10.12.7.37',
                                            'outgoing_interface': 'Vlan101',
                                            'updated': '2w1d'}}},
                                'route': '10.12.6.15/32',
                                'route_preference': 115,
                                'source_protocol': 'isis',
                                'source_protocol_codes': 'i ia'},
                            '10.12.6.2/32': 
                                {'active': True,
                                'metric': 100,
                                'next_hop': 
                                    {'next_hop_list': 
                                        {1: 
                                            {'index': 1,
                                            'next_hop': '10.12.7.33',
                                            'outgoing_interface': 'Vlan100',
                                            'updated': '6w0d'}}},
                                'route': '10.12.6.2/32',
                                'route_preference': 115,
                                'source_protocol': 'isis',
                                'source_protocol_codes': 'i L1'},
                            '10.12.6.3/32': 
                                {'active': True,
                                'metric': 100,
                                'next_hop': 
                                    {'next_hop_list': 
                                        {1: 
                                            {'index': 1,
                                            'next_hop': '10.12.7.37',
                                            'outgoing_interface': 'Vlan101',
                                            'updated': '3w6d'}}},
                                'route': '10.12.6.3/32',
                                'route_preference': 115,
                                'source_protocol': 'isis',
                                'source_protocol_codes': 'i L1'},
                            '10.12.6.4/32': 
                                {'active': True,
                                'metric': 50,
                                'next_hop': 
                                    {'next_hop_list': 
                                        {1: 
                                            {'index': 1,
                                            'next_hop': '10.12.7.33',
                                            'outgoing_interface': 'Vlan100',
                                            'updated': '6w0d'}}},
                                'route': '10.12.6.4/32',
                                'route_preference': 115,
                                'source_protocol': 'isis',
                                'source_protocol_codes': 'i L1'},
                            '10.12.6.7/32': 
                                {'active': True,
                                'metric': 50,
                                'next_hop': 
                                    {'next_hop_list': 
                                        {1: 
                                            {'index': 1,
                                            'next_hop': '10.12.7.37',
                                            'outgoing_interface': 'Vlan101',
                                            'updated': '3w6d'}}},
                                'route': '10.12.6.7/32',
                                'route_preference': 115,
                                'source_protocol': 'isis',
                                'source_protocol_codes': 'i L1'},
                            '10.12.6.9/32': 
                                {'active': True,
                                'next_hop': 
                                    {'outgoing_interface': 
                                        {'Loopback0': 
                                            {'outgoing_interface': 'Loopback0'}}},
                                'route': '10.12.6.9/32',
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C'},
                            '10.12.7.32/30': 
                                {'active': True,
                                'next_hop': 
                                    {'outgoing_interface': 
                                        {'Vlan100': 
                                            {'outgoing_interface': 'Vlan100'}}},
                                'route': '10.12.7.32/30',
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C'},
                            '10.12.7.34/32': 
                                {'active': True,
                                'next_hop': 
                                    {'outgoing_interface': 
                                        {'Vlan100': 
                                            {'outgoing_interface': 'Vlan100'}}},
                                'route': '10.12.7.34/32',
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L'},
                            '10.12.7.36/30': 
                                {'active': True,
                                'next_hop': 
                                    {'outgoing_interface': 
                                        {'Vlan101': 
                                            {'outgoing_interface': 'Vlan101'}}},
                                'route': '10.12.7.36/30',
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C'},
                            '10.12.7.38/32': 
                                {'active': True,
                                'next_hop': 
                                    {'outgoing_interface': 
                                        {'Vlan101': 
                                            {'outgoing_interface': 'Vlan101'}}},
                                'route': '10.12.7.38/32',
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L'}}}}}}}

    golden_output4 = {'execute.return_value': '''
        Router#show ip route
        Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
               D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
               N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
               E1 - OSPF external type 1, E2 - OSPF external type 2
               i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
               ia - IS-IS inter area, * - candidate default, U - per-user static route
               o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
               a - application route
               + - replicated route, % - next hop override, p - overrides from PfR

        Gateway of last resort is 10.12.7.37 to network 0.0.0.0

        i*L1  0.0.0.0/0 [115/100] via 10.12.7.37, 3w6d, Vlan101
                        [115/100] via 10.12.7.33, 3w6d, Vlan100
              10.0.0.0/8 is variably subnetted, 14 subnets, 2 masks
        i ia     10.12.6.1/32 [115/200] via 10.12.7.33, 1w1d, Vlan100
        i L1     10.12.6.2/32 [115/100] via 10.12.7.33, 6w0d, Vlan100
        i L1     10.12.6.3/32 [115/100] via 10.12.7.37, 3w6d, Vlan101
        i L1     10.12.6.4/32 [115/50] via 10.12.7.33, 6w0d, Vlan100
        i L1     10.12.6.7/32 [115/50] via 10.12.7.37, 3w6d, Vlan101
        C        10.12.6.9/32 is directly connected, Loopback0
        i ia     10.12.6.10/32 [115/200] via 10.12.7.33, 2w1d, Vlan100
        i ia     10.12.6.13/32 [115/250] via 10.12.7.33, 2w1d, Vlan100
        i ia     10.12.6.14/32 [115/300] via 10.12.7.37, 2w1d, Vlan101
                                [115/300] via 10.12.7.33, 2w1d, Vlan100
        i ia     10.12.6.15/32 [115/250] via 10.12.7.37, 2w1d, Vlan101
        C        10.12.7.32/30 is directly connected, Vlan100
        L        10.12.7.34/32 is directly connected, Vlan100
        C        10.12.7.36/30 is directly connected, Vlan101
        L        10.12.7.38/32 is directly connected, Vlan101
        '''}

    def test_empty_1(self):
        self.device = Mock(**self.empty_output)
        obj = ShowIpRoute(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_show_ip_route_1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_1)
        obj = ShowIpRoute(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output_1)

    def test_show_ip_route_2_with_vrf(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_2_with_vrf)
        obj = ShowIpRoute(device=self.device)
        parsed_output = obj.parse(vrf='VRF1')
        self.assertEqual(parsed_output, self.golden_parsed_output_2_with_vrf)

    def test_show_ip_route3(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output3)
        obj = ShowIpRoute(device=self.device)
        parsed_output = obj.parse(vrf='OOB_Mgmt')
        self.assertEqual(parsed_output, self.golden_parsed_output3)

    def test_show_ip_route4(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output4)
        obj = ShowIpRoute(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output4)


###################################################
# unit test for show ipv6 route updated
####################################################
class test_show_ipv6_route_updated(unittest.TestCase):
    """
    unit test for show ipv6 route updated
    """
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}
    golden_output_1 = {'execute.return_value': '''
    R1_iosv#show ipv6 route updated
    IPv6 Routing Table - default - 23 entries
    Codes: C - Connected, L - Local, S - Static, U - Per-user Static route
           B - BGP, HA - Home Agent, MR - Mobile Router, R - RIP
           H - NHRP, I1 - ISIS L1, I2 - ISIS L2, IA - ISIS interarea
           IS - ISIS summary, D - EIGRP, EX - EIGRP external, NM - NEMO
           ND - ND Default, NDp - ND Prefix, DCE - Destination, NDr - Redirect
           O - OSPF Intra, OI - OSPF Inter, OE1 - OSPF ext 1, OE2 - OSPF ext 2
           ON1 - OSPF NSSA ext 1, ON2 - OSPF NSSA ext 2, la - LISP alt
           lr - LISP site-registrations, ld - LISP dyn-eid, a - Application
    LC  2001:1:1:1::1/128 [0/0]
         via Loopback0, receive
          Last updated 22:55:51 04 December 2017
    S   2001:2:2:2::2/128 [1/0]
         via 2001:10:1:2::2, GigabitEthernet0/0
          Last updated 22:57:07 04 December 2017
         via 2001:20:1:2::2, GigabitEthernet0/1
          Last updated 22:57:23 04 December 2017
    S   2001:3:3:3::3/128 [1/0]
         via GigabitEthernet0/2, directly connected
          Last updated 22:57:34 04 December 2017
         via GigabitEthernet0/3, directly connected
          Last updated 22:57:43 04 December 2017
    B   20:0:0:1::/64 [200/1]
        via 192.168.51.1%default, indirectly connected
        Last updated 09:43:27 06 December 2017
    '''}
    golden_parsed_output_1 = {
        'ipv6_unicast_routing_enabled': True,
        'vrf':{
            'default':{
                'address_family': {
                    'ipv6': {
                        'routes': {
                            '2001:1:1:1::1/128': {
                                'route': '2001:1:1:1::1/128',
                                'active': True,
                                'source_protocol_codes': 'LC',
                                'source_protocol': 'local',
                                'route_preference': 0,
                                'metric': 0,
                                'next_hop': {
                                    'outgoing_interface': {
                                        'Loopback0': {
                                            'outgoing_interface': 'Loopback0',
                                            'updated': '22:55:51 04 December 2017',
                                        },
                                    },
                                },
                            },
                            '2001:2:2:2::2/128': {
                                'route': '2001:2:2:2::2/128',
                                'active': True,
                                'route_preference': 1,
                                'metric': 0,
                                'source_protocol_codes': 'S',
                                'source_protocol': 'static',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '2001:10:1:2::2',
                                            'outgoing_interface': 'GigabitEthernet0/0',
                                            'updated': '22:57:07 04 December 2017',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '2001:20:1:2::2',
                                            'outgoing_interface': 'GigabitEthernet0/1',
                                            'updated': '22:57:23 04 December 2017',
                                        },
                                    },
                                },
                            },
                            '2001:3:3:3::3/128': {
                                'route': '2001:3:3:3::3/128',
                                'active': True,
                                'route_preference': 1,
                                'metric': 0,
                                'source_protocol_codes': 'S',
                                'source_protocol': 'static',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/2':{
                                            'outgoing_interface': 'GigabitEthernet0/2',
                                            'updated': '22:57:34 04 December 2017',
                                            },
                                        'GigabitEthernet0/3': {
                                            'outgoing_interface': 'GigabitEthernet0/3',
                                            'updated': '22:57:43 04 December 2017',
                                        },
                                    },
                                },
                            },
                            '20:0:0:1::/64': {
                                'route': '20:0:0:1::/64',
                                'active': True,
                                'route_preference': 200,
                                'metric': 1,
                                'source_protocol_codes': 'B',
                                'source_protocol': 'bgp',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '192.168.51.1',
                                            'updated': '09:43:27 06 December 2017',
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    golden_output_2 = {'execute.return_value': '''
    IPv6 Routing Table - VRF1 - 104 entries
    Codes: C - Connected, L - Local, S - Static, U - Per-user Static route
           B - BGP, R - RIP, H - NHRP, I1 - ISIS L1
           I2 - ISIS L2, IA - ISIS interarea, IS - ISIS summary, D - EIGRP
           EX - EIGRP external, ND - ND Default, NDp - ND Prefix, DCE - Destination
           NDr - Redirect, O - OSPF Intra, OI - OSPF Inter, OE1 - OSPF ext 1
           OE2 - OSPF ext 2, ON1 - OSPF NSSA ext 1, ON2 - OSPF NSSA ext 2
           la - LISP alt, lr - LISP site-registrations, ld - LISP dyn-eid
           a - Application
    O   10::/64 [110/1]
         via FE80::211:1FF:FE00:1, GigabitEthernet0/0/2.100
          Last updated 09:42:39 06 December 2017
    O   10:0:0:1::/64 [110/1]
         via FE80::211:1FF:FE00:1, GigabitEthernet0/0/2.100
          Last updated 09:42:39 06 December 2017
    O   10:0:0:2::/64 [110/1]
         via FE80::211:1FF:FE00:1, GigabitEthernet0/0/2.100
          Last updated 09:42:39 06 December 2017

       '''}
    golden_parsed_output_2 = {
        'ipv6_unicast_routing_enabled': True,
        'vrf': {
            'VRF1': {
                'address_family': {
                    'ipv6': {
                        'routes': {
                            '10::/64': {
                                'route': '10::/64',
                                'active': True,
                                'source_protocol_codes': 'O',
                                'source_protocol': 'ospf',
                                'route_preference': 110,
                                'metric': 1,
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': 'FE80::211:1FF:FE00:1',
                                            'outgoing_interface': 'GigabitEthernet0/0/2.100',
                                            'updated': '09:42:39 06 December 2017',
                                        },
                                    },
                                },
                            },
                            '10:0:0:1::/64': {
                                'route': '10:0:0:1::/64',
                                'active': True,
                                'source_protocol_codes': 'O',
                                'source_protocol': 'ospf',
                                'route_preference': 110,
                                'metric': 1,
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': 'FE80::211:1FF:FE00:1',
                                            'outgoing_interface': 'GigabitEthernet0/0/2.100',
                                            'updated': '09:42:39 06 December 2017',
                                        },
                                    },
                                },
                            },
                            '10:0:0:2::/64': {
                                'route': '10:0:0:2::/64',
                                'active': True,
                                'source_protocol_codes': 'O',
                                'source_protocol': 'ospf',
                                'route_preference': 110,
                                'metric': 1,
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': 'FE80::211:1FF:FE00:1',
                                            'outgoing_interface': 'GigabitEthernet0/0/2.100',
                                            'updated': '09:42:39 06 December 2017',
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    def test_empty_1(self):
        self.device = Mock(**self.empty_output)
        obj = ShowIpv6RouteUpdated(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_show_ipv6_route_1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_1)
        obj = ShowIpv6RouteUpdated(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output_1)

    def test_show_ipv6_route_2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_2)
        obj = ShowIpv6RouteUpdated(device=self.device)
        parsed_output = obj.parse(vrf='VRF1')
        self.assertEqual(parsed_output,self.golden_parsed_output_2)


###################################################
# unit test for show ip route <WROD>
####################################################
class test_show_ip_route_word(unittest.TestCase):
    """unit test for show ip route <WORD>"""

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_output_with_route = {'execute.return_value': '''
        show ip route 192.168.154.0
        Routing entry for 192.168.154.0/24
          Known via "eigrp 1", distance 130, metric 10880, type internal
          Redistributing via eigrp 1
          Last update from 192.168.151.2 on Vlan101, 2w3d ago
          Routing Descriptor Blocks:
          * 192.168.151.2, from 192.168.151.2, 2w3d ago, via Vlan101
              Route metric is 10880, traffic share count is 1
    '''}

    golden_parsed_output_with_route = {
        "entry": {
            "192.168.154.0/24": {
               "mask": "24",
               "type": "type internal",
               "known_via": "eigrp 1",
               "ip": "192.168.154.0",
               "redist_via": "eigrp",
               "distance": "130",
               "metric": "10880",
               "redist_via_tag": "1",
               "update": {
                    "age": "2w3d",
                    "interface": "Vlan101",
                    "from": "192.168.151.2"
               },
               "paths": {
                    1: {
                         "age": "2w3d",
                         "interface": "Vlan101",
                         "from": "192.168.151.2",
                         "metric": "10880",
                         "share_count": "1",
                         "nexthop": "192.168.151.2"
                    }
                }
            }
        },
        "total_prefixes": 1
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowIpRouteWord(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse(route='192.168.154.0')

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_with_route)
        obj = ShowIpRouteWord(device=self.device)
        parsed_output = obj.parse(route='192.168.154.0')
        self.assertEqual(parsed_output,self.golden_parsed_output_with_route)


###################################################
# unit test for show ipv6 route <WROD>
####################################################
class test_show_ipv6_route_word(unittest.TestCase):
    """unit test for show ipv6 route <WORD>"""

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output_with_route = {
    	"total_prefixes": 1,
		"entry": {
		    "2000:2::4:1/128": {
		       "ip": "2000:2::4:1",
		       "type": "type level-2",
		       "distance": "115",
		       "metric": "20",
		       "known_via": "isis",
		       "mask": "128",
		       "paths": {
		            1: {
		                 "age": "2w4d",
		                 "fwd_intf": "Vlan202",
		                 "from": "FE80::EEBD:1DFF:FE09:56C2",
		                 "fwd_ip": "FE80::EEBD:1DFF:FE09:56C2"
		            }
		       },
		       "share_count": "0",
		       "route_count": "1/1"
		    }
		}
    }

    golden_output_with_ipv6_route = {'execute.return_value': '''
        Routing entry for 2000:2::4:1/128
		  Known via "isis", distance 115, metric 20, type level-2
		  Route count is 1/1, share count 0
		  Routing paths:
		    FE80::EEBD:1DFF:FE09:56C2, Vlan202
		      From FE80::EEBD:1DFF:FE09:56C2
		      Last updated 2w4d ago

    '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowIpv6RouteWord(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse(route='2000:2::4:1')

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_with_ipv6_route)
        obj = ShowIpv6RouteWord(device=self.device)
        parsed_output = obj.parse(route='2000:2::4:1')
        self.assertEqual(parsed_output,self.golden_parsed_output_with_route)

if __name__ == '__main__':
    unittest.main()