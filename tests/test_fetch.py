from unittest.mock import Mock, patch

import pytest
from inaturalist_observations.observations import (fetch_species,
                                                   get_coordinates)

# Mock data for get_observations
mock_observations = {
    "results": [
        {"species_guess": "Kangaroo"},
        {"species_guess": "Koala"},
        {"species_guess": "Kangaroo"},
        {"species_guess": None},
    ]
}

# Mock data for Nominatim
mock_location = Mock()
mock_location.latitude = -32.1234
mock_location.longitude = 116.0150


# Test get_coordinates
@patch("inaturalist_observations.observations.Nominatim.geocode")
def test_get_coordinates_valid_location(mock_geocode):
    mock_geocode.return_value = mock_location
    lat, lon = get_coordinates("Roleystone, Western Australia")
    assert lat == -32.1234
    assert lon == 116.0150


@patch("inaturalist_observations.observations.Nominatim.geocode")
def test_get_coordinates_invalid_location(mock_geocode):
    mock_geocode.return_value = None
    lat, lon = get_coordinates("Invalid Location")
    assert lat is None
    assert lon is None


# Test fetch_species
@patch(
    "inaturalist_observations.observations.get_observations",
    return_value=mock_observations,
)
@patch(
    "inaturalist_observations.observations.get_coordinates",
    return_value=(-32.1234, 116.0150),
)
@patch("click.echo")
def test_fetch_species_with_location(
    mock_echo, mock_get_coordinates, mock_get_observations
):
    fetch_species(None, None, 10, "Roleystone, Western Australia", 100)
    mock_echo.assert_called_with("Found 2 unique species in the specified area:")


@patch(
    "inaturalist_observations.observations.get_observations",
    return_value=mock_observations,
)
@patch("click.echo")
def test_fetch_species_with_coordinates(mock_echo, mock_get_observations):
    fetch_species(-32.1234, 116.0150, 10, None, 100)
    mock_echo.assert_called_with("Found 2 unique species in the specified area:")


@patch(
    "inaturalist_observations.observations.get_coordinates", return_value=(None, None)
)
@patch("click.echo")
def test_fetch_species_invalid_location(mock_echo, mock_get_coordinates):
    fetch_species(None, None, 10, "Invalid Location", 100)
    mock_echo.assert_called_with(
        "Could not find coordinates for the location: Invalid Location"
    )


@patch("click.echo")
def test_fetch_species_no_coordinates_or_location(mock_echo):
    fetch_species(None, None, 10, None, 100)
    mock_echo.assert_called_with("Either coordinates or location must be provided.")


@patch(
    "inaturalist_observations.observations.get_observations",
    return_value={"results": []},
)
@patch("click.echo")
def test_fetch_species_no_species_found(mock_echo, mock_get_observations):
    fetch_species(-32.1234, 116.0150, 10, None, 100)
    mock_echo.assert_called_with("No species found in the specified area.")
