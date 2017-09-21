
def iter_elb(session):
    client = session.client('elb')
    paginator = client.get_paginator('describe_load_balancers')
    pages = paginator.paginate(PaginationConfig={'PageSize': 5})
    for page in pages:
        for elb in page.pop('LoadBalancerDescriptions'):
            yield elb

