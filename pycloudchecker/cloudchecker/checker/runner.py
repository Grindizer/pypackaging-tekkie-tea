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
    client = session.client('elb')
    for elb in list_load_balancer(client):
        for check_name, check in list_elb_checks():
            name, status = check(session, elb)
            yield (check_name, name, status)


__all__ = ['check_elb']
