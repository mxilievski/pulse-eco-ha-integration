# Pulse.Eco
[![pulse.eco logo](https://pulse.eco/img/pulse-logo-horizontal.svg)](https://pulse.eco)

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]

_Integration to integrate with [pulseeco][pulseeco]._

**This integration will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show sensors from pulse.eco.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `pulseeco`.
1. Download _all_ the files from the `custom_components/pulseeco/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Pulse.Eco"

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[pulseeco]: https://github.com/mxilievski/pulse-eco-ha-integration
[commits-shield]: https://img.shields.io/github/commit-activity/y/mxilievski/pulse-eco-ha-integration.svg?style=for-the-badge
[commits]: https://github.com/mxilievski/pulse-eco-ha-integration/commits/main
[exampleimg]: example.png
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/mxilievski/pulse-eco-ha-integration.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Martin%20Ilievski%20%40mxilievski-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/mxilievski/pulse-eco-ha-integration.svg?style=for-the-badge
[releases]: https://github.com/mxilievski/pulse-eco-ha-integration/releases
