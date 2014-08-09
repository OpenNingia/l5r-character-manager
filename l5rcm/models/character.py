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

class Traits:
    # earth ring
    STAMINA      = 'stamina'
    WILLPOWER    = 'willpower'

    # air ring
    REFLEXES     = 'reflexes'
    AWARENESS    = 'awareness'

    # water ring
    STRENGTH     = 'strength'
    PERCEPTION   = 'perception'

    # fire ring
    AGILITY      = 'agility'
    INTELLIGENCE = 'intelligence'

    # void ring
    VOID         = 'void'

class OtherTraits:

    # other traits
    HONOR        = 'honor'
    GLORY        = 'glory'
    STATUS       = 'status'
    INFAMY       = 'infamy'
    TAINT        = 'taint'

class Rings:
    EARTH = 'earth'
    AIR   = 'air'
    WATER = 'water'
    FIRE  = 'fire'
    VOID  = 'void'

class RingMap:

    EARTH = ( Traits.STAMINA , Traits.WILLPOWER    )
    AIR   = ( Traits.REFLEXES, Traits.AWARENESS    )
    WATER = ( Traits.STRENGTH, Traits.PERCEPTION   )
    FIRE  = ( Traits.AGILITY , Traits.INTELLIGENCE )
    VOID  = ( Traits.VOID, )

    _map = {
        Rings.EARTH: EARTH,
        Rings.AIR  : AIR  ,
        Rings.WATER: WATER,
        Rings.FIRE : FIRE ,
        Rings.VOID : VOID
    }

    @staticmethod
    def get(ring_id):
        return RingMap._map[ring_id] if ring_id in RingMap._map else None

class Gender:

    UNSPECIFIED = 'unspecified'
    MALE        = 'male'
    FEMALE      = 'female'
    OTHER       = 'other'

class Character(object):

    #base_traits       = {}
    #other_traits      = {}

    #advancements      = []
    #rank_advancements = []

    # this persist how many kiho were bought for free thanks to rank advancements
    #free_kiho_point_spent = 0

    # XP earned ( 40 default from L5R manual )
    #xp_earned             = 40

    # advancement id incremental
    #aid                   = 0

    # character name
    #name                  = ''

    # character gender
    #gender                = Gender.UNSPECIFIED

    def __init__(self):

        self.base_traits = {
            Traits.STAMINA      : 2,
            Traits.WILLPOWER    : 2,

            Traits.REFLEXES     : 2,
            Traits.AWARENESS    : 2,

            Traits.STRENGTH     : 2,
            Traits.PERCEPTION   : 2,

            Traits.AGILITY      : 2,
            Traits.INTELLIGENCE : 2,

            Traits.VOID         : 2
        }

        self.other_traits = {

            OtherTraits.HONOR        : 0.0,
            OtherTraits.GLORY        : 0.0,
            OtherTraits.STATUS       : 0.0,
            OtherTraits.INFAMY       : 0.0,
            OtherTraits.TAINT        : 0.0

        }

        self.advancements      = []
        self.rank_advancements = []

        self.free_kiho_point_spent  = 0
        self.xp_earned              = 40
        self.aid                    = 0
        self.name                   = ''
        self.gender                 = Gender.UNSPECIFIED


class Snapshot(object):

    skills   = {} # id ==> value
    traits   = {} # id ==> value
    rings    = {} # id ==> value

    tags     = [] # tag list
    rules    = [] # rules list

    schools  = {} # id ==> rank

    insight_rank = 0

    model  = None

    honor  = 0.0

    def __init__(self, pc):
        self.model = pc

        for k, v in [ (x, pc.get_skill_rank(x)) for x in pc.get_skills() ]:
            self.skills[k] = v

        for k, v in pc.iter_traits_final():
            self.traits[k] = v

        for k, v in pc.iter_rings():
            self.rings[k] = v

        for k, v in [ (x.school, x.school_rank) for x in pc.iter_rank_advancements() ]:
            print('copy school {} rank {}'.format(k, v))
            if k in self.schools:
                self.schools[k] = max( v, self.schools[k] )
            else:
                self.schools[k] = v

        self.tags  = pc.get_tags ()
        self.rules = pc.get_rules()

        self.insight_rank = pc.get_insight_rank()
        self.honor        = pc.get_honor()

    def get_skills(self):
        return self.model.get_skills()

    def get_skill_rank(self, id_):
        if id_ in self.skills:
            return self.skills[id_]
        return 0

    def set_skill_rank(self, id_, val):
        self.skills[id_] = val

    def get_ring_rank(self, id_):
        if id_ in self.rings:
            return self.rings[id_]
        return 0

    def set_ring_rank(self, id_, val):
        self.rings[id_] = val

    def get_trait_rank(self, id_):
        if id_ in self.traits:
            return self.traits[id_]
        return 0

    def set_trait_rank(self, id_, val):
        self.traits[id_] = val

    def has_tag(self, tag):
        return tag in self.tags

    def has_rule(self, rule):
        return rule in self.rules

    def get_schools(self):
        return self.schools.keys()

    def get_school_rank(self, id_):
        if id_ in self.schools:
            return self.schools[id_]
        return 0

    def set_school_rank(self, id_, val):
        self.schools[id_] = val

    def get_skill_emphases(self, skid):
        return self.model.get_skill_emphases(skid)

    def get_insight_rank(self):
        return self.insight_rank

    def get_honor(self):
        return self.honor
