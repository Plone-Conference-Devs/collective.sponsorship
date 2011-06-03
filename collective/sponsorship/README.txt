.. -*-doctest-*-

============
Sponsorships
============

Start with a portal.

    >>> from collective.sponsorship import testing
    >>> app = testing.SPONSORSHIP_FUNCTIONAL_TESTING['app']
    >>> portal = testing.SPONSORSHIP_FUNCTIONAL_TESTING['portal']

----------------------------
Configure Sponsorship Levels
----------------------------

Open a browser as a user with rights to configure the sponsorship
levels.

    >>> from plone.testing import z2
    >>> admin_browser = z2.Browser(app)
    >>> admin_browser.handleErrors = False
    >>> admin_browser.open(portal.absolute_url())

    >>> admin_browser.getLink('Log in').click()
    >>> admin_browser.getControl('Login Name').value = 'admin'
    >>> admin_browser.getControl('Password').value = 'secret'
    >>> admin_browser.getControl('Log in').click()

The admin can configure the sponsorship levels with the price of the
level and an optional maximum number of sponsorships.  Navigate to the
sponsorship control panel.

    >>> admin_browser.getLink('Site Setup').click()
    >>> admin_browser.getLink('Sponsorship settings').click()

The name and amount sponsorship level fields are required.

TODO    >>> admin_browser.getControl('Add sponsorship level').click()
TODO    >>> admin_browser.getControl('Save').click()
TODO    <...There were some errors...
TODO    ...Name...Required input is missing...
TODO    ...Amount...Required input is missing...

Add the gold sponsorship level limited to 1 sponsorship.

TODO    >>> admin_browser.getControl('Add sponsorship level').click()
TODO    >>> admin_browser.getControl('Name').value = 'Gold'
TODO    >>> admin_browser.getControl('Amount').value = '5000'
TODO    >>> admin_browser.getControl('Number Allowed').value = '1'

    >>> admin_browser.getControl('Sponsorship Levels').value = 'Gold,5000,1'

    >>> admin_browser.getControl('Save').click()
    >>> print admin_browser.contents
    <...Changes saved...
    >>> admin_browser.getLink('Sponsorship settings').click()
    >>> print admin_browser.contents
    <...Gold,5000,1...

Add a silver sponsorship level limited to 2 sponsorships.

TODO    >>> admin_browser.getControl('Add sponsorship level').click()
TODO    >>> admin_browser.getControl('Name').value = 'Silver'
TODO    >>> admin_browser.getControl('Amount').value = '1000'
TODO    >>> admin_browser.getControl('Number Allowed').value = '2'

    >>> admin_browser.getControl(
    ...     'Sponsorship Levels').value += '\nSilver,1000,2'

    >>> admin_browser.getControl('Save').click()
    >>> print admin_browser.contents
    <...Changes saved...
    >>> admin_browser.getLink('Sponsorship settings').click()
    >>> print admin_browser.contents
    <...Gold,5000,1
    Silver,1000,2...

The 'Number Allowed' field is optional.  If left blank then there is
no limit to the number of sponsorships.  Add a bronze sponsorship
level without a limit to the number of sponsorships.

TODO    >>> admin_browser.getControl('Add sponsorship level').click()
TODO    >>> admin_browser.getControl('Name').value = 'Bronze'
TODO    >>> admin_browser.getControl('Amount').value = '200'

    >>> admin_browser.getControl(
    ...     'Sponsorship Levels').value += '\nBronze,200'

    >>> admin_browser.getControl('Save').click()
    >>> print admin_browser.contents
    <...Changes saved...
    >>> admin_browser.getLink('Sponsorship settings').click()
    >>> print admin_browser.contents
    <...Gold,5000,1
    Silver,1000,2
    Bronze,200...

-------------------
Adding Sponsorships
-------------------

Open a browser as a user with rights to add a sponsorship.

    >>> sponsor_browser = z2.Browser(app)
    >>> sponsor_browser.handleErrors = False
    >>> sponsor_browser.open(portal.absolute_url())

    >>> sponsor_browser.getLink('Log in').click()
    >>> sponsor_browser.getControl('Login Name').value = 'test-user'
    >>> sponsor_browser.getControl('Password').value = 'secret'
    >>> sponsor_browser.getControl('Log in').click()

