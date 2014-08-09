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

class InsightCalculator(object):

    MODE1 = 1,
    MODE2 = 2,
    MODE3 = 3

    def __init__(self, model):
        self.mode  = InsightCalculator.MODE1
        self.model = model

    def calculate(self):
        if self.mode == InsightCalculator.MODE1:
            return self.insight_calculation_1()
        if self.mode == InsightCalculator.MODE2:
            return self.insight_calculation_2()
        if self.mode == InsightCalculator.MODE3:
            return self.insight_calculation_3()
        return 0

    def calculate_rank(self):
        value = self.calculate()

        if value > 349:
            return int((value - 349)/25 + 10)
        if value > 324: return 9
        if value > 299: return 8
        if value > 274: return 7
        if value > 249: return 6
        if value > 224: return 5
        if value > 199: return 4
        if value > 174: return 3
        if value > 149: return 2
        return 1

    def get_current_rank(self):
        '''Returns current character Insight Rank'''

        last_rank_advancement = model.get_last_rank_advancement()
        return last_rank_advancement.rank

    def insight_calculation_1(self):
        '''Default insight calculation method = Rings*10+Skills+SpecialPerks'''

        model = self.model
        n = 0
        for r, v in model.iter_rings():
            n += v *10
        for s in model.get_skills():
            n += model.get_skill_rank(s)

        n += 3*model.cnt_rule('ma_insight_plus_3')
        n += 7*model.cnt_rule('ma_insight_plus_7')

        return n

    def insight_calculation_2(model):
        '''Another insight calculation method. Similar to 1, but ignoring
           rank 1 skills
        '''

        model = self.model
        n = 0
        for r, v in model.iter_rings():
            n += v *10
        for s in model.get_skills():
            sk = model.get_skill_rank(s)
            if sk > 1:
                n += sk

        n += 3*model.cnt_rule('ma_insight_plus_3')
        n += 7*model.cnt_rule('ma_insight_plus_7')

        return n

    def insight_calculation_3(model):
        '''Another insight calculation method. Similar to 2, but
           school skill are counted even if rank 1
        '''

        model = self.model
        school_skills = model.get_school_skills()

        n = 0
        for r, v in model.iter_rings():
            n += v *10
        for s in model.get_skills():
            sk = model.get_skill_rank(s)
            if sk > 1 or s in school_skills:
                n += sk

        n += 3*model.cnt_rule('ma_insight_plus_3')
        n += 7*model.cnt_rule('ma_insight_plus_7')

        return n