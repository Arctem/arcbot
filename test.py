import sys

import tests.test_sql
import tests.test_mangle
import tests.test_phrases

TEST_OPTIONS = {
    'sql' : tests.test_sql,
    'mangle' : tests.test_mangle,
    'phrases' : tests.test_phrases,
}

def main(args = []):
    print(args)
    if len(args) == 0 or 'all' in args:
        args = TEST_OPTIONS.keys()
    for test in args:
        TEST_OPTIONS[test].run()


if __name__ == '__main__':
    print(sys.argv)
    sys.exit(main(sys.argv[1:]))
