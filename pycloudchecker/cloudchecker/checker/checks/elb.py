# -- example elb content --
# { 'AvailabilityZones': ['eu-west-1b', 'eu-west-1c', 'eu-west-1a'],
#   'BackendServerDescriptions': [],
#   'CanonicalHostedZoneName': 'test-opsworks-1329544464.eu-west-1.elb.amazonaws.com',
#   'CanonicalHostedZoneNameID': 'Z32O12XQLNTSW2',
#   'CreatedTime': datetime.datetime(2017, 1, 9, 15, 32, 5, 280000, tzinfo=tzutc()),
#   'DNSName': 'test-opsworks-1329544464.eu-west-1.elb.amazonaws.com',
#   'HealthCheck': {'HealthyThreshold': 10, 'Interval': 30, 'Target': 'HTTP:80/', 'Timeout': 5, 'UnhealthyThreshold': 2},
#   'Instances': [],
#   'ListenerDescriptions': [{'Listener': {'InstancePort': 80, 'InstanceProtocol': 'HTTP', 'LoadBalancerPort': 80, 'Protocol': 'HTTP'}, 'PolicyNames': []}],
#   'LoadBalancerName': 'test-opsworks',
#   'Policies': {'AppCookieStickinessPolicies': [], 'LBCookieStickinessPolicies': [], 'OtherPolicies': []},
#   'Scheme': 'internet-facing',
#   'SecurityGroups': ['sg-bae2ecdf'],
#   'SourceSecurityGroup': {'GroupName': 'default', 'OwnerAlias': '580501780015'},
#   'Subnets': ['subnet-1d8f3744', 'subnet-db5d3bac', 'subnet-eeb1cf8b'],
#   'VPCId': 'vpc-4ce06d29'
# }


def get_elb_cross_zone_attr(session, elb_name):
    client = session.client('elb')
    attr = client.describe_load_balancer_attributes(LoadBalancerName=elb_name)
    attr = attr.pop('LoadBalancerAttributes').pop('CrossZoneLoadBalancing').pop('Enabled')
    return attr


def check_elb_cross_zone(session, elb):
    """
    Check if the elb has the cross az option active.
    :param session: boto3 session.
    :param elb: elb information as return by describe elb call.
    :return: typle (name, result) name is the elb name being checked, and result is True/False
        i.e success/failed the check
    """
    name = elb['LoadBalancerName']
    enabled = get_elb_cross_zone_attr(session, name)
    status = "OK" if enabled else "NOK"
    return name, status


def check_elb_azs(session, elb):
    """
    Check that the elb has at least 2 availability zone setup.
    :param session: boto3 session
    :param elb: elb information as return by describe elb call.
    :return: typle (name, result) name is the elb name being checked, and result is True/False
        i.e success/failed the check
    """
    zones = elb['AvailabilityZones']
    name = elb['LoadBalancerName']
    status = "OK" if len(zones) > 1 else "NOK"
    return name, status


__all__ = ['check_elb_cross_zone', 'check_elb_azs']
