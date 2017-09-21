from boto3 import session as boto3_session


def get_session(account, region):
    return boto3_session.Session(region_name=region, **account)


__all__ = ['get_session']
