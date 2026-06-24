from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState
from . import names


MAIN_BOSSES = [
    names.burst_man_defeated,
    names.cloud_man_defeated,
    names.junk_man_defeated,
    names.freeze_man_defeated,
    names.slash_man_defeated,
    names.spring_man_defeated,
    names.shade_man_defeated,
    names.turbo_man_defeated,
]

WEAKNESS_TABLE = {
    names.burst_man_defeated:  [names.freeze_cracker, names.scorch_wheel],
    names.cloud_man_defeated:  [names.danger_wrap],
    names.junk_man_defeated:   [names.thunder_bolt],
    names.freeze_man_defeated: [names.junk_shield, names.scorch_wheel],
    names.mash_defeated:       [names.danger_wrap],
    names.slash_man_defeated:  [names.freeze_cracker, names.scorch_wheel],
    names.spring_man_defeated: [names.slash_claw],
    names.shade_man_defeated:  [names.wild_coil],
    names.turbo_man_defeated:  [names.noise_crush],
    names.guts_man_g_defeated: [names.slash_claw],
    names.gamerizer_defeated:  [names.wild_coil, names.danger_wrap],
    names.hannya_ned_defeated: [names.slash_claw, names.noise_crush],
    "Wily Machine 7 Defeated": [names.thunder_bolt],
    names.wily_capsule:        [names.wild_coil],
}


BOSS_ACCESS_TABLE = {
    names.burst_man_defeated:  names.burst_man_access,
    names.cloud_man_defeated:  names.cloud_man_access,
    names.junk_man_defeated:   names.junk_man_access,
    names.freeze_man_defeated: names.freeze_man_access,
    names.slash_man_defeated:  names.slash_man_access,
    names.spring_man_defeated: names.spring_man_access,
    names.shade_man_defeated:  names.shade_man_access,
    names.turbo_man_defeated:  names.turbo_man_access,
}


BOSS_ITEM_LOCATION_TABLE = {
    names.burst_man_defeated:  names.burst_man_defeated_item,
    names.cloud_man_defeated:  names.cloud_man_defeated_item,
    names.junk_man_defeated:   names.junk_man_defeated_item,
    names.freeze_man_defeated: names.freeze_man_defeated_item,
    names.slash_man_defeated:  names.slash_man_defeated_item,
    names.spring_man_defeated: names.spring_man_defeated_item,
    names.shade_man_defeated:  names.shade_man_defeated_item,
    names.turbo_man_defeated:  names.turbo_man_defeated_item,
}


# Super Adapter is not an AP item. In logic, it is derived from all four Rush plates.
def has_super_adapter(state: CollectionState, player: int) -> bool:
    return (
        state.has(names.rush_r_plate, player) and
        state.has(names.rush_u_plate, player) and
        state.has(names.rush_s_plate, player) and
        state.has(names.rush_h_plate, player)
    )


# Convenience: can the player traverse vertically?
def can_traverse_vertical(state: CollectionState, player: int) -> bool:
    return (
        state.has(names.rush_coil, player) or
        state.has(names.rush_jet, player) or
        has_super_adapter(state, player)
    )


