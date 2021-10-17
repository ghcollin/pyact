from setuptools import setup

setup(
    name='pyact',
    version='0.9.0',
    url='https://github.com/ghcollin/pyact',
    description='Create and run a React app directly in Python from a Python server.',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords='react python material-ui antd',
    license='MIT',
    author='ghcollin',
    author_email='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=['pyact'],
    install_requires=['starlette']
)