# Species Finder CLI Tool (Version 0.1.0)

A cli tool that fetches a list of unique species observed in a specified
geographic area using the iNaturalist API.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Options](#options)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/species-finder.git
    ```

2. Navigate to the project directory:

    ```bash
    cd species-finder
    ```

3. Install the required packages:

    ```bash
    poetry install
    ```

## Usage

You can specify either latitude and longitude or a location name to search for
species within a certain radius.

```bash
Usage: inat-fetch [OPTIONS]

  Fetch species in a geographic area using the iNaturalist API.

Options:
  --latitude FLOAT     Latitude of the center point
  --longitude FLOAT    Longitude of the center point
  --radius FLOAT       Radius around the center point, in kilometers
                       [required]
  --location TEXT      Town name or region as geographic area
  --page-size INTEGER  Max number of species to return
  --help               Show this message and exit.
```

Fetching a list of species found in a 10km radius of Roleystone, Western Australia

### Using Latitude and Longitude:

```bash
$ inat-fetch --latitude -32.1232 --longitude 116.0144 --radius 10
```

### Using a Location Name:

```bash
$ inat-fetch --location "Roleystone, Western Australia" --radius 10
```

### Options

- `--latitude`: Latitude of the center point.
- `--longitude`: Longitude of the center point.
- `--radius`: Radius around the center point, in kilometers. (Required)
- `--location`: Town name or region as a geographic area.
- `--page-size`: Maximum number of species to return. Default is 100.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

## License

[MIT License](LICENSE)

