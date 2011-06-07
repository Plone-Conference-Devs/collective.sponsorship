from plone.app import testing

from Acquisition import aq_parent

from Products.CMFCore.utils import getToolByName

class PloneFixture(testing.PloneSandboxLayer):
    """A fixture which just loads the package code."""
    defaultBases = (testing.PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.sponsorship
        self.loadZCML(package=collective.sponsorship)

PLONE_FIXTURE = PloneFixture()
PLONE_FUNCTIONAL_TESTING = testing.FunctionalTesting(
    bases=(PLONE_FIXTURE,), name="SponsorshipPlone:Functional")


class SponsorshipFixture(testing.PloneSandboxLayer):
    """A fixture which installs the profile."""
    defaultBases = (PLONE_FIXTURE,)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(
            portal, 'collective.sponsorship:default')

        testing.login(aq_parent(portal), 'admin')
        wftool = getToolByName(portal, 'portal_workflow')
        wftool.setDefaultChain('simple_publication_workflow')
        wftool.doActionFor(portal.sponsorships, 'publish')
        testing.logout()

        portal.manage_setLocalRoles('AuthenticatedUsers', ('Contributor',))

SPONSORSHIP_FIXTURE = SponsorshipFixture()
SPONSORSHIP_FUNCTIONAL_TESTING = testing.FunctionalTesting(
    bases=(SPONSORSHIP_FIXTURE,), name="Sponsorship:Functional")
