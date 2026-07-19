"""
JARVIS Weather Tool

Provides current weather information.

Current Provider:
- Open-Meteo (API key not required)

Responsibilities:
- Validate coordinates
- Fetch weather
- Return structured weather information

Contains NO business logic outside weather retrieval.
"""

from __future__ import annotations

from typing import Any

import requests

from app.tools.base import BaseTool
from app.tools.exceptions import (
    ToolExecutionError,
    ToolValidationError,
)
from app.tools.models import ToolCategory


class WeatherTool(BaseTool):
    """
    Weather tool using Open-Meteo API.
    """

    API_URL = (
        "https://api.open-meteo.com/v1/forecast"
    )

    @property
    def name(self) -> str:
        return "weather"

    @property
    def description(self) -> str:
        return "Get current weather."

    @property
    def category(self) -> ToolCategory:
        return ToolCategory.UTILITY

    def validate(self, **kwargs: Any) -> None:

        latitude = kwargs.get("latitude")
        longitude = kwargs.get("longitude")

        if latitude is None:
            raise ToolValidationError(
                "Missing latitude."
            )

        if longitude is None:
            raise ToolValidationError(
                "Missing longitude."
            )

        if not isinstance(latitude, (int, float)):
            raise ToolValidationError(
                "Latitude must be numeric."
            )

        if not isinstance(longitude, (int, float)):
            raise ToolValidationError(
                "Longitude must be numeric."
            )

        if not (-90 <= latitude <= 90):
            raise ToolValidationError(
                "Latitude out of range."
            )

        if not (-180 <= longitude <= 180):
            raise ToolValidationError(
                "Longitude out of range."
            )

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        """
        Fetch current weather.
        """

        self.validate(**kwargs)

        latitude = kwargs["latitude"]
        longitude = kwargs["longitude"]

        try:

            response = requests.get(
                self.API_URL,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current_weather": True,
                },
                timeout=15,
            )

            response.raise_for_status()

            data = response.json()

            weather = data["current_weather"]

            return {
                "temperature": weather["temperature"],
                "windspeed": weather["windspeed"],
                "winddirection": weather["winddirection"],
                "weathercode": weather["weathercode"],
                "time": weather["time"],
            }

        except requests.RequestException as error:
            raise ToolExecutionError(
                "Unable to fetch weather."
            ) from error