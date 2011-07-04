from Products.Five import BrowserView
from collective.sponsorship.interfaces import IManageSponsorhips
from zope.interface import implements
from collective.sponsorship import sponsors


class ManageSponsorships(BrowserView):
    implements(IManageSponsorhips)
    
    def render(self):
        return self.index()
        
    def getAllSponsors(self):
        return sponsors.getSponsors(minimumDonation=None)
        
        
