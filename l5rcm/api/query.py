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

from models import character

from . import (
    insight,
    kiho,
    kata )

class pc_query(object):

    def __init__(self, pc, data):
        self.pc      = pc
        self.data    = data
        self.insight = insight.InsightCalculator(self)
        self.kiho    = kiho.Kiho(self, data)
        self.kata    = kata.Kata(self, data)

    def get_current_clan(self):
        '''The clan is decided on the first character advancement'''
        adv = self.get_first_rank_advancement()
        if adv: return adv.clan
        return None

    def get_current_family(self):
        adv = self.get_first_rank_advancement()
        if adv: return adv.family
        return None

    def get_first_school(self):
        adv = self.get_first_rank_advancement()
        if adv: return adv.school
        return None

    def get_current_school(self):
        adv = self.get_last_rank_advancement()
        if adv: return adv.school
        return None

    def get_clan_trait(self):
        '''not implemented'''
        return None

    def get_family_trait(self):
        family     = self.get_current_family()
        if not family: return None
        family_dal = self.data.query.get_family(family)
        if family_dal: return family_dal.trait
        return None

    def get_school_trait(self):
        school     = self.get_first_school()
        if not school: return None
        school_dal = self.data.query.get_school(school)
        if school_dal: return school_dal.trait
        return None

    def get_trait_rank(self, trait_id):
        trait_value = self.pc.base_traits[trait_id] if trait_id in self.pc.base_traits else 0

        # NB. clan, family and school trait are inherited from the
        # character creation school ( i.e. the first advancement )

        # clan trait bonus will be probably == None in most cases
        if self.get_clan_trait() == trait_id:
            trait_value += 1

        # assumption: family trait bonus grants +1 on trait
        if self.get_family_trait() == trait_id:
            trait_value += 1

        # assumption: school trait bonus grants +1 on trait
        if self.get_school_trait() == trait_id:
            trait_value += 1

        trait_value += sum( [1 for x in self.iter_advancements('trait') if x.trait_id == trait_id] )

        return trait_value

    def get_trait_rank_final(self, trait_id):
        trait_value = self.get_trait_rank(trait_id)

        weakness_flaw = 'weak_{}'.format(trait_id)

        if self.has_rule(weakness_flaw):
            trait_value -= 1

        return trait_value

    def get_other_trait_value(self, trait_id):
        trait_value = self.pc.other_traits[trait_id] if trait_id in self.pc.other_traits else 0.0
        trait_value += sum( [0.1 for x in self.iter_advancements('trait') if x.trait_id == trait_id] )
        return trait_value

    def get_name (self):
        return self.pc.name
        
    def get_honor(self):
        return self.get_other_trait_value('honor')

    def get_glory(self):
        return self.get_other_trait_value('glory')

    def get_taint(self):
        return self.get_other_trait_value('taint')

    def get_status(self):
        return self.get_other_trait_value('status')

    def get_infamy(self):
        return self.get_other_trait_value('infamy')

    def get_skill_rank(self, skill_id):
        '''returns the skill rank on the given skill or 0 if the skill is not learned'''
        return sum( [1 for x in self.iter_advancements('skill') if x.skill_id == skill_id] )

    def get_ring_rank(self, ring_id):
        traits = character.RingMap.get(ring_id)
        if not traits: return 0
        return min( [self.get_trait_rank(x) for x in traits] )

    def get_void_rank(self):
        return self.get_ring_rank( character.Rings.VOID )

    def get_xp_spent(self):
        return sum( [x.cost for x in self.pc.advancements] )

    # TAG & RULES
    def is_monk(self):
        '''returns True if the pc has joined at least one monk school'''
        monk_schools = [ x for x in self.iter_rank_advancements() if 'monk' in x.tags ]
        return len(monk_schools) > 0

    def is_brotherhood(self):
        '''returns True if the pc has joined at least one brotherhood monk school'''
        if not self.is_monk(): return False

        brotherhood_schools = [ x for x in self.iter_rank_advancements() if 'brotherhood' in x.tags ]
        is_brotherhood      = len(brotherhood_schools) > 0

        # a friend of the brotherhood pay the same as the brotherhood members
        is_brotherhood = is_brotherhood or self.has_rule('friend_brotherhood')

        return is_brotherhood

    def is_ninja(self):
        '''returns True if the pc has joined at least one ninja school'''
        ninja_schools = [ x for x in self.iter_rank_advancements() if 'ninja' in x.tags ]
        return len(ninja_schools) > 0

    def get_school_rank_sum(self, tag):
        '''returns the school rank sum of school of the given tag'''
        return sum([1 for x in self.iter_rank_advancements() if tag in x.tags ])

    def is_shugenja(self):
        '''returns True if the pc has joined at least one shugenja school'''
        shugenja_schools = [ x for x in self.iter_rank_advancements() if 'shugenja' in x.tags ]
        return len(shugenja_schools) > 0

    def is_bushi(self):
        '''returns True if the pc has joined at least one bushi school'''
        bushi_schools = [ x for x in self.iter_rank_advancements() if 'bushi' in x.tags ]
        return len(bushi_schools) > 0

    def is_courtier(self):
        '''returns True if the pc has joined at least one courtier school'''
        courtier_schools = [ x for x in self.iter_rank_advancements() if 'courtier' in x.tags ]
        return len(courtier_schools) > 0

    def get_insight(self):
        return self.insight.calculate()

    def get_insight_rank(self):
        return self.insight.calculate_rank()

    def get_rules(self):
        return self.get_techs() + self.get_mastery_abilities() + self.get_merits() + self.get_flaws()

    def get_school_tags(self):
        lol = [x.tags for x in self.pc.rank_advancements]
        return [y for x in lol for y in x]

    def get_techs(self):
        return [x.tech for x in self.pc.rank_advancements]

    def get_skills(self):
        distinct_skill_list = []
        for a in self.pc.rank_advancements:
            distinct_skill_list += [x for x in a.skills if x not in distinct_skill_list]
        distinct_skill_list += [x.skill_id for x in self.iter_advancements('skill') if x.skill_id not in distinct_skill_list]
        return distinct_skill_list

    def get_mastery_abilities(self):
        mal = []
        for x in self.get_skills():
            for i in range(0, self.get_skill_rank(x)):
                ma = self.data.query.get_mastery_ability_rule(x, i+1)
                if ma: mal.append(ma)
        return mal

    def get_merits(self):
        return [x.perk_id for x in self.iter_advancements('perk') if x.tag == 'merit']

    def get_flaws(self):
        return [x.perk_id for x in self.iter_advancements('perk') if x.tag == 'flaw']

    def get_kiho(self):
        return [x.kiho_id for x in self.iter_advancements('kiho')]

    def get_kata(self):
        return [x.kata_id for x in self.iter_advancements('kata')]

    def get_tags (self):
        return self.get_school_tags() + [self.get_current_clan()] + [self.get_current_family()]

    def has_rule(self, rule_id):
        return rule_id in self.get_rules()

    def has_tag(self, tag_id):
        return tag_id in self.get_tags()

    def cnt_rule(self, rule_id):
        return self.get_rules().count(rule_id)

    # HELPERS

    def iter_advancements(self, adv_type):
        for a in self.pc.advancements:
            if adv_type == a.tag: yield a

    def iter_rank_advancements(self):
        for a in self.pc.rank_advancements:
            yield a

    def iter_traits(self):
        import inspect
        for k, v in inspect.getmembers( character.Traits ):
            if not k.startswith('__'):
                yield v, self.get_trait_rank(v)

    def iter_rings(self):
        import inspect
        for k, v in inspect.getmembers( character.Rings ):
            if not k.startswith('__'):
                yield v, self.get_ring_rank(v)

    def iter_traits_final(self):
        import inspect
        for k, v in inspect.getmembers( character.Traits ):
            if not k.startswith('__'):
                yield v, self.get_trait_rank_final(v)

    def get_advancements(self, tag):
        return [x for x in self.pc.advancements if x.tag == tag]

    def get_rank_advancements(self):
        return self.pc.rank_advancements

    def get_last_advancement(self):
        if len( self.pc.advancements ):
            return self.pc.advancements[-1]
        return None

    def get_first_rank_advancement(self):
        if len( self.pc.rank_advancements ):
            return self.pc.rank_advancements[0]
        return None

    def get_last_rank_advancement(self):
        if len( self.pc.rank_advancements ):
            return self.pc.rank_advancements[-1]
        return None
