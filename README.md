# ASTERION

ASTERION is a Python and Ursina Engine project that generates and displays a small planetary system from a numerical seed. It creates a star and a set of planets, draws their orbital paths, and animates their motion. Entering the same seed reproduces the same generated numerical system.

The project is a simplified educational visualization. It uses a few astronomy-inspired relationships to make the generated systems behave coherently; it is not a full astrophysics simulator.

## What it does

- Accepts a numerical seed, or chooses a random seed when the field is left blank.
- Generates one star and between 2 and 8 planets.
- Assigns generated masses, orbital distances, starting angles, and rotation rates.
- Chooses a star texture based on the generated star temperature and planet and space-background textures from the bundled image folders.
- Draws circular orbit paths and animates the planets around the star.
- Displays the seed, star mass, and planet count after generation.
- Lets the viewer pause, change simulation speed, and create another random system.

## Run ASTERION

### Requirements

- Windows, macOS, or Linux desktop with a graphics-capable display.
- Python 3.10 or newer. The local project environment records Python 3.14.7.
- Ursina 8.3.0. Installing Ursina also installs its runtime dependencies, including Panda3D and Pillow.
- The complete `textures` directory. The application loads images through paths relative to the project folder.

The local environment records Ursina 8.3.0, Panda3D 1.10.16, and Pillow 13.0.0. The `.venv` directory is a local virtual environment and is excluded from version control; judges should create their own environment.

### Windows setup

Download or clone the complete project, then open PowerShell in the `ASTERION` project folder. Keep the `textures` folder beside `main.py`.

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install ursina==8.3.0
.\.venv\Scripts\python.exe main.py
```

If the Python launcher does not recognize `-3.14`, install Python 3.14 first or use another installed Python 3 version that meets Ursina's requirements, and substitute that version in the virtual-environment command.

### macOS or Linux setup

Open a terminal in the project folder and run:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install ursina==8.3.0
.venv/bin/python main.py
```

Run `main.py` from the project root. Running it from another working directory can prevent the relative texture paths from resolving.

## Controls

### Opening screen

1. Enter a number in the seed field, or leave it empty for a random seed.
2. Select **CREATE PLANETARY SYSTEM**.
3. The generated seed and basic system information appear in the scene.

The seed field accepts digits. An empty field selects a random integer from 0 through 10,000,000. After generation, the opening controls are disabled. Restart the application to enter another specific seed.

### Simulation

| Input | Action |
|---|---|
| `Space` | Pause or resume orbital motion |
| `Up Arrow` | Increase simulation speed by one step |
| `Down Arrow` | Decrease simulation speed by one step, down to a minimum of one |
| `N` | Generate a new system with a random seed |
| Right mouse drag | Rotate the camera view |
| Mouse wheel | Zoom in or out |
| Middle mouse drag | Pan the camera |
| `W`, `A`, `S`, `D`, `E`, `Q` while holding right mouse | Move the camera |

The simulation starts at speed 10. Pressing `N` resets the elapsed simulation time and speed to 10 before generating the next random system.

## How the project is organized

```text
ASTERION/
├── main.py                 # Ursina app, interface, rendering, controls, and animation
├── asterion.py             # System data classes, generation, and orbital-position math
├── textures/
│   ├── background/         # Space sky images
│   ├── planets/            # Planet surface images
│   └── stars/              # Star surface images by color class
├── README.md
└── .venv/                  # Local environment; ignored by Git and not needed by judges
```

### `asterion.py`

Defines the `Star`, `Planet`, and `System` data classes. `generate_system(seed)` creates the star and planets from the seed. `current_position(system, elapsed_time)` calculates each planet's current position in the system's orbital plane.

### `main.py`

Creates the Ursina application and opening screen; loads the image assets; builds the star, planets, orbit paths, and background; advances the simulation each frame; and handles keyboard and mouse controls. The opening screen uses `textures/background/7.png`; after generation, a background is selected from the bundled background images.

## Generation and mathematical model

ASTERION uses Python's pseudorandom number generator. The seed initializes that generator, so the same seed produces the same generated numerical values in the same code and runtime environment.

For each system, the generator chooses:

- **Star mass:** uniformly between 0.3 and 3.0 solar-mass units.
- **Planet count:** an integer from 2 through 8, inclusive.
- **Planet mass:** uniformly between 0.5 and 5.0 project earth-mass units.
- **Starting orbital angle:** uniformly between 0 and 360 degrees.
- **Planet rotation rate:** uniformly between 8 and 30 code units; this is a visual rotation rate, not a measured planetary spin period.

Planet orbital distances are selected in successive bands. For planet index `i`, beginning at zero:

```text
orbital distance a is uniformly selected from [0.5 + i, 1.0 + i]
```

The calculation treats the distance as AU-like and star mass as solar-mass-like when estimating the orbital period. The code does not attach formal units to the stored distance values.

### Star properties

The generated star stores mass `M`, normalized luminosity `L`, and a normalized temperature value `T`:

```text
L = M^4
T = M^0.6 (unit:sun's temperature)
```

These are simple mass-based heuristics inspired by main-sequence star relationships. They are not a stellar evolution model; `T` is not in kelvin. The normalized temperature selects one of five star texture/color classes:

| Normalized temperature | Display class |
|---:|---|
| `T <= 0.64` | Red |
| `0.64 < T <= 0.90` | Orange |
| `0.90 < T <= 1.03` | Yellow |
| `1.03 < T <= 1.72` | White |
| `T > 1.72` | Blue |

The luminosity value is calculated and stored but is not currently used to calculate lighting or planet temperatures.

### Orbital period and position

