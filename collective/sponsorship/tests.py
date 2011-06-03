import unittest2 as unittest
import doctest

from collective.sponsorship import testing

optionflags = (doctest.NORMALIZE_WHITESPACE |
               doctest.ELLIPSIS |
               doctest.REPORT_NDIFF)


def test_suite():
    install_suite = doctest.DocFileSuite(
        'README.txt',
        optionflags=optionflags)
    install_suite.layer = testing.SPONSORSHIP_FUNCTIONAL_TESTING
    return unittest.TestSuite([install_suite])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
