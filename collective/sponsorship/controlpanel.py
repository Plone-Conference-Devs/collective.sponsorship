from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from plone.z3cform import layout

from collective.sponsorship import interfaces


class SponsorshipControlPanelForm(RegistryEditForm):
    schema = interfaces.ISponsorshipSettings

SponsorshipControlPanelView = layout.wrap_form(
    SponsorshipControlPanelForm, ControlPanelFormWrapper)
SponsorshipControlPanelView.label = u"Sponsorship settings"
