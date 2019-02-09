# dpiswitch — a KDE Plasma DPI switcher

Configure and automate KDE Plasma DPI scaling from the command line by using a JSON-based configuration file with different profiles.

---

## Purpose
This tool is particularly handy for people who need different scaling factors at differnt times. 

Scenario: A HiDPI laptop that needs a scaling of 1.5 to be usable. Which is then docked onto a standard 1080p display that needs a 1.0 scaling.

Manually changing DPI settings, panel height/width, clock font or other settings for widgets each time the computer is connected to a different display is tedious.

This tool will automatically update all the necessary settings reducing manual work to a minimum.

## Usage

`$ dpiswitch --config profiles.json --profile name`

Nb: Executing `dpiswitch` will kill your current plasma session and force a logout, so make sure not to have any unsaved work.

Users need to create their own configuration file based on their scaling factors and the widget/panel configuration in the system. A sample `profile.json` file which scales the screen, fonts, sets the height of the bottom panel and updates widget configuration is provided below:

```json
{
    "version": "1.0",
    "profiles": [{
        "name": "laptop",
        "description": "Set scaling to 1.5",
        "scaling": 1.5,
        "cursor": {
            "size": 36
        },
        "panels": [{
            "groups": ["Panel 2", "Horizontal1920"],
            "thickness": 50
        }],
        "widgets": [{
            "groups": ["Containments", 2, "Applets", 22, "Configuration", "General"],
            "key": "clock_maxheight",
            "value": 36
        }]
    }]
}

```

## Widget and Panel configuration

Plasma configuration is stored in a [INI-like](https://en.wikipedia.org/wiki/INI_file) syntax in the following locations

| Config. | Filename  | 
|---|---|
| Panels | `~/.config/plasmashellrc` |
| Widgets | `~/.config/plasma-org.kde.plasma.desktop-appletsrc` |

### Panel scaling example

While this paragraph shows how to change the "thickness" of panels, the same method can be used to update widgets. Panel "thickness" denotes width or height, depending on whether the panel is horizontal or vertical.

In order to scale the panel's width or height one must locate the panel's Groups/Section's and use them in the configuration file to identify it.

An example configuration of a bottom panel:
```ini
[Plasma Views][Panel2][Horizontal1920]
thickness=38
```

each of the groups is an element of the object inside the `panels` array. The above example would get translated into

```json
{
    "groups": ["Plasma Views", "Panel2", "Horizontal1920"],
    "thickness": "<New thickness>"
}
```

### Limitations

* Executing this tool will kill your Plasma session in order not to have the DE overwrite the newly updated values.
* A logout is needed for all the DPI scaling features to be fully applied.
