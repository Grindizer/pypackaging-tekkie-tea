from boto3 import session as boto3_session


def get_session(account, region):
    return boto3_session.Session(region_name=region, **account)


def get_client(service, session):
    return session.client(service)


def list_load_balancer(client):
    paginator = client.get_paginator('describe_load_balancers')
    pages = paginator.paginate(PaginationConfig={'PageSize': 5})
    for page in pages:
        for elb in page.pop('LoadBalancerDescriptions'):
            yield elb


checks = {}


def get_elb_cross_zone_attr(client, elb_name):
    attr = client.describe_load_balancer_attributes(LoadBalancerName=elb_name)
    attr = attr.pop('LoadBalancerAttributes').pop('CrossZoneLoadBalancing').pop('Enabled')
    return attr


def check_elb_cross_zone(client, elb):
    name = elb['LoadBalancerName']
    enabled = get_elb_cross_zone_attr(client, name)
    status = "OK" if enabled else "NOK"
    return name, status


checks['cross_zone'] = check_elb_cross_zone


def check_elb_azs(client, elb):
    zones = elb['AvailabilityZones']
    name = elb['LoadBalancerName']
    status = "OK" if len(zones) > 1 else "NOK"
    return name, status


checks['azs'] = check_elb_azs


def check_elb(region):
    session = get_session({}, region)
    client = get_client('elb', session)
    for elb in list_load_balancer(client):
        for check_name, check in checks.items():
            name, status = check(client, elb)
            yield (check_name, name, status)
