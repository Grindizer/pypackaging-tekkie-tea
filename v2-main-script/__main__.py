import sys

# - dynamically insert the dependency directory -
# from os.path import dirname, join as pjoin
# from os import getcwd
#
# here = getcwd()
# sys.path.insert(0, pjoin(here, 'deps'))
# --

# - distribute this script as a single file -
# $ mkdir dist && cd dist
# $ python -m zipfile -c elb-cross-az-check.zip ../__main__.py
# Python can run the zip file.
# $ python elb-cross-az-check.zip
# OR
# $ echo '#!/usr/bin/env python' > check
# $ cat elb-cross-az-check.zip >> check
# $ chmod a+x check
# executable archive.
# $ ./check
# Add boto3 dependencies.
# $ pip install -t deps boto3
#

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


def check_elb_cross_zone_attr(client, elb_name):
    attr = client.describe_load_balancer_attributes(LoadBalancerName=elb_name)
    attr = attr.pop('LoadBalancerAttributes').pop('CrossZoneLoadBalancing').pop('Enabled')
    return attr


def main():
    client_elb = get_client('elb', get_session({}, 'eu-west-1'))
    for elb in list_load_balancer(client_elb):
        elb_name = elb['LoadBalancerName']
        check = check_elb_cross_zone_attr(client_elb, elb_name)
        status = "OK" if check else "NOK"
        print('{} -> {}'.format(elb_name, status))

if __name__ == '__main__':
    sys.exit(main())

