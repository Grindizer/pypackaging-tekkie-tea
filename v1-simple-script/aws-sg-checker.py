from boto3 import session as boto3_session
import sys


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


def check_elb_cross_zone_attr(client, elb_name):
    attr = client.describe_load_balancer_attributes(LoadBalancerName=elb_name)
    attr = attr.pop('LoadBalancerAttributes').pop('CrossZoneLoadBalancing').pop('Enabled')
    return attr


def main():
    client_elb = get_client('elb', get_session({}, 'eu-west-1'))
    for elb in list_load_balancer(client_elb):
        elb_name = elb['LoadBalancerName']
        check = check_elb_cross_zone_attr(client_elb, elb_name)
        print(f'{elb_name} -> {"OK" if check else "NOK"}')

if __name__ == '__main__':
    sys.exit(main())
