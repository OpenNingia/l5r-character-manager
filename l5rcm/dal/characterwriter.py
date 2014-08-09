# -*- coding: utf-8 -*-
# Copyright (C) 2014 Daniele Simonetti

class CharacterWriter(object):

    SAVE_FILE_VERSION = "4.0"

    def __init__(self, model = None):
        self._model = model

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    def to_dict(self):

        if not self._model:
            raise Exception('Model is None')

        obj            = {}
        obj['version'] = self.SAVE_FILE_VERSION

        self.__fill_base_traits      ( obj )
        self.__fill_rank_advancements( obj )
        self.__fill_stat_advancements( obj )
        self.__fill_character_info   ( obj )
        self.fill_game_info          ( obj )

        #self.fill_schools       ( obj )
        #self.fill_advancements  ( obj )
        #self.fill_outfit        ( obj )
        #self.fill_modifiers     ( obj )

        return obj

    def __fill_base_traits(self, obj):
        obj['base_traits' ] = self.model.base_traits
        obj['other_traits'] = self.model.other_traits

    def __fill_rank_advancements(self, obj):
        ranks = []
        for a in self.model.rank_advancements:
            ranks.append( a.to_dict() )
        obj['rank_advancements'] = ranks

    def __fill_stat_advancements(self, obj):
        stats = []
        for a in self.model.advancements:
            stats.append( a.to_dict() )

        obj['stat_advancements'] = stats


    def __fill_character_info(self, obj):

        char_info = {}
        char_info['name'  ] = self.model.name
        char_info['gender'] = self.model.gender
        char_info['aid'   ] = self.model.aid

        obj['info'] = char_info

    def __fill_game_info(self, obj):

        game_info = {}
        game_info['free_kiho_point_spent'] = self.model.free_kiho_point_spent
        game_info['xp_earned'            ] = self.model.xp_earned

        obj['game_info'] = game_info
