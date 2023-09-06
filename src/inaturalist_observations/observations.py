import click
from geopy.geocoders import Nominatim
from pyinaturalist import pprint
from pyinaturalist.node_api import get_observations


def get_coordinates(location_name: str) -> tuple[float | None, float | None]:
    """
    Get the latitude and longitude coordinates of a given location name.

    :param location_name: Name of the location to geocode
    :type location_name: str
    :return: Tuple containing latitude and longitude
    :rtype: Tuple[Optional[float], Optional[float]]
    """

    geolocator = Nominatim(user_agent="geoapiExercises")
    if location := geolocator.geocode(location_name):
        return location.latitude, location.longitude
    else:
        return None, None


@click.command()
@click.option(
    "--latitude",
    type=float,
    help="Latitude of the center point",
)
@click.option(
    "--longitude",
    type=float,
    help="Longitude of the center point",
)
@click.option(
    "--radius",
    type=float,
    required=True,
    help="Radius around the centre point, in kilometres",
)
@click.option(
    "--location",
    type=str,
    help="Town name or region as geographic area",
)
@click.option(
    "--page-size",
    type=int,
    default=100,
    help="Max number of species to return",
)
def fetch_species(
    latitude: float | None,
    longitude: float | None,
    radius: float,
    location: str | None,
    page_size: int,
) -> None:
    """
    Fetch species in a geographic area using the iNaturalist API.
    """

    if location:
        latitude, longitude = get_coordinates(location)
        if latitude is None or longitude is None:
            click.echo(f"Could not find coordinates for the location: {location}")
            return

    if latitude is None or longitude is None:
        click.echo("Either coordinates or location must be provided.")
        return

    params = {
        "lat": latitude,
        "lng": longitude,
        "radius": radius,
        "per_page": page_size,
    }

    observations = get_observations(**params)
    pprint(observations)
    species_set = set()

    for observation in observations["results"]:
        if species_name := observation["species_guess"]:
            species_set.add(species_name)

    if species_set:
        click.echo(f"Found {len(species_set)} unique species in the specified area:")
        for species in sorted(species_set):
            click.echo(f"- {species}")
    else:
        click.echo("No species found in the specified area.")
