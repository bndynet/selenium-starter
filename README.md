# selenium-starter

## Run on CentOS without Desktop

- [Install Xvfb](https://gist.github.com/bndynet/cfab58172f37c0632d529a87371f0b93)
- Install Firefox
- Confirm Webdriver is matched with your browser  
  - [Firefox Drivers](https://github.com/mozilla/geckodriver/releases)  
  - [Chrome Drivers](https://sites.google.com/a/chromium.org/chromedriver/downloads)

## Python Issues

- `UnicodeEncodeError: 'ascii' codec can't encode characters in position`

  Set env to your *~/.bash_profile*
  > `export PYTHONIOENCODING=utf-8`
