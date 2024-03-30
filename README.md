# Spritmonitor API sample code

This repository contains sample code for the Spritmonitor API endpoints.
Individual API features have folders where you can find examples of usage.

* [Spritmonitor API documentation](https://api.spritmonitor.de/doc)

## Prerequisites

* User account on Spritmonitor ([Sign up here](https://www.spritmonitor.de/en/register.html))

## Using the code samples

In order to run the samples in this repository you will need to setup some environment variables. You can create a new access bearer token on the [Spritmonitor Password Page](https://www.spritmonitor.de/en/my_account/change_password.html). The app token can be requested by the Spritmonitor support on the [Spritmonitor Contact Page](https://www.spritmonitor.de/en/contact.html).


```bash
export BEARER_TOKEN='<your_bearer_token>'
export APP_TOKEN='<your_app_token>'
```

Be sure to replace  `<your_bearer_token>` with your own bearer token without the `< >`. The same applies for the app token.

## Python environment setup

You will need to have Python 3 installed to run this code samples. The Python samples use the `requests` package.

(Optionally) It is common and recommended not to install required packages globally, but locally under a project subfolder using `venv`.

```bash
python3 -m venv venv
source venv/bin/activate
```

You can install the package as follows:

```bash
pip install requests
```

## Support

* For general questions related to the Spritmonitor API, please contact the Spritmonitor support via the [Spritmonitor Contact Page](https://www.spritmonitor.de/en/contact.html).
* If there's an bug or issue with the sample code itself, please create a [new issue](https://github.com/FundF/Spritmonitor-API-sample-code/issues) here on GitHub.

## Contributing

We welcome pull requests that add meaningful additions to these code samples.

## Copyright

Copyright 2024 Fisch und Fischl GmbH

Licensed under the Apache License, Version 2.0: https://www.apache.org/licenses/LICENSE-2.0