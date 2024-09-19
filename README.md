# GNOME check extensions
When a new Gnome DE release is out, the first concern is making sure all extensions used have been updated to the latest version. This tool automates this process for all desired extensions.

## Setup

- Install requirements

```bash
pip install -r requirements.txt
```

## Usage
1. Fill the `extensions.yml` file with the list of gnome extensions links you desire to check on.
1. Run the script

```bash
python3 gnome_check_extensions.py ${GNOME_VERSION}
```

**Example:**
```bash
python3 gnome_check_extensions.py 47
```

**Output example:**
```diff
+ Dash to Dock: 47
+ Caffeine: 47
+ Emoji Copy: 47
+ Tiling Shell: 47
- Desktop Icons NG (DING): 46
```
