from setuptools import setup, find_packages

setup(
    name='nose-beautify',
    version='0.1.0',
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
        'fancyformatter',
        'pygments-pprint-sql',
    ],

    packages=find_packages(),

    entry_points="""
    [nose.plugins.0.10]
    beautify = nosebeautify.plugin:BeautifyPlugin
    """,
)
