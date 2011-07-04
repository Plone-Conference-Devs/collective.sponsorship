from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName


def getSponsors(minimumDonation=None):
    """
    Return Sponsors that have qualified for logo on the site.
    Pass in a minimum sponsorship amount to limit to those that 
    have a minimum donation. (int)
    """
    context = getSite()
    catalog = getToolByName(context, 'portal_catalog')
    queryFilter = {'portal_type': 'collective.sponsorship.sponsor', 
                                    'review_state': 'published',
                                    'sort_on':'getSponsorshipAmount',
                                    'sort_order':'descending',
                                    }
    if minimumDonation:
        queryFilter['getSponsorshipAmount'] = {'query':minimumDonation,
                                                'range':'min'}
    results = catalog.searchResults(queryFilter)
    return results