Navigate to the sponsorships folder, just a folder with constrain
types used to limit the allowed types to the sponsorship type, and add
a new gold sponsorship.

    >>> sponsor_browser.getLink('Sponsorships').click()
    >>> sponsor_browser.getLink(
    ...     url="++add++collective.sponsorship.sponsor").click()

The sponsorship object has fields for the sponsor name, sponsorship
level, an image and arbitrary WYSIWYG content.

    >>> sponsor_browser.getControl('Name')
    <Control name='form.widgets.title' type='text'>
    >>> sponsor_browser.getControl('Sponsorship Level')
    <ListControl name='form.widgets.level:list' type='select'>
    >>> sponsor_browser.getControl(name='form.widgets.image')
    <Control name='form.widgets.image' type='file'>
    >>> sponsor_browser.getControl(name='form.widgets.text')
    <Control name='form.widgets.text' type='textarea'>

The sponsorship level field has no default.

    >>> sponsor_browser.getControl('Sponsorship Level').value
    ['--NOVALUE--']

All these fields are required.

    >>> sponsor_browser.getControl('Save').click()
    >>> print sponsor_browser.contents
    <...There were some errors...
    ...Name...Required input is missing...
    ...Sponsorship Level...Required input is missing...
    ...Image...Required input is missing...

TODO    ...Body Text...Required input is missing...

The payment information fields are required.

    TODO

If the payment information is not valid, an error is displayed to the
user.

    TODO

Enter valid values for all the fields and save the sponsorship.

    >>> sponsor_browser.getControl('Name').value = 'Foo Sponsor Title'
    >>> sponsor_browser.getControl(
    ...     'Sponsorship Level').getControl('Gold - $5000').selected = True

    >>> import os
    >>> import cStringIO
    >>> from Products import CMFPlone
    >>> image = open(os.path.join(
    ...     os.path.dirname(CMFPlone.__file__),
    ...     'skins', 'plone_images', 'link_icon.png'))
    >>> sponsor_browser.getControl(name='form.widgets.image').add_file(
    ...     image, 'image/png', 'link_icon.png')

    >>> sponsor_browser.getControl(
    ...     name='form.widgets.text').value = 'Foo Sponsor body text'

    >>> sponsor_browser.getControl('Save').click()
    >>> print sponsor_browser.contents
    <...Item created...
    ...Foo Sponsor Title...
    ...Gold...
    ...Foo Sponsor body text...
    ...link_icon.png...

The gold level fee has been successfully charged using the payment
information when the sponsorship is published.

    >>> from Products.CMFCore.utils import getToolByName
    >>> wftool = getToolByName(portal, 'portal_workflow')

    >>> from Acquisition import aq_parent
    >>> from plone.app import testing
    >>> testing.login(aq_parent(portal), 'admin')
    >>> wftool.doActionFor(
    ...     portal.sponsorships['foo-sponsor-title'], 'publish')
    >>> testing.logout()

    >>> import transaction
    >>> transaction.commit()

    TODO $5000

Add a silver sponsorship.

    >>> sponsor_browser.getLink('Sponsorships').click()
    >>> sponsor_browser.getLink(
    ...     url="++add++collective.sponsorship.sponsor").click()

    >>> sponsor_browser.getControl('Name').value = 'Bar Sponsor Title'

    >>> image = open(os.path.join(
    ...     os.path.dirname(CMFPlone.__file__),
    ...     'skins', 'plone_images', 'event_icon.png'))
    >>> sponsor_browser.getControl(name='form.widgets.image').add_file(
    ...     image, 'image/png', 'event_icon.png')

    >>> sponsor_browser.getControl(
    ...     name='form.widgets.text').value = 'Bar Sponsor body text'

