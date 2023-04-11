import os
import re

from setuptools import setup

HERE = os.path.dirname(os.path.abspath(__file__))


def get_version():
    filename = os.path.join(HERE, 'flask_firebaseauth.py')
    contents = open(filename).read()
    pattern = r"^__version__ = '(.*?)'$"
    return re.search(pattern, contents, re.MULTILINE).group(1)


setup(
    name='Flask-FirebaseAuth',
    version=get_version(),
    url='https://github.com/vsheffer/flask-firebaseauth',
    license='MIT',
    author='Vincent Sheffer',
    author_email='vincent.sheffer@gmail.com',
    description='HTTP bearer token authentication using Firebase Auth accessToken.',
    long_description=(
        open('README.md').read() + '\n\n' +
        open('CHANGES.md').read()
    ),
    py_modules=['flask_firebaseauth'],
    zip_safe=False,
    python_requires='>=3.7',
    include_package_data=True,
    platforms='any',
#    install_requires=['Flask'],
    test_suite='test_firebaseauth.suite',
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
