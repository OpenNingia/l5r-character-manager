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

class Rank(object):
    def __init__(self):

    	# the clan
        self.clan        = None
        # the family
        self.family      = None
        # the target school
        self.school      = None
        # the insight rank
        self.rank        = 0
        # the school rank
        self.school_rank = 0
        # the learned tech
        self.tech        = None
        # is 'school' an alternate path
        self.is_alternate_path  = False
        # the original school
        self.original_school    = None
        # the character left an alternate path
        self.left_alternate_path = False
        # skills
        self.skills = []


        out['clan']                = self.clan
    def to_dict(self):
        out = {}
        out['family']              = self.family
        out['school']              = self.school
        out['rank']                = self.rank
        out['school_rank']         = self.school_rank
        out['tech']                = self.tech
        out['is_alternate_path']   = self.is_alternate_path
        out['original_school']     = self.original_school
        out['left_alternate_path'] = self.left_alternate_path
        out['skills']              = []

        for s in self.skills:
            out['skills'].append( s.to_dict() )

        return out


class StartingSkill(object):
    def __init__(self, skill_id, rank = 1, emphasis = None):
        self.skill_id = skill_id
        self.rank     = rank
        self.emphasis = emphasis

    def to_dict(self):
        out = {}
        out['skill_id'] = self.skill_id
        out['rank'    ] = self.rank
        out['emphasis'] = self.emphasis

        return out


class CustomStartingSkill(object):
    def __init__(self, options, rank = 1):
        self.rank     = rank
        self.options  = options # ( value, modifier )
        #self.value    = value
        #self.modifier = modifier

    def to_dict(self):
        out = {}
        out['rank'    ] = self.rank
        out['options' ] = self.options

        return out

class CustomStartingSpells(object):
    def __init__(self, element, tag, count = 1):
        self.element  = element
        self.tag      = tag
        self.count    = count

    def to_dict(self):
        out = {}
        out['element'] = self.element
        out['tag'    ] = self.tag
        out['count'  ] = self.count

        return out
