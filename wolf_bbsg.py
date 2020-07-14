# coding UTF-8
import csv
from typing import Dict, Any
import pandas as pd
import re
import requests
import time
from bs4 import BeautifulSoup


class WolfBBsg:

    def __init__(self, village_number):
        self.village_number = village_number
        self.agent_role = {}  # 役職
        self.players = 0  # プレイヤー人数
        self.sud_death = False  # 突然死があったかどうか
        self.prologue_url = "http://www.wolfg.x0.com/index.rb?vid={0}&meslog=000_ready".format(village_number)
        self.epilogue_url = ""
        self.last_day = 0  # 何日までやったか
        self.winner = ""  # 勝者の陣営
        self.missing = False  # 初日に失踪があったかどうか

        # インスタンスメソッド
        self.set_missing()
        self.get_epilogue_url()
        self.set_sud_death()
        self.set_winner()
        self.set_role()

    def get_epilogue_url(self):
        for day_number in range(0, 15):  # エピローグの探索
            epi_url: str = "http://www.wolfg.x0.com/index.rb?vid={0}&meslog=00{1}_party".format(self.village_number,
                                                                                                day_number)
            req_url = requests.get(epi_url)
            soup = BeautifulSoup(req_url.text, "lxml")
            announce = soup.find("body").find("div", class_="announce")
            if announce is not None:
                self.epilogue_url = epi_url
                self.last_day = day_number
                print(epi_url)

        return

    def set_role(self):
        name_list = []
        role_list = []
        sentence = []

        req_url = requests.get(self.epilogue_url)
        soup = BeautifulSoup(req_url.text, "lxml")
        all_announce = soup.find("body").find_all("div", class_="announce")

        for announce in all_announce:
            org_text = announce.text
            if ("生存" in org_text) or ("死亡" in org_text):
                text = org_text.replace("だった", "")
                sentence = text.rsplit("。")
                sentence.pop(-1)

            for part in sentence:
                if len(part) > 3:  # 役職名は短い
                    roll_name = part.rsplit(" ")
                    name_list.append(roll_name[0] + roll_name[1])
                else:
                    role_list.append(part)

        for name, role in zip(name_list, role_list):
            self.agent_role[name] = role

        self.players = len(name_list)
        return

    def get_sentence(self):
        if self.winner == "人狼":
            f = open("village_talklist/wolf_win/village_g{0}.csv".format(self.village_number), "a")

        elif self.winner == "村人":
            f = open("village_talklist/villager_win/village_g{0}.csv".format(self.village_number), "a")

        else:
            print("どっち勝ったかわかんね")
            f = open("village_talklist/village_g{0}.csv".format(self.village_number), "a")

        for day_number in range(0, self.last_day):
            url = "http://www.wolfg.x0.com/index.rb?vid={0}&meslog=00{1}_progress&mode=say".format(self.village_number,
                                                                                                   day_number)
            req_url = requests.get(url)
            soup = BeautifulSoup(req_url.text, "lxml")

            if soup.find("body").find("table", class_="message_box") is None:
                break

            else:
                messages = soup.find("body").find_all("div", class_="mes_say_body1")
                name_list = soup.find("body").find_all("a", class_="ch_name")

                for name, message in zip(name_list, messages):
                    name_text = name.text.replace(" ", "")
                    simple_mes = message.text.replace("\n", "")
                    f.write("{0}日目,".format(day_number + 1))
                    f.write(name_text + ",")
                    f.write(self.agent_role[name_text] + ",")
                    f.write(simple_mes + "\n")

        time.sleep(1)
        f.close()
        return

    def set_sud_death(self):
        epi_url = self.epilogue_url
        req_epi_url = requests.get(epi_url)
        soup = BeautifulSoup(req_epi_url.text, "lxml")
        all_mes_ch0 = soup.find("body").find("div", class_="message ch0")
        if all_mes_ch0 is not None:
            for announce in all_mes_ch0:
                text = announce.text
                if "突然死した。" in text:
                    self.sud_death = True
                    return

        for day_number in range(0, self.last_day):
            url = "http://www.wolfg.x0.com/index.rb?vid={0}&meslog=00{1}_progress&mode=say".format(self.village_number,
                                                                                                   day_number)
            req_url = requests.get(url)
            soup = BeautifulSoup(req_url.text, "lxml")
            all_mes_ch0 = soup.find("body").find("div", class_="message ch0")
            if all_mes_ch0 is not None:
                for announce in all_mes_ch0:
                    text = announce.text
                    if "突然死した。" in text:
                        self.sud_death = True
                        return

        return

    def set_winner(self):
        url = self.epilogue_url
        req_url = requests.get(url)
        soup = BeautifulSoup(req_url.text, "lxml")
        all_mes_ch0 = soup.find("body").find_all("div", class_="message ch0")
        if all_mes_ch0 is not None:
            for announce in all_mes_ch0:
                text = announce.text
                if "もう人狼に抵抗できるほど村人は残っていない……。" in text:
                    self.winner = "人狼"
                    return
                elif "全ての人狼を退治した……。" in text:
                    self.winner = "村人"
                    return

    def set_missing(self):
        url = self.prologue_url
        req_url = requests.get(url)
        soup = BeautifulSoup(req_url.text, "lxml")
        all_mes_ch0 = soup.find("body").find_all("div", class_="message ch0")
        if all_mes_ch0 is not None:
            for announce in all_mes_ch0:
                text = announce.text
                if ("失踪した。" in text) or ("を去った。" in text):
                    self.missing = True
        return

    def get_prologue(self):
        if self.winner == "人狼":
            f = open("village_talklist/wolf_win/village_g{0}.csv".format(self.village_number), "w")

        elif self.winner == "村人":
            f = open("village_talklist/villager_win/village_g{0}.csv".format(self.village_number), "w")

        else:
            print("どっち勝ったかわかんね")
            f = open("village_talklist/village_g{0}.csv".format(self.village_number), "w")

        url = self.prologue_url
        req_url = requests.get(url)
        soup = BeautifulSoup(req_url.text, "lxml")
        if soup.find("body").find("table", class_="message_box") is not None:
            messages = soup.find("body").find_all("div", class_="mes_say_body1")
            name_list = soup.find("body").find_all("a", class_="ch_name")

            for name, message in zip(name_list, messages):
                name_text = name.text.replace(" ", "")
                simple_mes = message.text.replace("\n", "")
                f.write("プロローグ,")
                f.write(name_text + ",")
                f.write(self.agent_role[name_text] + ",")
                f.write(simple_mes + "\n")

        time.sleep(1)
        f.close()
        return

    def get_whisper(self):

        if self.winner == "人狼":
            whisper_file = open("../village_whisper_list/wolf_win/village_g{0}.csv".format(self.village_number), "w")

        elif self.winner == "村人":
            whisper_file = open("../village_whisper_list/villager_win/village_g{0}.csv".format(self.village_number), "w")

        else:
            print("どっち勝ったかわかんね")
            whisper_file = open("../village_whisper_list/village_g{0}.csv".format(self.village_number), "w")

        for day_number in range(0, self.last_day):
            url = "http://www.wolfg.x0.com/index.rb?vid={0}&meslog=00{1}_progress&mode=whisper".format(
                self.village_number, day_number)

            req_url = requests.get(url)
            soup = BeautifulSoup(req_url.text, "lxml")
            if soup.find("body").find("table", class_="message_box") is not None:
                messages = soup.find("body").find_all("div", class_=re.compile("message"))
                for message in messages:

                    if message.find("div", class_="mes_whisper_body1") is not None:
                        name = message.find("a", class_="ch_name").text.replace(" ", "")
                        whisper = message.find("div", class_="mes_whisper_body1").text.replace("\n", "")
                        print(name, whisper)
                        whisper_file.write("{0},".format(day_number + 1))
                        whisper_file.write(name + "," + whisper + "\n")
        whisper_file.close()
        return


#  __ main__
for text_line in [61, 89]:  #捜索村範囲の指定
    bbs_game = WolfBBsg(text_line)
    if (bbs_game.players >= 14) and (bbs_game.sud_death is False) and (bbs_game.missing is False):  #自然死や失踪の有無
        print("village{0} OK".format(text_line))
        bbs_game.get_sentence()
    else:
        print(bbs_game.sud_death)
        print(bbs_game.missing)


#   epi_nothing = [100, 202, 433, 883, 910, 1349]
#   [61,89]村は失踪があるが、戻ってくため例外と扱う
