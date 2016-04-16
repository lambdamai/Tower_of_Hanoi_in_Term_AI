#!/usr/bin/env python3

import AI
import re, copy, sys
import threading
import os, os.path
import time, getopt, random
from help import *


class StoppableThread(threading.Thread):

    def __init__(self, trg, argv):
        super(StoppableThread, self).__init__(target=trg, args=argv)
        self.event = threading.Event()

    def stop(self):
        self.event.set()

    def stopped(self):
        return self.event.isSet()

# Вместо len лучше было бы вставить hoops_number


class stack_pyramid(list):

    def __init__(self, arr=[]):
        self.hoops_number = len(arr)
        list.__init__(self)
        for i in arr:
            self.append(i)

    def push(self, value):
        if not(self.hoops_number) or value <= self[-1]:
            self.hoops_number += 1
            self.append(value)
        else:
            raise Exception("ERROR: YOUR PYRAMID LIKE LEANING TOWER OF PISA")

    def pop(self):
        try:
            elem = self[-1]
            del self[-1]
            self.hoops_number -= 1
            return elem
        except:
            raise Exception("ERROR: EMPTY PYRAMID.")

    def get_top(self):
        try:
            return self[-1]
        except:
            raise Exception("ERROR: EMPTY PYRAMID.")

    def get_all(self):
        return self

    def get_len(self):
        return self.hoops_number


class Game:

    mov_cmd = re.compile('\d+')

    def __init__(self, ai=None, who="Player", amount=3, istream=input, ostream=print, log=0, delay=0, web=False):
        self.status = "Runing"
        self.who = who
        self.istream = istream
        self.ai = ai
        self.rod = amount
        self.lvl = amount + 2
        self.log = log
        self.delay = delay
        self.count = 0
        arr = list(range(self.lvl+1))[1:]
        arr.reverse()
        self.pyramids = [stack_pyramid(copy.copy(arr))]
        for i in range(1, amount):
            self.pyramids.append(stack_pyramid())
        self.win_combination = arr
        self.web = web
        self.flask_thread = None

    def run(self):
        try:
            self.situation()
            self.process()
        except Exception as e:
            raise(e)

    def process(self):

        def create_app(g):
            import webserver
            import logging
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)
            webserver.run(g)

        if self.web:
            self.flask_thread = StoppableThread(create_app, (self,))
            self.flask_thread.daemon = True
            self.flask_thread.start()

        if (self.log == 1):
            f = open('log.txt', 'w')
        while(self.status == "Runing"):
            if self.who == "Player":
                moves = self.istream().lower()
                moves = re.findall(Game.mov_cmd, moves)
                if len(moves) < 2:
                    continue
                for i in range(len(moves)):
                    moves[i] = int(moves[i])
            elif self.who == "AI":
                if self.count > 1000:
                    self.status = "Stopped"
                    print("AI FAILED (TO MANY MOVES)")
                moves = self.ai(self)
            else:
                break
            if(moves[0] > 0 and moves[0] < self.lvl) and (moves[1] > 0 and moves[1] < self.lvl):
                self.count += 1
                from_ = moves[0]-1
                if (self.log == 1):
                    f.write(str(from_))
                to_ = moves[1]-1
                if (self.log == 1):
                    f.write(str(to_)+'\n')
            else:
                print("WRONG MOVE")
            try:
                self.pyramids[to_].push(self.pyramids[from_][-1])
                self.pyramids[from_].pop()
            except:
                if self.who == "AI":
                    self.status = "Stopped"
                    print("AI FAILED (FORBIDDEN MOVE)")
            self.situation()
            time.sleep(self.delay/1000)

    def draw(self):
        os.system('cls')

        print("COUNT: " + str(self.count))
        print("| "*self.rod)
        for g in range(self.lvl):
            for pyramid in self.pyramids:
                try:
                    print(str(pyramid[self.lvl-g-1]), end=" ")
                except IndexError:
                    print("|", end=" ")
            print()

    def situation(self):
        # self.count+=1
        self.draw()
        for i in range(1, len(self.pyramids)):
            if self.pyramids[i] == self.win_combination:
                self.status = "Win"
                print("YOU WIN")


def main(argv):
    # TODO make this import less ugly
    from settings import who, ai, log, web, delay, amount

    try:
        opts, args = getopt.getopt(
            argv, "hrlwd:", ["help", "rules", "ai", "log", "web", "delay=", "amount=", "random"])
    except getopt.GetoptError:
        print(help_text())
        sys.exit(2)

    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help_text())
            sys.exit(2)
        elif opt in ("-r", "--rules"):
            print(rules_text())
            sys.exit(2)
        elif opt in ("--ai"):
            who = "AI"
            ai = AI.AI
        elif opt in ("-l", "--log"):
            log = 1
        elif opt in ("-w", "--web"):
            web = True
        elif opt in ("-d", "--delay"):
            delay = int(arg)
        elif opt in ("-a", "--amount"):
            if int(arg) < 3 or int(arg) > 10:
                raise NameError('Invalid number')
            else:
                amount = int(arg)
        elif opt in ("--random"):
            random.seed()
            amount = random.randint(3, 10)

    game = Game(who=who, ai=ai, log=log, delay=delay, web=web, amount=amount)
    game.run()

if __name__ == "__main__":
    main(sys.argv[1:])
