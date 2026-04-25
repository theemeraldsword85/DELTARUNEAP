from worlds.generic.Rules import set_rule

from typing import TYPE_CHECKING

from .Items import CCItems
from .LocationsAndRegions import CCLocations
from ..chapter_1.LocationsAndRegions import Ch1Locations
from ..chapter_1.Items import Ch1Items
from ..chapter_1.LocationsAndRegions import Ch1Locations
from ..chapter_2.Items import Ch2Items
from ..chapter_2.LocationsAndRegions import Ch2Locations
from ..chapter_3.Items import Ch3Items
from ..chapter_3.LocationsAndRegions import Ch3Locations
from ..chapter_4.Items import Ch4Items
from ..chapter_4.LocationsAndRegions import Ch4Locations
from ..chapter_5.Items import Ch5Items
from ..chapter_5.LocationsAndRegions import Ch5Locations

if TYPE_CHECKING:
    from .. import DeltaruneWorld


def set_rules(world: "DeltaruneWorld"):
    player = world.player
    multiworld = world.multiworld

    # Fusions
    if world.can_access_fusion():

        # TwinRibbon
        if world.has_at_least_one_chapter_included([2, 3]) and world.has_at_least_one_chapter_included([1, 2, 3]):
            if (not world.include_chapter(2)) or (
                world.include_chapter(1) and world.is_chapters_in_order
            ):  # If you play chapter 1 in order then you don't get the white ribbon ralsei starts with
                set_rule(
                    multiworld.get_location(CCLocations.castle_town_twin_ribbon_fusion, player),
                    lambda state: state.has(CCItems.pink_ribbon, player) and state.has(CCItems.white_ribbon, player),
                )
            else:
                set_rule(
                    multiworld.get_location(CCLocations.castle_town_twin_ribbon_fusion, player),
                    lambda state: state.has(CCItems.pink_ribbon, player),
                )

        # SpikeBand
        if world.include_chapter(1):
            if world.include_chapter(4):  # Chapter 4 have GlowWist have starter item so don't require it
                set_rule(
                    multiworld.get_location(CCLocations.castle_town_spike_band_fusion, player),
                    lambda state: state.has(Ch1Items.ironshackle, player) and state.has(Ch4Items.chapter_4_unlock, player),
                )
            elif world.include_chapter(2):  # Chapter 2 have to gain GlowWist so require it to acquire it
                set_rule(
                    multiworld.get_location(CCLocations.castle_town_spike_band_fusion, player),
                    lambda state: state.has(Ch1Items.ironshackle, player) and state.has(Ch2Items.glowwrist, player),
                )

        # TensionBow
        if world.include_chapter(2) and (not world.is_weird_route() or world.is_all_routes()):
            set_rule(
                multiworld.get_location(CCLocations.castle_town_tensionbow_fusion, player),
                lambda state: state.has(Ch2Items.bshotbowtie, player) and state.has(Ch2Items.tensionbit, player),
            )

        # TwistedSwd
        if False and world.is_unused_items_included() and world.include_chapter(2) and world.is_weird_route():
            set_rule(
                multiworld.get_location(CCLocations.castle_town_twistedsword_fusion, player),
                lambda state: state.has(Ch2Items.thornring, player) and state.has(CCItems.purecrystal, player),
            )
            multiworld.get_location(CCLocations.castle_town_twistedsword_fusion, player).place_locked_item(
                world.create_item(CCItems.twistedswd)
            )


def get_location(world: "DeltaruneWorld", chapter: int):
    if chapter == 1:
        return world.multiworld.get_location(Ch1Locations.fountain_sealed, world.player)
    if chapter == 2:
        return world.multiworld.get_location(Ch2Locations.fountain_sealed, world.player)
    if chapter == 3:
        return world.multiworld.get_location(Ch3Locations.fountain_sealed, world.player)
    if chapter == 4:
        return world.multiworld.get_location(Ch4Locations.third_sanctuary_fountain_sealed, world.player)


def get_unlock_item(world: "DeltaruneWorld", chapter: int):
    if chapter == 1:
        return Ch1Items.chapter_1_unlock
    if chapter == 2:
        return Ch2Items.chapter_2_unlock
    if chapter == 3:
        return Ch3Items.chapter_3_unlock
    if chapter == 4:
        return Ch4Items.chapter_4_unlock
    if chapter == 5:
        return Ch5Items.chapter_5_unlock


def handle_locked_items(world: "DeltaruneWorld"):
    player = world.player
    multiworld = world.multiworld

    if world.is_chapters_in_order():
        playable_chapters = world.get_playable_chapters()

        for current_chapter in playable_chapters:
            next_chapter = world.get_next_in_order_chapter(current_chapter)
            if next_chapter == -1:
                next_chapter = current_chapter + 1

            get_location(world, current_chapter).place_locked_item(
                world.create_item(get_unlock_item(world, next_chapter))
            )
