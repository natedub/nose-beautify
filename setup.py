from setuptools import setup, find_packages

setup(
    name='nose-beautify',
    version='0.5.0',
    description='Colorize your test results with Pygments for readable tracebacks and SQLAlchemy queries.',
    author='Nathan Wright',
    author_email='thatnateguy@gmail.com',
    url='http://github.com/natedub/nose-beautify',
    license='GNU LGPL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],

    install_requires=[
        'Pygments',
    ],

    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    package_data={'mediacore': ['i18n/*/LC_MESSAGES/*.mo']},
    zip_safe=False,

    entry_points="""
    [nose.plugins.0.10]
    beautify = nosebeautify.plugin:BeautifyPlugin
    """,
)