Only the sponsorship levels that have not reached their limit are
selectable on the add form.

    >>> sponsor_browser.getControl(
    ...     'Sponsorship Level').getControl('Gold - $5000')
    Traceback (most recent call last):
    LookupError: label 'Gold - $5000'
    >>> sponsor_browser.getControl(
    ...     'Sponsorship Level').getControl(
    ...         'Silver - $1000').selected = True

Save the new silver level sponsorship.

    >>> sponsor_browser.getControl('Save').click()
    >>> print sponsor_browser.contents
    <...Item created...
    ...Bar Sponsor Title...
    ...Silver...
    ...Bar Sponsor body text...
    ...event_icon.png...

The silver level fee has been successfully charged using the payment
information. 

    >>> testing.login(aq_parent(portal), 'admin')
    >>> wftool.doActionFor(
    ...     portal.sponsorships['bar-sponsor-title'], 'publish')
    >>> testing.logout()

    >>> transaction.commit()

    TODO $1000

Attempt to add another silver level sponsorship.

    >>> sponsor_browser.getLink('Sponsorships').click()
    >>> sponsor_browser.getLink(
    ...     url="++add++collective.sponsorship.sponsor").click()

    >>> sponsor_browser.getControl('Name').value = 'Qux Sponsor Title'

    >>> image = open(os.path.join(
    ...     os.path.dirname(CMFPlone.__file__),
    ...     'skins', 'plone_images', 'file_icon.png'))
    >>> sponsor_browser.getControl(name='form.widgets.image').add_file(
    ...     image, 'image/png', 'file_icon.png')

    >>> sponsor_browser.getControl(
    ...     name='form.widgets.text').value = 'Qux Sponsor body text'

The silver level sponsorship is still available since there is one
more sponsorship available at that level.

    >>> sponsor_browser.getControl(
    ...     'Sponsorship Level').getControl('Gold - $5000')
    Traceback (most recent call last):
    LookupError: label 'Gold - $5000'
    >>> sponsor_browser.getControl(
    ...     'Sponsorship Level').getControl(
    ...         'Silver - $1000').selected = True

Add another silver sponsorship in the meantime, exhausting the silver
sponsorships available.

    >>> testing.login(aq_parent(portal), 'admin')
    >>> portal.sponsorships.invokeFactory(
    ...     type_name='collective.sponsorship.sponsor',
    ...     id='baz-sponsor-title',
    ...     title='Baz Sponsor Title',
    ...     level=1)
    'baz-sponsor-title'
    >>> wftool.doActionFor(
    ...     portal.sponsorships['baz-sponsor-title'], 'publish')
    >>> testing.logout()

    >>> transaction.commit()

Attempt to save the silver sponsorship in progress.  A validation
error is displayed to the user indicating the the silver level is no
longer available.

TODO    >>> sponsor_browser.getControl('Save').click()
TODO    >>> print sponsor_browser.contents
TODO    <...There were some errors...
TODO    ...Sponsorship Level is invalid, please correct...

Successfully save the new sponsorship as a bronze sponsorship.

    >>> sponsor_browser.getControl(
    ...     'Sponsorship Level').getControl('Gold - $5000')
    Traceback (most recent call last):
    LookupError: label 'Gold - $5000'
    
TODO    >>> sponsor_browser.getControl(
TODO    ...     'Sponsorship Level').getControl('Silver - $1000')
TODO    Traceback (most recent call last):
TODO    LookupError: label 'Silver - $1000'

    >>> sponsor_browser.getControl(
    ...     'Sponsorship Level').getControl(
    ...         'Bronze - $200').selected = True

    >>> sponsor_browser.getControl('Save').click()
    >>> print sponsor_browser.contents
    <...Item created...
    ...Qux Sponsor Title...
    ...Bronze...
    ...Qux Sponsor body text...
    ...file_icon.png...

The bronze level fee has been successfully charged using the payment
information.

    >>> testing.login(aq_parent(portal), 'admin')
    >>> wftool.doActionFor(
    ...     portal.sponsorships['qux-sponsor-title'], 'publish')
    >>> testing.logout()

    >>> transaction.commit()

    TODO $200

