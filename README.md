# Secure Selenium Python Template
Secure Selenium driver with settings.  

## Usage

1. `my_instance = SecureSelenium(<webdriver path>, <user agent>, <if headless display>)`
1. `my_instance.get(<url>)`

## Example

```
user_agent: str = "Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36"

my_instance: SecureSelenium = SecureSelenium(
  "path/to/webdriver", user_agent, False)

some_response: str = my_instance.get(<url>)
```

# How to update Chrome and Selenium Chrome webdriver

_IMPORTANT: Chrome browser and Chrome webdriver must match in version but not necessarily the same version number._

1. Download the Chrome browser
   1. Choose the Linux version from https://omahaproxy.appspot.com/, preferably the `stable` release.
   1. Download the Chrome browser version at https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}-1_amd64.deb where ${CHROME_VERSION} is the specific browser version.  Note: this may not work for all versions.  

      Example: `https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_101.0.4951.44-1_amd64.deb`

   1. https://commondatastorage.googleapis.com/chromium-browser-continuous/index.html

1. Download the matching webdriver
   1. Go to https://chromedriver.chromium.org/downloads and download the correct version of the webdriver.  Sometimes you only need to match the 100.* version depending on the site's instructions.  
   1. Before building, `unzip` zip file and name the binary `chromedriver`.    

## Common pitfalls

**Selenium can't find my browser**

Ensure the location of the Chrome browser is in the environment variable `$PATH`.
