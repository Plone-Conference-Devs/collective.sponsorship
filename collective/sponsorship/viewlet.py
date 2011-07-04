from plone.app.layout.viewlets.common import ViewletBase
from collective.sponsorship import interfaces
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from collective.sponsorship import sponsors


class SponsorsViewlet(ViewletBase):

    def render(self):
        return self.index()
    
    def update(self):
        super(SponsorsViewlet, self).update()
        self.levels = []
        
        site = getSite()
        if site.get('sponsorships'):
            source = interfaces.SimpleVocabulary(self.context.sponsorships)
            self.levels.extend(
                term for term in source._terms
                if getattr(term, 'sponsors', ()))
                
    def getSponsors(self, minimumDonation=None):
        return sponsors.getSponsors(minimumDonation)
        
