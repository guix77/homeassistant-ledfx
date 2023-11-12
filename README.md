# Home Assistant LedFx

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

<!-- ![Project Maintenance][maintenance-shield] -->
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]
<!--  -->
<!-- [![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum] -->

**This integration will set up the following platforms.**

Platform | Description
-- | --
`media_player` | Set LedFx on play or pause.

This integration only allows to set LedFx on play or on pause, which is my only personal use case. I have a lots of WLEDs at home and I want to be able to use them in other ways than LedFx (HA, Hyperion, ...), and I was fed up with opening the LedFx UI to set pause or play.

This integration is not meant at all to re-create https://github.com/dmamontov/hass-ledfx which has unfortunately been broken for a while now.

PRs are welcome if you need something else and can code it.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `ledfx`.
1. Download _all_ the files from the `custom_components/ledfx/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "LedFx"

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[buymecoffee]: https://www.buymeacoffee.com/guix77
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/guix77/homeassistant-ledfx.svg?style=for-the-badge
[commits]: https://github.com/guix77/homeassistant-ledfx/commits/main
[discord]: https://discord.gg
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/guix77/homeassistant-ledfx.svg?style=for-the-badge
<!-- [maintenance-shield]: https://img.shields.io/badge/maintainer.svg?style=for-the-badge -->
[releases-shield]: https://img.shields.io/github/release/guix77/homeassistant-ledfx.svg?style=for-the-badge
[releases]: https://github.com/guix77/homeassistant-ledfx/releases
