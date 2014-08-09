# -*- coding: utf-8 -*-
# Copyright (C) 2014 Daniele Simonetti
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

def get_clan(storage, ident):
    try:
        return [x for x in storage.clans if x.id == ident][0]
    except:
        return None

def get_family(storage, ident):
    try:
        return [x for x in storage.families if x.id == ident][0]
    except:
        return None

def get_school(storage, ident):
    try:
        return [x for x in storage.schools if x.id == ident][0]
    except Exception as e:
        print(e)
        return None

def get_base_schools(storage):
    def is_base_school(school):
        return (len(school.require) == 0 and
                'advanced' not in school.tags and
                'alternate' not in school.tags)
    try:
        return [x for x in storage.schools if is_base_school(x)]
    except:
        return None

def get_school_tech(school_obj, rank):
    try:
        return [x for x in school_obj.techs if x.rank == rank][0]
    except:
        return None

def get_tech(storage, ident):
    for sc in storage.schools:
        tech = [x for x in sc.techs if x.id == ident]
        if len(tech): return sc, tech[0]
    return None, None

def get_skill(storage, ident):
    try:
        return [x for x in storage.skills if x.id == ident][0]
    except:
        return None

def get_skills(storage, categ):
    return [x for x in storage.skills if x.type == categ]

def get_spells(storage, ring, mastery):
    return [x for x in storage.spells if x.element == ring and x.mastery == mastery]

def get_maho_spells(storage, ring, mastery):
    return [x for x in storage.spells if x.element == ring and x.mastery == mastery and 'maho' in x.tags]

def get_mastery_ability_rule(storage, ident, value):
    try:
        skill = get_skill(storage, ident)
        return [x for x in skill.mastery_abilities if x.rank == value][0].rule
    except:
        return None

def get_kata(storage, ident):
    try:
        return [x for x in storage.katas if x.id == ident][0]
    except:
        return None

def get_kiho(storage, ident):
    try:
        return [x for x in storage.kihos if x.id == ident][0]
    except:
        return None

def get_spell(storage, ident):
    try:
        return [x for x in storage.spells if x.id == ident][0]
    except:
        return None

def get_merit(storage, ident):
    try:
        return [x for x in storage.merits if x.id == ident][0]
    except:
        return None

def get_flaw(storage, ident):
    try:
        return [x for x in storage.flaws if x.id == ident][0]
    except:
        return None

def get_weapon(storage, name):
    try:
        return [x for x in storage.weapons if x.name == name][0]
    except:
        return None

def get_armor(storage, name):
    try:
        return [x for x in storage.armors if x.name == name][0]
    except:
        return None

def get_weapon_effect(storage, ident):
    try:
        return [x for x in storage.weapon_effects if x.id == ident][0]
    except:
        return None

def get_ring(storage, ident):
    try:
        return [x for x in storage.rings if x.id == ident][0]
    except:
        return None

def get_trait(storage, ident):
    try:
        return [x for x in storage.traits if x.id == ident][0]
    except:
        return None


class DataQuery(object):
    def __init__(self, data):
        self.d = data

    def get_clan(self, ident):
        return get_clan(self.d, ident)

    def get_family(self, ident):
        return get_family(self.d, ident)

    def get_school(self, ident):
        s = get_school(self.d, ident)
        return get_school(self.d, ident)

    def get_base_schools(self):
        return get_base_schools(self.d)

    def get_school_tech(self, school_id, rank):
        school_obj = self.get_school(school_id)
        return get_school_tech(school_obj, rank)

    def get_tech(self, ident):
        return get_tech(self.d, ident)

    def get_skill(self, ident):
        return get_skill(self.d, ident)

    def get_skills(self, categ):
        return get_skills(self.d, categ)

    def get_spells(self, ring, mastery):
        return get_spells(self.d, ring, mastery)

    def get_maho_spells(self, ring, mastery):
        return get_maho_spells(self.d, ring, mastery)

    def get_mastery_ability_rule(self, ident, value):
        return get_mastery_ability_rule(self.d, ident, value)

    def get_kata(self, ident):
        return get_kata(self.d, ident)

    def get_kiho(self, ident):
        return get_kiho(self.d, ident)

    def get_spell(self, ident):
        return get_spell(self.d, ident)

    def get_merit(self, ident):
        return get_merit(self.d, ident)

    def get_flaw(self, ident):
        return get_flaw(self.d, ident)

    def get_weapon(self, name):
        return get_weapon(self.d, name)

    def get_armor(self, name):
        return get_armor(self.d, name)

    def get_weapon_effect(self, ident):
        return get_weapon_effect(self.d, ident)

    def get_ring(self, ident):
        return get_ring(self.d, ident)

    def get_trait(self, ident):
        return get_trait(self.d, ident)
