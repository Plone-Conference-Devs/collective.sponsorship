from setuptools import setup, find_packages
import os

version = '1.0'

test_require = ['plone.app.testing']

setup(name='collective.sponsorship',
      version=version,
      description="Plone Conference Registration System",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='https://github.com/Plone-Conference-Devs/collective.sponsorship',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Plone',
          'plone.app.dexterity',
          'plone.app.registry',
          'collective.autopermission',
          'plone.namedfile [blobs]',
      ],
      test_require=test_require,
      extras_require={'test': test_require},
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=[],
      paster_plugins=[],
      )
