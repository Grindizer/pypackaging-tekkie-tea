import sys
from .runner import check_elb
from .connection import get_session
import optparse


def get_parser():
    parser = optparse.OptionParser(description='Smoke tests for aws elb', prog='checker', epilog='')
    parser.add_option('--regions', '-r', action='append', type='string', default=[], help='region list to run '
                                                                                          'the checks')
    return parser


def main(args=sys.argv):
    parser = get_parser()
    opts, args = parser.parse_args(args)
    for region in opts.regions:
        session = get_session({}, region)
        print(f'{"region":10}{"elb":30}{"check":20}{"status":6}')
        print('-' * 66)
        for check_name, elb_name, status in check_elb(session):
            print(f'{region:10}{elb_name:30}{check_name:20}{status:6}')
        print('-' * 66)


if __name__ == '__main__':
    sys.exit(main())
