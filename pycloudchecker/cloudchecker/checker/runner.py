from pkg_resources import iter_entry_points


def iter_checks():
    for entry in iter_entry_points('cloudchecker.checks'):
        try:
            check = entry.resolve()
        except Exception as error:
            # error loading check entrypoint !
            # for now just ignore the entrypoint.
            pass
        else:
            yield entry.name, check


def run_checker(session):
    """
    Perform all elb checks on all elbs for a given region.
    :param session: boto3 session.
    :return: generator that yield the results as a tuple (<name of the check>, <elb name>, <check result>)
    """
    client = session.client('elb')
    for elb in list_load_balancer(client):
        for check_name, check in list_elb_checks():
            name, status = check(session, elb)
            yield (check_name, name, status)


__all__ = ['check_elb']