The project uses the simplified form of Kepler's third law for a planet orbiting a much more massive star. With orbital distance `a` in AU-like units and star mass `M` in solar-mass-like units, the period is approximated as:

```text
P_years = sqrt(a^3 / M)
P_days  = 365.25 * P_years
```

This comes from the normalized relationship `P^2 = a^3 / M`. It assumes the planet's mass is negligible compared with the star's mass.

For elapsed simulated time `t` in days and starting angle `theta(0)`, the orbital angle and position are:

```text
theta = (theta0 + 360 * t / P_days) modulo 360 degrees
x = a * cos(theta)
z = a * sin(theta)
```

The position is placed in the XZ plane, leaving the Y coordinate at zero. The rendered orbital distance is multiplied by 10 for visibility. Simulation time advances by `frame_time * simulation_speed`; the initial speed is 10 simulated days per real second by convention.

Planet sphere size and star sphere size are visual scaling choices. They are not rendered to the same physical scale as their orbital distances. Planet spin is also accelerated by the simulation-speed setting.

## Assumptions and limitations

- Orbits are circular, coplanar, and centered on a stationary star.
- Each planet moves at a constant angular rate calculated from its approximate orbital period.
- The simulation does not calculate gravitational forces, interactions between planets, orbital eccentricity, inclination, collisions, or long-term orbital changes.
- Star luminosity and temperature are heuristic normalized values, not outputs from a detailed stellar model.
- Planet masses, radii, colors, and distances are generated for a visual demonstration and should not be interpreted as validated exoplanet measurements.
- Texture selection is seeded, but the order in which a filesystem returns texture filenames may vary between computers; exact texture assignments can therefore differ even when the numerical system matches.

## Suggested judge demo

1. Launch the application from the project root.
2. Enter a seed such as `31415` and generate a system.
3. Point out the displayed seed, star mass, and planet count; use right-drag and the mouse wheel to inspect the system.
4. Press `Space` to pause and resume, then use the arrow keys to change orbital speed.
5. Press `N` to show a different randomly seeded system.
6. To demonstrate the same seed again, restart the application and enter it again.

## Asset credits

The project includes third-party images under `textures/`. Credits and license notes for the identifiable sets are below.

### Planet textures

- `textures/planets/Arid_*`, `Barren_*`, `Dusty_*`, `Gaseous_*`, `Grassland_*`, `Jungle_*`, `Marshy_*`, `Martian_*`, `Methane_*`, `Sandy_*`, `Snowy_*`, and `Tundra_*`: **Screaming Brain Studios**, from the [Planet Texture Pack](https://screamingbrainstudios.com/dl-planet-texture-pack-1/). The pack is released as CC0 / public domain, so attribution is optional.
- `textures/planets/2k_mars.jpg`, `2k_ceres_fictional.jpg`, `2k_eris_fictional.jpg`, `2k_haumea_fictional.jpg`, and `2k_makemake_fictional.jpg`: **Solar System Scope**, from its [solar texture collection](https://www.solarsystemscope.com/textures/). The collection is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Suggested attribution: "Planet textures by Solar System Scope, licensed under CC BY 4.0." The Ceres, Eris, Haumea, and Makemake maps are stylized fictional surface maps, not spacecraft photographs.

### Space backgrounds

The numbered PNG panoramas match these downloads from **TonyS / Space Spheremaps** by their 10000 x 5000 dimensions and exact file sizes. The creator says the maps were made in Cinema 4D. They are free to use and modify; attribution is appreciated. The site lists Creative Commons BY 4.0 terms and says not to use the images for AI image training.

| Project file | Source asset |
|---|---|
| `textures/background/1.png` and `8.png` | [Multi Nebulae 1](https://www.spacespheremaps.com/multi-nebulae-spheremaps/) (`8.png` is a duplicate of `1.png`) |
| `textures/background/2.png` | [Galactic Plane 1](https://www.spacespheremaps.com/galactic-plane-spheremaps/) |
| `textures/background/3.png` | [Blue Nebulae 3](https://www.spacespheremaps.com/blue-nebulae-spheremaps/) |
| `textures/background/4.png` | [Blue Nebulae 2](https://www.spacespheremaps.com/blue-nebulae-spheremaps/) |
| `textures/background/5.png` | [Blue Nebulae 1](https://www.spacespheremaps.com/blue-nebulae-spheremaps/) |
| `textures/background/6.png` | [Multi Nebulae 3](https://www.spacespheremaps.com/multi-nebulae-spheremaps/) |
| `textures/background/7.png` | [Multi Nebulae 2](https://www.spacespheremaps.com/multi-nebulae-spheremaps/) |

### Star textures and remaining background

- `textures/stars/orange.jpg` is likely Solar System Scope's `2k_sun.jpg`: its 2048 x 1024 dimensions and file size match that source image. Credit it as Solar System Scope, CC BY 4.0, if this source is confirmed by the project author.
- The source of `textures/stars/blue.jpeg`, `red.jpeg`, `white.jpeg`, and `yellow.jpeg` could not be established from the files or reliable matching source pages. Their embedded image metadata contains no creator information.
- `textures/background/9.jpg` is a 4096 x 2048 Milky Way panorama. It resembles Solar System Scope's Stars + Milky Way map, but its exact source or any resizing/editing history could not be confirmed from the files.

Please confirm the last two groups with the person who collected the images or their original download history before claiming a creator or license for them. Do not leave third-party assets without a valid source/license if you redistribute the project publicly.

## References

- [Ursina Engine](https://github.com/pokepetter/ursina)
- [Kepler's laws of planetary motion](https://science.nasa.gov/solar-system/orbits-and-keplers-laws/)
