import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='BekiDash',
    version='0.0.1',
    author='Klajdi Beqiraj',
    author_email='klajdi.beqiraj@numerical.it',
    description='Testing installation of Package',
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url='https://github.com/KlajdiBeqiraj/BekiDash.git',
    license='MIT',
    packages=['BekiDash'],
    install_requires=['jupyter_dash', 'plotly', 'matplotlib', 'numpy', 'pandas', 'dash'],
)