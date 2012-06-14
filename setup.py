from distutils.core import setup

setup(
    name = "mallory",
    version = "0.0.1",
    packages = ["mallory"],
    author = "Braintree",
    author_email = "code@braintreepayments.com",
    url = "https://github.com/braintree/mallory",
    license = "MIT",
    long_description = "Man-in-the-middle for fun and profit",
    install_requires = ["tornado>=2.3"]
)
