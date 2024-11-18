# CHANGELOG

- [CHANGELOG](#changelog)
  - [VERSION 0.1](#version-01)
  - [VERSION 0.2](#version-02)
    - [FIX 0.2.1](#fix-021)
  - [VERSION 0.3](#version-03)
    - [FIX 0.3.1](#fix-031)
    - [FIX 0.3.2](#fix-032)
    - [FIX 0.3.3](#fix-033)

## VERSION 0.1

- Working docker container
- Show in log which pods have been restarted

## VERSION 0.2

- Send Telegram notifications when there are restarted pods

### FIX 0.2.1

- Disable urllib3 warnings

## VERSION 0.3

- Instead show pod information in logs, this version shows a formatted table
- No `INFO` traces are logged, just `DEBUG` and `ERROR`

### FIX 0.3.1

- Fix docker image name in [README.md](README.md)

### FIX 0.3.2

- Changed entrypoint in [Dockerfile](Dockerfile) to include python script

### FIX 0.3.3

- Catch ApiException for unauthorized requests
- Improved verbosity of logged errors