Add 2 more bronze sponsorships then add another sponsorship using the
form, demonstrating there is no limit.

    >>> testing.login(aq_parent(portal), 'admin')
    >>> portal.sponsorships.invokeFactory(
    ...     type_name='collective.sponsorship.sponsor',
    ...     id='bah-sponsor-title',
    ...     title='Bah Sponsor Title',
    ...     level=2)
    'bah-sponsor-title'
    >>> wftool.doActionFor(
    ...     portal.sponsorships['bah-sponsor-title'], 'publish')

    >>> portal.sponsorships.invokeFactory(
    ...     type_name='collective.sponsorship.sponsor',
    ...     id='quux-sponsor-title',
    ...     title='Quux Sponsor Title',
    ...     level=2)
    'quux-sponsor-title'
    >>> wftool.doActionFor(
    ...     portal.sponsorships['quux-sponsor-title'], 'publish')
    >>> testing.logout()

    >>> transaction.commit()

    >>> sponsor_browser.getLink('Sponsorships').click()
    >>> sponsor_browser.getLink(
    ...     url="++add++collective.sponsorship.sponsor").click()

    >>> sponsor_browser.getControl('Name').value = 'Blah Sponsor Title'

    >>> image = open(os.path.join(
    ...     os.path.dirname(CMFPlone.__file__),
    ...     'skins', 'plone_images', 'file_icon.png'))
    >>> sponsor_browser.getControl(name='form.widgets.image').add_file(
    ...     image, 'image/png', 'file_icon.png')

    >>> sponsor_browser.getControl(
    ...     name='form.widgets.text').value = 'Blah Sponsor body text'

    >>> sponsor_browser.getControl(
    ...     'Sponsorship Level').getControl('Gold - $5000')
    Traceback (most recent call last):
    LookupError: label 'Gold - $5000'
    >>> sponsor_browser.getControl(
    ...     'Sponsorship Level').getControl('Silver - $1000')
    Traceback (most recent call last):
    LookupError: label 'Silver - $1000'
    >>> sponsor_browser.getControl(
    ...     'Sponsorship Level').getControl(
    ...         'Bronze - $200').selected = True

    >>> sponsor_browser.getControl('Save').click()
    >>> print sponsor_browser.contents
    <...Item created...
    ...Blah Sponsor Title...
    ...Bronze...
    ...Blah Sponsor body text...
    ...file_icon.png...

    >>> testing.login(aq_parent(portal), 'admin')
    >>> wftool.doActionFor(
    ...     portal.sponsorships['blah-sponsor-title'], 'publish')
    >>> testing.logout()

    >>> transaction.commit()

--------------------
Sponsorships Viewlet
--------------------

A viewlet is provided which lists all the sponsorships sorted and
grouped by level.

Open a browser as an anonymous user.

    >>> anon_browser = z2.Browser(app)
    >>> anon_browser.handleErrors = False

