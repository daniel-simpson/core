"""Support for Powerwall Switches (V2 API only)"""

from typing import Any, Union
from homeassistant.components.powerwall.models import PowerwallRuntimeData
from homeassistant.components.switch import (
    SwitchDeviceClass,
    SwitchEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import EventType

from tesla_powerwall import (
    IslandMode,
    GridStatus,
)

from .const import DOMAIN, POWERWALL_API, POWERWALL_COORDINATOR

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Powerwall switch platform from Powerwall resournces."""
    powerwall_data: PowerwallRuntimeData = hass.data[DOMAIN][config_entry.entry_id]
    power_wall = powerwall_data[POWERWALL_API]
    coordinator = powerwall_data[POWERWALL_COORDINATOR]
    assert coordinator is not None
    
    async_add_entities([PowerwallOffGridEnabledEntity(power_wall, coordinator)])

class PowerwallOffGridEnabledEntity(SwitchEntity):
    """Representation of a Switch entity for Powerwall Off-grid operation."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_device_class = SwitchDeviceClass.SWITCH

    def __init__(
        self,
        power_wall,
        coordinator,
    ) -> None:
        """Initialise the entity."""
        self.power_wall = power_wall
        self.coordinator = coordinator
    
    @property
    def is_on(self) -> bool:
        """Return true if the powerwall is off-grid"""
        return self.coordinator.data.grid_status == GridStatus.TRANSITION_TO_ISLAND or self.coordinator.data.grid_status == GridStatus.ISLANDED
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn off-grid mode on"""
        await self.power_wall.set_island_mode(IslandMode.OFFGRID)
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off-grid mode off (return to on-grid usage)"""
        await self.power_wall.set_island_mode(IslandMode.ONGRID)