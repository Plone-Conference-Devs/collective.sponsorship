from Products.Five import BrowserView
from collective.sponsorship.interfaces import IListSponsorhips
from zope.interface import implements
from collective.sponsorship import sponsors


class ListSponsorships(BrowserView):
    implements(IListSponsorhips)
    
    def render(self):
        return self.index()
        
    def getAllSponsors(self):
        return sponsors.getSponsors(minimumDonation=None)
        
        