Now the viewlet shows all levels and sponsorships.

    >>> anon_browser.open(portal.absolute_url())
    >>> print anon_browser.contents
    <...
    <div id="sponsorships">
      <h2>Sponsorships</h2>
      <dl id="sponsorship-level-0">
        <dt>Gold</dt>
        <dd><dl>
          <dt>
            <a
            href="http://nohost/plone/sponsorships/foo-sponsor-title">Foo
            Sponsor Title</a>
          </dt>
          <dd>
            <a
            href="http://nohost/plone/sponsorships/foo-sponsor-title">
            <img alt="Foo Sponsor Title"
            src="http://nohost/plone/sponsorships/foo-sponsor-title/@@download/image"
            />
            </a>
          </dd>
        </dl></dd>
      </dl>
      <dl id="sponsorship-level-1">
        <dt>Silver</dt>
        <dd><dl>
          <dt>
            <a
            href="http://nohost/plone/sponsorships/bar-sponsor-title">Bar
            Sponsor Title</a>
          </dt>
          <dd>
            <a
            href="http://nohost/plone/sponsorships/bar-sponsor-title">
            <img alt="Bar Sponsor Title"
            src="http://nohost/plone/sponsorships/bar-sponsor-title/@@download/image"
            />
            </a>
          </dd>
          <dt>
            <a
            href="http://nohost/plone/sponsorships/baz-sponsor-title">Baz
            Sponsor Title</a>
          </dt>
          <dd>
            <a
            href="http://nohost/plone/sponsorships/baz-sponsor-title">
            <img alt="Baz Sponsor Title"
            src="http://nohost/plone/sponsorships/baz-sponsor-title/@@download/image"
            />
            </a>
          </dd>
        </dl></dd>
      </dl>
      <dl id="sponsorship-level-2">
        <dt>Bronze</dt>
        <dd><dl>
          <dt>
            <a
            href="http://nohost/plone/sponsorships/qux-sponsor-title">Qux
            Sponsor Title</a>
          </dt>
          <dd>
            <a
            href="http://nohost/plone/sponsorships/qux-sponsor-title">
            <img alt="Qux Sponsor Title"
            src="http://nohost/plone/sponsorships/qux-sponsor-title/@@download/image"
            />
            </a>
          </dd>
          <dt>
            <a
            href="http://nohost/plone/sponsorships/bah-sponsor-title">Bah
            Sponsor Title</a>
          </dt>
          <dd>
            <a
            href="http://nohost/plone/sponsorships/bah-sponsor-title">
            <img alt="Bah Sponsor Title"
            src="http://nohost/plone/sponsorships/bah-sponsor-title/@@download/image"
            />
            </a>
          </dd>
          <dt>
            <a
            href="http://nohost/plone/sponsorships/quux-sponsor-title">Quux
            Sponsor Title</a>
          </dt>
          <dd>
            <a
            href="http://nohost/plone/sponsorships/quux-sponsor-title">
            <img alt="Quux Sponsor Title"
            src="http://nohost/plone/sponsorships/quux-sponsor-title/@@download/image"
            />
            </a>
          </dd>
          <dt>
            <a
            href="http://nohost/plone/sponsorships/blah-sponsor-title">Blah
            Sponsor Title</a>
          </dt>
          <dd>
            <a
            href="http://nohost/plone/sponsorships/blah-sponsor-title">
            <img alt="Blah Sponsor Title"
            src="http://nohost/plone/sponsorships/blah-sponsor-title/@@download/image"
            />
            </a>
          </dd>
        </dl></dd>
      </dl>
    </div>...

The viewlet only lists the levels with sponsorships which have been
published.  Retract all but one silver sponsorship.

    >>> testing.login(aq_parent(portal), 'admin')
    >>> for sponsorship in portal.sponsorships.contentValues():
    ...     if sponsorship.getId() == 'bar-sponsor-title':
    ...         continue
    ...     wftool.doActionFor(sponsorship, 'retract')
    >>> testing.logout()

    >>> transaction.commit()

Now the viewlet shows one level and one sponsorship.

    >>> anon_browser.open(portal.absolute_url())
    >>> print anon_browser.contents
    <...
    <div id="sponsorships">
      <h2>Sponsorships</h2>
      <dl id="sponsorship-level-1">
        <dt>Silver</dt>
        <dd><dl>
          <dt>
            <a
            href="http://nohost/plone/sponsorships/bar-sponsor-title">Bar
            Sponsor Title</a>
          </dt>
          <dd>
            <a
            href="http://nohost/plone/sponsorships/bar-sponsor-title">
            <img alt="Bar Sponsor Title"
            src="http://nohost/plone/sponsorships/bar-sponsor-title/@@download/image"
            />
            </a>
          </dd>
        </dl></dd>
      </dl>
    </div>...

If no sponsorships have been published yet, the viewlet lists doesn't
list any sponsorships or levels.

    >>> testing.login(aq_parent(portal), 'admin')
    >>> wftool.doActionFor(
    ...     portal.sponsorships['bar-sponsor-title'], 'retract')
    >>> testing.logout()

    >>> transaction.commit()

    >>> anon_browser.open(portal.absolute_url())
    >>> print anon_browser.contents
    <...
    <div id="sponsorships">
    </div>...
