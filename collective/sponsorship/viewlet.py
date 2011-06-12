from plone.app.layout.viewlets.common import ViewletBase

from collective.sponsorship import interfaces


class SponsorsViewlet(ViewletBase):

    def update(self):
        super(SponsorsViewlet, self).update()
        source = interfaces.SimpleVocabulary(self.context.sponsorships)
        self.levels = [
            term for term in source._terms
            if getattr(term, 'sponsors', ())]
        
