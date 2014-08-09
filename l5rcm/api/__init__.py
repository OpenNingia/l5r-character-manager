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

import warnings
import logging
import dal

# from PyQt5 import QtCore

from models import character
from models.character import Character

from models.advancements.rank import (
    Rank,
    StartingSkill,
    CustomStartingSkill )

from . import (
    constants,
    kiho,
    kata,
    requirements )


class L5R(object):

    def __init__(self):
        super(L5R, self).__init__()

        self.pc     = None
        self.data   = None
        self.locale = 'en'
        self.log    = logging.getLogger('api')

        self.load_data()
        self.new_pc()

    def load_data(self):
        '''loads data from installed data packs'''
        # Data storage
        if not self.data:
            self.data = dal.Data(
                [dal.get_path('core.data'),
                 dal.get_path('data'),
                 dal.get_path('data.' + self.locale)],
                 [])
        else:
            self.log.debug('Re-loading datapack data')

            self.dstore.rebuild(
                    [osutil.get_user_data_path('core.data'),
                    osutil.get_user_data_path('data'),
                    osutil.get_user_data_path('data.' + self.locale)],
                    self.data_pack_blacklist)

    def new_pc(self):
        '''creates a new pc, discarding the old one'''
        from .query  import pc_query

        self.pc      = Character()
        self.query   = pc_query(self.pc, self.data)

        self.log.info('Created new character')

    def create_rank_advancement(self):
        '''start a rank advancement'''
        r =  Rank()
        r.rank = self.query.get_insight_rank()
        return r

    def get_missing_requirements_to_join_school(self, school_id):
        '''get missing requirements, however the role playing ones are automatically accepted'''

        from .requirements import RequirementSet

        # get the school dal
        school_dal = self.data.query.get_school( school_id )

        # get school requirements
        requirements = RequirementSet(self.query, self.data, school_dal.require)

        # rpg requirements automatically passes
        requirements.add_manual_match('rpg')

        # get missing requirements
        is_match, missing_requirements = requirements.match_all()

        return missing_requirements

    def commit_rank_advancement(self, advancement):
        '''ends the given rank advancement'''

        is_first_advancement = len(self.pc.rank_advancements) == 0
        previous_advancement = None if is_first_advancement else self.pc.rank_advancements[-1]

        is_same_school       = False
        if previous_advancement and previous_advancement.school == advancement.school:
            is_same_school = True

        if is_first_advancement:
            self.first_rank_advancement_setup( advancement )

        # get the school dal
        school_dal = self.data.query.get_school( advancement.school )

        # set any tags that the school grants
        advancement.tags = school_dal.tags

        # add school id to tags
        advancement.tags += [school_dal.id]

        # free kihos
        advancement.free_kiho_count = school_dal.kihos.count if school_dal.kihos else 0

        # some (dragon) school grants free tattoos also
        # however the dal cannot cover it, so I hardcode that for now
        # TODO.

        # the school rank is given by the past advancements in the same school plus 1
        advancement.school_rank = sum( [1 for x in self.pc.rank_advancements if x.school == advancement.school ] ) + 1

        # the tech is given by the school and its rank, it can be calculated so the persistance is for commodity reasons
        # if can be None of course if the rank don't grant any technique
        tech_dal         = self.data.query.get_school_tech(advancement.school, advancement.school_rank)
        advancement.tech = tech_dal.id if tech_dal else None

        # is the school an alternate path?
        advancement.is_alternate_path = 'alternate' in school_dal.tags

        # if this is an alternate path we should persiste the original school
        # if this is school_rank 1 then we take that from the previous advancement school
        # otherwise from the previous advancement original school
        if advancement.is_alternate_path:
            if advancement.school_rank == 1:
                advancement.original_school = previous_advancement.school
            else:
                advancement.original_school = previous_advancement.original_school

        self.pc.rank_advancements.append(advancement)

    def first_rank_advancement_setup(self, advancement):
        '''setup the rank advancement with stuff that only happen on the first one'''

        # get the school dal
        school_dal = self.data.query.get_school( advancement.school )

        if not school_dal:
            raise Exception('school not found {}'.format(advancement.school))

        # set the school trait
        advancement.trait = school_dal.trait

        # set the school starting skill
        advancement.skills = [ StartingSkill(x.id, x.rank, x.emph) for x in school_dal.skills ]

        # set the school starting custom skill wildcards if any
        advancement.custom_skills = []
        for sset in school_dal.skills_pc:
            options = [ (x.value, x.modifier) for x in sset.wildcards ]
            advancement.custom_skills.append(CustomStartingSkill(options, sset.rank))

        # set the school starting spells
        advancement.spells = [ x.id for x in school_dal.spells ]

        # set the school starting custom spells wildcards if any
        advancement.custom_spells = [ CustomStartingSpells(x.element, x.tag, x.element) for x in school_dal.spells_pc ]

        # the first rank adds honor too
        advancement.honor = school_dal.honor

        # ...and the equipment
        advancement.equip = school_dal.outfit

        # ...and the starting money
        advancement.money = school_dal.money

        # one might want to join a path immediately at the rank 1

    ## XP MANAGEMENT ##

    def set_xp_limit(self, value):
        '''set the maximum experience points a player can spent on advancements'''
        self.pc.xp_earned = value

    def get_xp_limit(self):
        '''returns the value sets by set_xp_limit'''
        return self.pc.xp_earned

    def get_xp_spent(self):
        '''calculate and return the XP spent in advancements'''
        return self.query.get_xp_spent()

    def has_enough_xp(self, xp):
        '''helper function to check if the player has enought xp to spent'''
        return self.get_xp_limit() - ( self.get_xp_spent() + xp ) >= 0

    def append_advancement(self, adv):
        '''append an advancement to the advancement list'''
        self.pc.advancements.append(adv)
        return adv

    def increase_skill(self, skill_id, new_rank = None):
        '''increase a skill rank, or set the new rank'''
        if not new_rank:
            # calculate new_rank
            cr       = self.query.get_skill_rank(skill_id)
            new_rank = cr + 1
        from models.advancements import skill
        return self.append_advancement( skill.Skill( self.__next_aid(), skill_id, new_rank ) )

    def increase_trait(self, trait_id, new_rank = None):
        '''increase a trait rank, or set the new rank'''
        if not new_rank:
            # calculate new_rank
            cr       = self.query.get_trait_rank(trait_id)
            new_rank = cr + 1
        from models.advancements import trait
        return self.append_advancement( trait.Trait( self.__next_aid(), trait_id, new_rank ) )

    def increase_void(self, new_rank = None):
        '''increase void rank, or set the new rank'''
        return self.increase_trait(character.Traits.VOID)

    def buy_skill_rank(self, skill_id):
        '''increase a skill rank by 1 only if the pc has enough xp'''
        cr   = self.query.get_skill_rank(skill_id)
        nr   = cr + 1
        cost = constants.INCREASE_SKILL_COST * nr

        if self.has_enough_xp(cost):
            adv = self.increase_skill(skill_id, nr)
            adv.cost = cost
            return True
        return False

    def buy_trait_rank(self, trait_id):
        '''increase a trait rank by 1 only if the pc has enough xp'''
        cr   = self.query.get_trait_rank(trait_id)
        nr   = cr + 1
        cost = constants.INCREASE_TRAIT_COST * nr

        if self.has_enough_xp(cost):
            adv = self.increase_trait(trait_id, nr)
            adv.cost = cost
            return True

        warnings.warn('character has not enough xp to increase trait {} to {}'.format(trait_id, nr))

        return False

    def buy_void_rank(self):
        '''increase the void rank by 1 only if the pc has enough xp'''
        cr   = self.query.get_trait_rank(character.Traits.VOID)
        nr   = cr + 1
        cost = constants.INCREASE_VOID_COST * nr

        if self.has_enough_xp(cost):
            adv = self.increase_void(nr)
            adv.cost = cost
            return True
        return False

    def add_skill_emphasis(self, skill_id, emphasis):
        '''add an emphasis to a skill'''

        skill_dal = self.data.query.get_kiho(skill_id)
        if not skill_dal:
            raise skill.SkillNotFound(skill_id)

        import models.advancements.skill as adv_skill
        return self.append_advancement( adv_skill.Emphasis( self.__next_aid(), skill_id, emphasis ) )

    def buy_skill_emphasis(self, skill_id, emphasis):
        '''buy an emphasis if the player has enough xp left'''

        cost = constants.EMPHASIS_COST

        if self.has_enough_xp(cost):
            adv = self.add_skill_emphasis(skill_id, emphasis)
            adv.cost = cost
            return True
        return False

    def add_kiho(self, kiho_id):
        '''add a kiho'''

        kiho_dal = self.data.query.get_kiho(kiho_id)
        if not kiho_dal:
            raise kiho.KihoNotFound(kiho_id)

        from models.advancements import powers
        return self.append_advancement( powers.Kiho( self.__next_aid(), kiho_id ) )

    def buy_kiho(self, kiho_id):
        '''buy a kiho if the player has enough xp and if the character is eligible'''

        kiho_status = self.query.kiho.check_status()
        if kiho_status == Kiho.ST_ERROR:
            return False
        kiho_eligibility, reason = self.query.kiho.check_eligibility(kiho_id)
        if not kiho_eligibility:
            return False
        cost = self.query.kiho.calculate_cost(kiho_id)

        if self.has_enough_xp(cost):
            adv = self.add_kiho(kiho_id)
            adv.cost = cost
            return True
        return False        

    def add_kata(self, kata_id):
        '''add a kata'''

        kata_dal = self.data.query.get_kata(kata_id)
        if not kata_dal:
            raise kata.KihoNotFound(kata_id)

        from models.advancements import powers
        return self.append_advancement( powers.Kata( self.__next_aid(), kata_id ) )

    def buy_kata(self, kata_id):
        '''buy a kata if the player has enough xp and if the character is eligible'''

        eligibility, matched_requirement = self.query.kata.check_eligibility(kata_id)
        if not eligibility:
            warnings.warn('the character is not eligible to learn the {} kata'.format(kata_id))
            return False

        cost = self.query.kata.calculate_cost(kata_id)

        if self.has_enough_xp(cost):
            adv = self.add_kata(kata_id)
            adv.cost = cost                    
            return True

        warnings.warn('the character has not enough xp to learn the {} kata'.format(kata_id))
        return False  


    def add_spell(self, spell_id):

        spell_dal = self.data.query.get_spell(spell_id)
        if not spell_dal:
            raise spell.SpellNotFound(spell_id)

        from models.advancements import powers
        return self.append_advancement( powers.Spell( self.__next_aid(), spell_id ) )

    #def remove_spell(self, spell_id):
    #    pass

    def add_memorized_spell(self, spell_id):

        spell_dal = self.data.query.get_spell(spell_id)
        if not spell_dal:
            raise spell.SpellNotFound(spell_id)

        from models.advancements import powers
        return self.append_advancement( powers.MemorizedSpell( self.__next_aid(), spell_id ) )

    def buy_memorized_spell(self, spell_id):

        cost = constants.MEMORIZED_SPELL_COST

        if self.has_enough_xp(cost):
            adv = self.add_memorized_spell(spell_id)
            adv.cost = cost
            return True
        return False 

    def undo_advancement(self):
        '''undo the last advancement'''
        adv = self.query.get_last_advancement()
        if adv: del self.pc.advancements[-1]

    def undo_rank_advancement(self):
        '''undo the last rank advancement'''
        adv = self.query.get_last_rank_advancement()
        if adv: del self.pc.rank_advancements[-1]
        print( 'adv qty', len(self.pc.rank_advancements) )

    ### HELPERS ###
    def __next_aid(self):
        self.pc.aid += 1
        return self.pc.aid