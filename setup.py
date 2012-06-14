from distutils.core import setup

setup(
    name = "mallory",
    version = "0.0.1",
    long_description = "Reverse proxy with SSL verification",
    url = "https://github.com/braintree/mallory",
    author = "Braintree",
    author_email = "code@braintreepayments.com",
    license = "MIT",

    packages = ["mallory"],
    scripts = ["bin/mallory"],
    install_requires = ["tornado>=2.3"]
)
