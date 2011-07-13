from zope.interface import Interface
from zope import interface
from zope import schema
from zope.schema import interfaces
from zope.schema import vocabulary
from zope.component import getUtility

from z3c.form.browser import select

from plone.directives import form
from plone.app.textfield import RichText
from plone.namedfile import field
from plone.registry.interfaces import IRegistry
from plone.registry import field as reg_field

from Products.CMFCore.utils import getToolByName


class IManageSponsorhips(Interface):
    """
    View to see all sponsorship details
    """
    

class IListSponsorhips(Interface):
    """
    List all sponsorships - for the end user/marketing
    """


class SimpleVocabulary(vocabulary.SimpleVocabulary):

    def __init__(self, context):
        # Retrieve the control panel setting
        registry = getUtility(IRegistry)
        setting = registry[
            ISponsorshipSettings.__identifier__+'.levels'] or ()

        # Assemble the terms and add attributes for the amount and
        # optionally the maximum
        terms = []
        for idx, level in enumerate(setting):
            if not level: # no levels configured
                continue
            level = level.split(',')
            if len(level) < 3: # improperly configured
                continue
            name = level[0]
            amount = int(level[1])
            term = vocabulary.SimpleTerm(
                idx, title=u'%s - $%s' % (name, amount))
            term.name = name
            term.amount = amount
            if len(level) == 3:
                term.maximum = int(level[2])
            terms.append(term)

        # Let the vocabulary finish assembly, including the by_value
        # mapping we need below for getTerm()
        super(SimpleVocabulary, self).__init__(terms)

        # Collect and count the sponsors for each level
        self.counts = counts = {}
        catalog = getToolByName(context, 'portal_catalog')
        for brain in catalog(
            path='/'.join(context.getPhysicalPath()),
            portal_type='collective.sponsorship.sponsor',
            review_state='published',
            sort_on='getObjPositionInParent'):
            sponsor = brain.getObject()
            idx = sponsor.level
            # XXX: I am not 100% whats going on here but if there 
            # is no level then this block needs an if and it works
            if idx: 
                term = self.getTerm(idx)
                if not hasattr(term, 'sponsors'):
                    term.sponsors = []
                term.sponsors.append(sponsor)
                if hasattr(term, 'maximum'):
                    count = counts.get(idx, 0) + 1
                    counts[idx] = count

    def __iter__(self):
        """Skip levels whose max has been reached."""
        for idx, term in enumerate(
            super(SimpleVocabulary, self).__iter__()):
            term = self.getTerm(idx)
            if (not hasattr(term, 'maximum') or
                self.counts.get(idx, 0) < term.maximum):
                yield term
            

class LevelsSourceBinder(object):
    interface.implements(interfaces.IContextSourceBinder)

    def __call__(self, context):
        return SimpleVocabulary(context)


class ISponsorshipLevel(Interface):

    name = schema.TextLine(
        title=u'Name')
    amount = schema.Int(
        title=u'Amount')
    maximum = schema.Int(
        title=u'Number Allowed')    
    

class ISponsorshipSettings(Interface):

    levels = schema.Tuple(
        title=u'Sponsorship Levels',
        value_type=reg_field.TextLine(
            # TODO schema=ISponsorshipLevel,
            title=u'Sponsorship Level',
            description=u'Name,amount,max'))


def PromptSelectFieldWidget(field, request):
    widget = select.SelectWidget(request)
    widget.prompt = True
    widget.promptMessage = u'Please select a sponsorship level ...'
    return select.FieldWidget(field, widget)


class ISponsor(form.Schema):
    # TODO: Want to hide on display only
    #form.mode(level='hidden', url='hidden')
    
    title = schema.TextLine(
        title=u'Name')

    form.widget(level=PromptSelectFieldWidget)
    level = schema.Choice(
        title=u'Sponsorship Level',
        required=False,
        source=LevelsSourceBinder())

    url = schema.URI(
        title=u'Link to company/personal website',
        required=False,
        )
    
    text = RichText(
        title=u'About',
        description=u'Information about this donation.',
        required=False,
        )
    
    amount = schema.Int(
        title=u'Donation Amount',
        required = False,
        )
        
    image = field.NamedBlobImage(
        title=u'Image',
        required=False, # some people are just people
        )
