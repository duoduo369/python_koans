#!/usr/bin/env python
# -*- coding: utf-8 -*-

# EXTRA CREDIT:
#
# Create a program that will play the Greed Game.
# Rules for the game are in GREED_RULES.TXT.
#
# You already have a DiceSet class and score function you can use.
# Write a player class and a Game class to complete the project.  This
# is a free form assignment, so approach it however you desire.

from functools import partial
from collections import Counter
from itertools import izip

from runner.koan import *
from koans.about_dice_project import DiceSet
from koans.about_scoring_project import score


class Player(object):

    def __init__(self, name, dice_number=5):
        super(Player, self).__init__()
        self._name = name
        self._dice_set = DiceSet()
        self._next_dice_number = dice_number
        self._records = []  # 记录每次点数
        self.score = 0
        self.is_alive = True
        self.inited_game = False

    @property
    def name(self):
        """player的名字"""
        return self._name

    @property
    def records(self):
        """每次摇骰子的记录 --> [[1, 3, 2, 1, 4],[1, 2, 3]]"""
        return self._records

    def roll(self):
        """player摇一次骰子

        会将这次摇骰子的结果添加到records列表中保存

        """
        record = self._dice_set.roll(self._next_dice_number)
        self._records.append(record)
        return record

    def set_next_dice_number(self, dice_number):
        """设置下次可以摇的骰子数目"""
        self._next_dice_number = dice_number

    def __str__(self):
        return '<选手 {0}: 总分{1}>\n记录({2})'.format(
            self.name,
            self.score,
            len(self.records)
        )


class Game(object):

    def __init__(self, num=2):
        super(Game, self).__init__()
        self._rounds = 0
        self._players = {i: Player(i) for i in xrange(num)}  # 所有playler列表
        self._in_game_players = self._players.copy()  # 开始所有player都有游戏资格
        self._finish_game_players = {}  # 失去游戏资格的人员
        self._top_score_player = None
        self._final_round = False

    @property
    def playing_number(self):
        """参见游戏的人数"""
        return len(self._players)

    @property
    def rounds(self):
        """第几轮游戏"""
        return self._rounds

    def runner(self):
        """游戏模拟

        胜利条件：
            1.如果有人到3000以上，最后一轮后得分高者获胜
            2.如果所有游戏者都失去资格，得分最高者胜利。
        """

        while not self._final_round and self._in_game_players:
            self.roll()
            if self._top_score_player and \
                    self._top_score_player.score > 3000:
                self._final_round = True

        if self._final_round:
            self.roll()

        return self._top_score_player

    def roll(self):
        """进行一轮游戏"""
        self._rounds += 1

        for i, p in self._in_game_players.iteritems():
            record = p.roll()  # 摇骰子
            score_ = score(record)  # 统计得分
            if not p.inited_game and score_ < 300:
                continue
            p.inited_game = True
            p.score += score_  # 只有init_game的player才能得分
            if not self._top_score_player or \
                    self._top_score_player.score < p.score:  # 更新最高分player
                self._top_score_player = p
            next_dice_number = self.next_dice_number(record, score_)
            # 下次可以摇几个骰子

            if next_dice_number == 0:
                p.is_alive = False
                self._finish_game_players[i] = p
            else:
                p.set_next_dice_number(next_dice_number)

        self._in_game_players = {i: p for i, p in
                                 self._in_game_players.iteritems() if
                                 p.is_alive}

    def next_dice_number(self, record, score):
        """获得下一次可以摇的骰子数目"""
        assert isinstance(record, (list, tuple))
        assert isinstance(score, int)
        if score == 0:  # 得分为0，丧失资格
            return 0
        counter = Counter(record)
        next_number = len(record)
        for num, times in counter.iteritems():
            if times >= 3:
                if num == 1 or num == 5:
                    next_number -= times
                else:
                    next_number -= 3
            else:
                if num == 1 or num == 5:
                    next_number -= times

        if next_number == 0:  # 如果所有骰子都记分了，获得5枚骰子资格
            next_number = 5

        assert next_number > 0, 'next_number应该大于0'
        return next_number

    def records(self, detail=False):
        """获得游戏的详细记录

        detail=True,则返回所有player的骰子记录

        """
        result = ['{0}轮:比赛  共有{1}名选手\n'.format(
            self.rounds,
            self.playing_number
        )]
        for i, p in self._players.iteritems():
            if detail:
                result.append('选手{0}: 总成绩{1} 历次成绩({2}) {3}'.format(
                    i, p.score, len(p.records), p.records)
                )
            else:
                result.append('选手{0}: 总成绩{1} 历次成绩({2})'.format(
                    i, p.score, len(p.records))
                )

        return '\n'.join(result)

    def __str__(self):
        return '第{0}轮\n'.format(self.rounds)


def new_game(n, detail_records=False):
    """测试用"""
    game = Game(n)
    winner = game.runner()
    print game.records(detail_records)
    print '优胜者 ', winner


if __name__ == '__main__':
    new_game(5)


class AboutExtraCredit(Koan):
    # Write tests here. If you need extra test classes add them to the
    # test suite in runner/path_to_enlightenment.py

    def test_player_roll(self):
        player = Player('player')
        self.assertEqual(player._next_dice_number, len(player.roll()))

    def test_player_records(self):
        player = Player('player')
        self.assertEqual(player.records, [player.roll()])

    def test_next_dice_number(self):
        game = Game()
        records = [
            [4, 3, 2, 4, 1],
            [1, 3, 6, 3, 2],
            [5, 3, 3, 2, 1],
            [3, 2, 3, 6, 6],
            [5, 1],
            [5, 5, 3, 6, 4],
            [3, 3, 2]
        ]
        next_dice_number = [
            4,
            4,
            3,
            0,
            5,
            3,
            0
        ]
        for num, record in izip(next_dice_number, records):
            self.assertEqual(num, game.next_dice_number(record, score(record)))
