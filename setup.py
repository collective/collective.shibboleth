from setuptools import setup, find_packages

version = '1.3'

long_description = (
    open('README.rst').read()
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(name='collective.shibboleth',
      version=version,
      description="Authentication integration layer for Shibboleth's "
                  "Embdedded Discovery Service (EDS) and Plone",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Environment :: Web Environment",
          "Operating System :: OS Independent",
          "Framework :: Zope2",
          "Framework :: Plone",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='plone discovery service shibboleth authentication',
      author='David Beitey',
      author_email='david@davidjb.com',
      url='https://github.com/collective/collective.shibboleth',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective', ],
      include_package_data=True,
      zip_safe=False,
      setup_requires=['setuptools-git'],
      install_requires=[
          'setuptools',
          'collective.monkeypatcher',
          'collective.pluggablelogin>=1.1',
          'Products.AutoUserMakerPASPlugin>=1.0dev',
          'zope.formlib',
          # -*- Extra requirements: -*-
      ],
      extras_require={'test':
        [
            'plone.app.testing',
            'Products.PloneTestCase'
        ]
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """
      )
