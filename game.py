from game_players import *
import choosers
import os
from datetime import datetime

class Game(object):
	def __init__(self, statisstic_logger, bot, player_name = 'Anon'):
		self.new(player_name)
		self.statisstic_logger = statisstic_logger
		self.bot = bot
		self.chat_id = 0
		self.uinput = 'none'
		
	def bprint(self, text):
		self.bot.send_message(self.chat_id, text)

	def new(self, player_name = 'Anon'):
		self.players = [Man(player_name, choosers.StdinChooser(0,5, self)),
				Comp(choosers.MyChooser(0,5))]
		self.stats = [0, 0]

	def print_chips(self):
		self.bprint('{2}:\t{0}\n{3}:\t{1}'.format(self.players[0], self.players[1],
						    self.players[0].name, self.players[1].name))

	def ask_chip(player):
		while True:
			p = player.choice()
			#print(p)
			if p == 666:
				return p;
			if p == 'none':
				return p;
			if player.take(p):
				break
		return p

	def give_back(self, p0, p1):
		self.players[0].chips[p0] = True
		self.players[1].chips[p1] = True

	def end(self):
		winner = 0
		looser = 1

		if self.stats[1] > self.stats[0]:
			winner = 1
			looser = 0
		elif self.stats[1] == self.stats[0]:
			return False
		if self.uinput != 'new':
			self.bprint("Player {0} takes all!\n".format(self.players[winner].name))
		self.statisstic_logger.addGame(self.players[winner], self.players[looser],
				               self.stats[winner], self.stats[looser],
				               datetime.now().__str__());
		return True

	def __str__(self):
		return "\n*** Score ***\n {0}:\t{1}\n{2}:\t{3}".format(self.players[0].name, self.stats[0],
						                       self.players[1].name, self.stats[1])

	def start(self, presenter):
		pass

	def start(self):
		#self.bprint('*** {0} vs. {1} ***'.format(self.players[0].name, self.players[1].name))
		#self.print_chips()
		while True:
			#os.system('clear')
			if self.uinput == 'none':
				self.bprint(self)
			if self.players[0].check_chips() == False:
				if self.end():
					return
				else:
					self.new(self.players[0].name)
			
			if self.uinput == 'none':
				self.print_chips()
			#print('\nYour chips:')
			#print(self.players[0])
			p0 = Game.ask_chip(self.players[0])
			if p0 == 'none':
				self.bprint('Enter num from {0} to {1}'.format(0 + 1,
						   5 + 1))
				return 0;
			if p0 == 666:
				self.statisstic_logger.write_file()
				self.bprint('bye!')
				return 1
			p1 = Game.ask_chip(self.players[1])
			if p0 < p1:
				winner = self.players[1]
				self.stats[1] += p0 + p1 + 2
			elif p0 > p1:
				winner = self.players[0]
				self.stats[0] += p0 + p1 + 2
			else:
				self.bprint("Draw\n")
				if self.players[0].check_chips() == False:
					self.end()
					return
				self.give_back(p0, p1)
				continue
			self.bprint("Player {0} wins!\n".format(winner.name))
			self.uinput = 'none'
