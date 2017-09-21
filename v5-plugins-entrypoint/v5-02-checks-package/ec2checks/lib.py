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
from botocore.exceptions import ClientError
import re

SUBNET_ID = re.compile("'(?P<subnet_id>subnet-.+)'")


def check_subnets(session, elb):
    ec2 = session.client('ec2')
    subnets = elb['Subnets']
    name = elb['LoadBalancerName']
    status = 'OK'
    try:
        ec2.describe_subnets(SubnetIds=subnets)
    except ClientError as error:
        status = 'NOK'
        if error.response['Error']['Code'] == 'InvalidSubnetID.NotFound':
            message = error.response['Error']['Message']
            result = SUBNET_ID.search(message)
            if result:
                subnet_id = result.groupdict(default={}).get('subnet_id', 'NOTSET')
                status += f' - ({subnet_id})'

    return name, status


def check_instances(session, elb):
    name = elb['LoadBalancerName']
    instances = elb['Instances']
    status = 'NOK' if len(instances) == 0 else 'OK'
    return name, status
