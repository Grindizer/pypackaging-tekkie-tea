import sys
from . lib import check_elb
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
        for check_name, name, status in check_elb(region):
            print('{} :: {} :: {} -> {}'.format(region, name, check_name, status))


if __name__ == '__main__':
    sys.exit(main())
