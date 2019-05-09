# encoding : UTF-8

from Settings import *


class ActionObject:
	def __init__(self, player_id=PlayerId.PLAYER_ID_ALL):
		self.player_id = player_id
		
	def update_actions(self, action_events, **kwargs):
		assert -1, "method to implement"
		
	def filter_action_events_by_player_id(self, action_events, use_player_id_all=True):
		filtered_action_events = []
		
		for ev in action_events:
			if self.player_id in (ev.player_id, PlayerId.PLAYER_ID_ALL) \
					or ((ev.player_id == PlayerId.PLAYER_ID_ALL) and use_player_id_all):
				filtered_action_events.append(ev)
				
		return filtered_action_events
	