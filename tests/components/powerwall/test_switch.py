"""Test for Powerwall off-grid switch"""

from homeassistant.helpers import entity_registry as ent_reg
from unittest.mock import patch

from .mocks import _mock_powerwall_with_fixtures

from tests.common import MockConfigEntry

async def test_entity_registry(hass):
    """Test powerwall device in device registry."""
    entity_registry = ent_reg.async_get(hass)

    assert "switch.off_grid" in entity_registry.entities

async def test_offgridswitch(hass):
    """Test creation of off-grid switch"""

    mock_powerwall = await _mock_powerwall_with_fixtures(hass)

    config_entry = MockConfigEntry(domain=DOMAIN, data={CONF_IP_ADDRESS: "1.2.3.4"})
    config_entry.add_to_hass(hass)

    with patch(
        "homeassistant.components.powerwall.config_flow.Powerwall",
        return_value=mock_powerwall,
    ), patch(
        "homeassistant.components.powerwall.Powerwall", return_value=mock_powerwall
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    state = hass.states.get("switch.")