def set_rules(world: World, multiworld: MultiWorld, player: int) -> None:

    # ============================================================
    # Main boss locations — access code gates both medal and item
    # locations for each boss. Weakness logic applied optionally.
    # ============================================================
    for boss, access in BOSS_ACCESS_TABLE.items():
        item_location = BOSS_ITEM_LOCATION_TABLE[boss]

        # Medal location
        multiworld.get_location(boss, player).access_rule = \
            lambda state, a=access: state.has(a, player)

        # Item location
        multiworld.get_location(item_location, player).access_rule = \
            lambda state, a=access: state.has(a, player)

    # Optional weakness logic
    if world.options.logic_boss_weakness:
        for boss, access in BOSS_ACCESS_TABLE.items():
            weaknesses = WEAKNESS_TABLE[boss]
            item_location = BOSS_ITEM_LOCATION_TABLE[boss]

            multiworld.get_location(boss, player).access_rule = \
                lambda state, a=access, w=weaknesses: (
                    state.has(a, player) and
                    any(state.has(weapon, player) for weapon in w)
                )

            multiworld.get_location(item_location, player).access_rule = \
                lambda state, a=access, w=weaknesses: (
                    state.has(a, player) and
                    any(state.has(weapon, player) for weapon in w)
                )

    # ============================================================
    # Mash — no access rule, game-enforced after 4 medals
    # ============================================================
    # no rule needed

    # ============================================================
    # Wily bosses — gated by region access only (linear chain)
    # weakness logic applied if option enabled
    # ============================================================
    if world.options.logic_boss_weakness:
        for boss in [names.guts_man_g_defeated,
                     names.gamerizer_defeated,
                     names.hannya_ned_defeated]:
            weaknesses = WEAKNESS_TABLE[boss]
            multiworld.get_location(boss, player).access_rule = \
                lambda state, w=weaknesses: \
                    any(state.has(weapon, player) for weapon in w)

    # ============================================================
    # Proto Man — meetings give locked clue items, fight requires
    # both clues
    # ============================================================
    multiworld.get_location(names.proto_man_cloud_man_loc, player).access_rule = \
        lambda state: (state.has(names.cloud_man_access, player) and
                       can_traverse_vertical(state, player))

    multiworld.get_location(names.proto_man_turbo_man_loc, player).access_rule = \
        lambda state: state.has(names.turbo_man_access, player)

    multiworld.get_location(names.proto_shield_loc, player).access_rule = \
        lambda state: (state.has(names.shade_man_access, player) and
                       state.has(names.proto_man_cloud_man, player) and
                       state.has(names.proto_man_turbo_man, player))

    # ============================================================
    # Bass — no weapon requirements, region access only
    # ============================================================
    # no additional rules needed beyond region access

    # ============================================================
    # Circuit Plates and unique items (0x0BA4 bitfield)
    # ============================================================
    multiworld.get_location(names.rush_r_plate_loc, player).access_rule = \
        lambda state: state.has(names.burst_man_access, player)

    multiworld.get_location(names.rush_u_plate_loc, player).access_rule = \
        lambda state: (state.has(names.cloud_man_access, player) and
                       can_traverse_vertical(state, player))

    multiworld.get_location(names.rush_s_plate_loc, player).access_rule = \
        lambda state: (state.has(names.junk_man_access, player) and
                       state.has(names.freeze_cracker, player))

    multiworld.get_location(names.rush_h_plate_loc, player).access_rule = \
        lambda state: (state.has(names.freeze_man_access, player) and
                       can_traverse_vertical(state, player))

    multiworld.get_location(names.hyper_bolt_loc, player).access_rule = \
        lambda state: state.has(names.spring_man_access, player)

    multiworld.get_location(names.exit_unit_loc, player).access_rule = \
        lambda state: (
            (state.has(names.freeze_man_access, player) and
             state.has(names.rush_search, player)) or
            state.has(names.shop_access, player)
        )

    multiworld.get_location(names.hyper_rocket_buster_loc, player).access_rule = \
        lambda state: (
            (state.has(names.turbo_man_access, player) and
             has_super_adapter(state, player) and
             state.has(names.rush_search, player)) or
            (state.has(names.shop_access, player) and
             state.has(names.hyper_bolt, player))
        )

    multiworld.get_location(names.energy_balancer_loc, player).access_rule = \
        lambda state: (
            (state.has(names.shade_man_access, player) and
             state.has(names.rush_search, player)) or
            (state.has(names.shop_access, player) and
             state.has(names.hyper_bolt, player))
        )

    multiworld.get_location(names.beat_loc, player).access_rule = \
        lambda state: (state.has(names.slash_man_access, player) and
                       state.has(names.scorch_wheel, player))

    # ============================================================
    # Rush items
    # ============================================================
    multiworld.get_location(names.rush_search_loc, player).access_rule = \
        lambda state: (
            state.has(names.freeze_man_access, player) or
            (state.has(names.shop_access, player) and
             state.has(names.hyper_bolt, player))
        )

    multiworld.get_location(names.rush_jet_loc, player).access_rule = \
        lambda state: (
            (state.has(names.junk_man_access, player) and
             (state.has(names.thunder_bolt, player) or
              state.has(names.rush_coil, player) or
              state.has(names.rush_jet, player) or
              has_super_adapter(state, player))) or
            (state.has(names.shop_access, player) and
             state.has(names.hyper_bolt, player))
        )

    # ============================================================
    # Mega Bolts and Mega Health Capsule — all require Rush Search
    # ============================================================
    multiworld.get_location(names.mega_bolt_cloud_man_loc, player).access_rule = \
        lambda state: (state.has(names.cloud_man_access, player) and
                       state.has(names.rush_search, player))

    multiworld.get_location(names.mega_bolt_spring_man_loc, player).access_rule = \
        lambda state: (state.has(names.spring_man_access, player) and
                       state.has(names.rush_search, player))

    multiworld.get_location(names.mega_bolt_shade_man_loc, player).access_rule = \
        lambda state: (state.has(names.shade_man_access, player) and
                       state.has(names.rush_search, player))

    multiworld.get_location(names.mega_bolt_turbo_man_loc, player).access_rule = \
        lambda state: (state.has(names.turbo_man_access, player) and
                       state.has(names.rush_search, player))

    multiworld.get_location(names.mega_bolt_junk_man_loc, player).access_rule = \
        lambda state: (state.has(names.junk_man_access, player) and
                       state.has(names.freeze_cracker, player) and
                       state.has(names.rush_search, player))

    multiworld.get_location(names.mega_health_capsule_loc, player).access_rule = \
        lambda state: (state.has(names.spring_man_access, player) and
                       state.has(names.rush_search, player))

    # ============================================================
    # Goal
    # ============================================================
    multiworld.completion_condition[player] = \
        lambda state: state.has(names.wily_capsule, player)
