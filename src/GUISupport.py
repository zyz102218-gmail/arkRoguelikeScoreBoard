# -*- coding: UTF-8 -*-
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication

from mainwindow import Ui_MainWindow

from datetime import datetime

import os


class NormalScoreAction:
    def __init__(self, name='', small_score=0, description=''):
        self.name = name
        self.small_score = small_score
        self.description = description
        self.time = None

    def set_name(self, name: str):
        self.name = name

    def set_small_score(self, score: int):
        self.small_score = score

    def set_description(self, description: str):
        self.description = description

    def __add__(self, other):
        return int(self) + int(other)

    def __int__(self):
        return self.small_score

    def __radd__(self, other):
        if isinstance(other, int):
            return NormalScoreAction(name=self.name, small_score=self.small_score + other)
        else:
            raise TypeError("Can only add int to NormalScoreAction")

    def set_timestamp(self, timestamp):
        self.time = timestamp  # datetime_str


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        self.shijian = []
        # 定义分数变量
        self.total_score = 0  # 总分
        self.end_score = 0  # 结局分数
        self.experience_score = 0  # 过程加分
        self.invest_score = 0  # 取钱扣分
        self.no_core_operator_score = 0  # 核心干员控制分
        self.five_six_no_exit = 0  # 五六层紧急无漏怪分数
        self.Nickname = ''
        self.School = ''
        self.long_str = ""

        self.shijian_hash = None

        self.end_t = NormalScoreAction("结局")
        self.experience_t = NormalScoreAction()
        self.no_core_operator_t = NormalScoreAction()
        self.invest_t = NormalScoreAction()

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.setFixedSize(self.width(), self.height())
        self.IsFromPyQt = False

        self.update_score_timer = QTimer(self)
        self.ConnectingAndInit()

    def auto_update(self) -> None:
        """
        更新分数槽函数
        :return: None
        """
        self.five_six_no_exit = int(self.emeract_fivesix_count.text()) * 15  # 5、6层的紧急无漏@15
        self.cac_end_score()  # 计算结局分
        self.cac_core_operator_score()  # 核心干员控制分
        self.cac_experience_score()  # 过程加分
        self.cac_invest_score()

        if len(self.shijian) == 1:
            self.total_score = (self.end_score + self.shijian[
                0].small_score + self.experience_score + self.no_core_operator_score + self.five_six_no_exit
                                - self.invest_score)
        else:
            self.total_score = (self.end_score + sum(
                self.shijian) + self.experience_score + self.no_core_operator_score + self.five_six_no_exit
                                - self.invest_score)

        self.end_score_ssum.setText("{:0>4d}".format(self.end_score))
        self.backpak_score_ssum.setText("{:0>4d}".format(self.experience_score))
        self.score_sum.setText("{:0>4d}".format(self.total_score))
        self.touzi_get_score_sum.setText("{:0>4d}".format(self.invest_score))

        self.log_gen()

    def ConnectingAndInit(self):
        self.update_score_timer.setInterval(100)
        self.update_score_timer.timeout.connect(self.auto_update)
        self.update_score_timer.start()
        self.setWindowTitle("探索者的银凇止境-计分板")
        self.button_retract.setShortcut("ctrl+Z")
        self.button_retract.setStatusTip("撤销最后一次计分事件中的操作")
        self.button_retract.pressed.connect(self.retract_last_do)
        self.button_save.pressed.connect(self.save_one)
        self.button_remake.pressed.connect(self.clear_all)

        # 紧急作战
        self.emeract_hechu.pressed.connect(lambda: self.emergency_add_score(self.emeract_hechu.text()))
        self.emeract_binghai.pressed.connect(lambda: self.emergency_add_score(self.emeract_binghai.text()))
        self.emeract_jiaoshou.pressed.connect(lambda: self.emergency_add_score(self.emeract_jiaoshou.text()))
        self.emeract_gongsi.pressed.connect(lambda: self.emergency_add_score(self.emeract_gongsi.text()))
        self.emeract_renzao.pressed.connect(lambda: self.emergency_add_score(self.emeract_renzao.text()))
        self.emeract_benneng.pressed.connect(lambda: self.emergency_add_score(self.emeract_benneng.text()))
        self.emeract_wangzhe.pressed.connect(lambda: self.emergency_add_score(self.emeract_wangzhe.text()))
        self.emeract_hunluan.pressed.connect(lambda: self.emergency_add_score(self.emeract_hunluan.text()))
        self.emeract_qiudi.pressed.connect(lambda: self.emergency_add_score(self.emeract_hunluan.text()))
        self.emeract_shuangyu.pressed.connect(lambda: self.emergency_add_score(self.emeract_shuangyu.text()))
        self.emeract_shengling.pressed.connect(lambda: self.emergency_add_score(self.emeract_shengling.text()))
        self.emeract_shengren.pressed.connect(lambda: self.emergency_add_score(self.emeract_shengren.text()))
        self.emeract_yueli.pressed.connect(lambda: self.emergency_add_score(self.emeract_yueli.text()))
        self.emeract_tansuo.pressed.connect(lambda: self.emergency_add_score(self.emeract_tansuo.text()))

        # 路网作战
        self.roadmap_binghai.pressed.connect(lambda: self.map_add_score(self.roadmap_binghai.text()))
        self.roadmap_gongsi.pressed.connect(lambda: self.map_add_score(self.roadmap_gongsi.text()))
        self.roadmap_wangzhe.pressed.connect(lambda: self.map_add_score(self.roadmap_wangzhe.text()))

        # 特殊作战
        self.specialact_huxi.pressed.connect(lambda: self.special_add_score(self.specialact_huxi.text()))
        self.specialact_duoshu.pressed.connect(lambda: self.special_add_score(self.specialact_duoshu.text()))
        self.specialact_haohua.pressed.connect(lambda: self.special_add_score(self.specialact_haohua.text()))
        self.specialact_dadi.pressed.connect(lambda: self.special_add_score(self.specialact_dadi.text()))
        self.specialact_gengu.pressed.connect(lambda: self.special_add_score(self.specialact_gengu.text()))

        # 特殊无漏
        self.special_noexit_tiantu.pressed.connect(lambda: self.special_add_score(self.special_noexit_tiantu.text()))
        self.special_noexit_chengfa.pressed.connect(lambda: self.special_add_score(self.special_noexit_chengfa.text()))

        # 两个特殊
        self.specialact_huangsha_submit.pressed.connect(self.special_huangsha)
        self.specialact_zhengyi_sumbit.pressed.connect(self.special_zhengyi)
        self.specialact_yingxiong_submit.pressed.connect(self.special_hero)

    def retract_last_do(self) -> None:
        """
        撤销函数
        :return:
        """
        if self.shijian:
            self.shijian.pop()
        # self.auto_update()
        # pass

    def cac_end_score(self):
        """
        计算结局分数，并赋值给self.end_score
        :return:
        """
        end_score = 0
        end_des = ''
        # 先判断是不是1+3+4 2+3+4
        multi_end_flag = 1 if sum(
            [self.end_one.isChecked(), self.end_two.isChecked(), self.end_three_checked.isChecked(),
             self.end_four_checked.isChecked()]) != 1 else 0
        if self.end_one.isChecked() and self.end_three_checked.isChecked() and self.end_four_checked.isChecked():
            # 是1+3+4
            end_score = 580
            end_des = "一结局+三结局+四结局"
        elif self.end_two.isChecked() and self.end_three_checked.isChecked() and self.end_four_checked.isChecked():
            # 2+3+4
            end_score = 700
            end_des = "二结局+三结局+四结局"
        elif self.end_two.isChecked() and self.end_three_checked.isChecked():
            # 2+3
            end_score = 420
            end_des = "二结局+三结局"
        elif self.end_two.isChecked() and self.end_four_checked.isChecked():
            # 2+4
            end_score = 530
            end_des = "二结局+四结局"
            # 下面考虑非特定组合
        else:
            if self.end_one.isChecked():
                end_score += 80
                end_des += "一结局"
            if self.end_two.isChecked():
                end_score += 160
                end_des += '二结局'
            if self.end_three_checked.isChecked():
                end_score += 140
                end_des += "三结局"
            if self.end_four_checked.isChecked():
                end_score += 180
                end_des += "四结局"
        end_name = end_des
        end_des += "+{:d}，".format(end_score)

        if self.end_one.isChecked() and self.end_one_plus.isChecked():
            end_score += 120
            end_des += "深寒造像+120，"
        if self.end_two.isChecked() and self.end_two_plus.isChecked():
            end_score += 80
            end_des += '虚无之偶+80，'
        if self.end_three_checked.isChecked() and self.end_three_plus.isChecked():
            end_score += 300
            end_des += "哨兵+300，"
        if self.end_four_checked.isChecked() and self.end_four_plus.isChecked():
            end_score += 60
            end_des += "迈入永恒+600，"
        if self.end_no_cave.isChecked() and multi_end_flag:
            end_score += 300
            end_des += "多结局且没有进入树篱之途+300，"
        end_score += self.end_collectible_wuyin.isChecked() * 30 + \
                     self.end_collectible_weidu.isChecked() * 20 + \
                     self.end_collectible_tansuo.isChecked() * 20 + \
                     self.end_collectible_kongjian.isChecked() * 20 + \
                     self.end_collectible_shendu.isChecked() * 10
        end_des += "无垠赠礼 30 " if self.end_collectible_wuyin.isChecked() else ''
        end_des += "维度流质 20 " if self.end_collectible_weidu.isChecked() else ''
        end_des += "坍缩之种 20 " if self.end_collectible_tansuo.isChecked() else ""
        end_des += "空间碎片 20 " if self.end_collectible_kongjian.isChecked() else ""
        end_des += "深度灼痕 10 " if self.end_collectible_shendu.isChecked() else ""
        self.end_score = end_score
        self.end_t.set_small_score(end_score)
        self.end_t.set_name(end_name)
        self.end_t.set_description(end_des)

    def cac_experience_score(self):
        exp_score = 0
        exp_score += int(self.tempcall_six_count.text()) * 50 \
                     + int(self.tempcall_five_count.text()) * 20 \
                     + int(self.tempcall_four_count.text()) * 10

        exp_score += int(self.special_collectible_count.text()) * 20 + \
                     int(self.normal_collectible_count.text()) * 10

        exp_score += int(self.secretspoke_times.text()) * 5
        self.experience_t.set_small_score(exp_score)
        self.experience_t.set_description("临时招募 6星@50 {}, 5星@20 {}, 4星@10 {},隐藏@20 {},常规@10 {},"
                                          " 宣告密文@5 {}".format(
            int(self.tempcall_six_count.text()), int(self.tempcall_five_count.text()),
            int(self.tempcall_four_count.text()),
            int(self.special_collectible_count.text()), int(self.normal_collectible_count.text()),
            int(self.secretspoke_times.text())
        ))
        self.experience_score = exp_score

    def cac_core_operator_score(self):
        """
        计算未抓取核心干员控制分
        :return:
        """
        self.no_core_operator_score = int(self.no_core_operator_count.text()) * 30
        des = "共{}名核心干员未抓取，加{}分".format(
            self.no_core_operator_count.text(), int(self.no_core_operator_count.text()) * 30)
        if int(self.no_core_operator_count.text()) >= 3:
            self.no_core_operator_score += 30
            des += "，未抓取核心干员大于等于3，+30分"
        self.no_core_operator_t.set_small_score(self.no_core_operator_score)
        self.no_core_operator_t.set_description(des)

    def cac_invest_score(self):
        if (int(self.touzi_get_count.text())) > 90:
            self.invest_score = (int(self.touzi_get_count.text())-90) * 50
            self.invest_t.small_score = (int(self.touzi_get_count.text())-90) * 50
            self.invest_t.set_description("共提取{}个源石锭，扣除{}分".format(int(self.touzi_get_count.text()),
                                                                             self.invest_score))
        else:
            self.invest_score = 0
            self.invest_t.small_score=0
            self.invest_t.set_description("共提取{}个源石锭，未超过90个，不扣分".format(int(self.touzi_get_count.text())))

    def emergency_add_score(self, role_name: str):
        """
        增加紧急作战历程
        :param role_name: 紧急作战关卡名，为按钮上的文字
        :return:
        """
        if role_name in ['冰海疑影', '公司纠葛', '坍缩体的午后', '生人勿近']:
            score = 40
        elif role_name in ['狡兽九窟']:
            score = 30
        elif role_name in ['人造物狂欢节']:
            score = 110
        elif role_name in ['本能污染', '亡者行军']:
            score = 90
        elif role_name in ['乐理之灾']:
            score = 70
        elif role_name in ['混乱的表象', '求敌得敌', '何处无山海', '霜与沙']:
            score = 50
        elif role_name in ['生灵的终点']:
            score = 130
        action = NormalScoreAction("紧急作战{}".format(role_name), score,
                                   description="紧急作战{:}+{:d}".format(role_name, score))
        action.set_timestamp(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
        self.shijian.append(action)

    def map_add_score(self, role_name: str):
        """
        增加路网作战历程
        :param role_name: 紧急作战关卡名，为按钮上的文字
        :return:
        """
        if role_name in ['冰海疑影', '公司纠葛', '坍缩体的午后', '生人勿近']:
            score = 60
        elif role_name in ['狡兽九窟']:
            score = 30
        elif role_name in ['人造物狂欢节']:
            score = 110
        elif role_name in ['本能污染', '亡者行军']:
            score = 110
        elif role_name in ['乐理之灾']:
            score = 70
        elif role_name in ['混乱的表象', '求敌得敌', '何处无山海', '霜与沙']:
            score = 50
        elif role_name in ['生灵的终点']:
            score = 130
        action = NormalScoreAction("路网作战{}".format(role_name), score,
                                   description="路网作战{:}+{:d}".format(role_name, score))
        action.set_timestamp(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
        self.shijian.append(action)

    def special_add_score(self, role_name: str):
        """
        增加特殊作战历程，不包括正义使者等需要额外信息的关卡
        :param role_name: 紧急特殊关卡名，为按钮上的文字
        :return:
        """
        score_dict = {'呼吸': 50,
                      '夺树者': 60,
                      '大地醒转': 40,
                      '豪华车队（杀熊）': 50,
                      '亘古仇敌': 20,
                      '惩罚': 20,
                      '天途半道': 30}

        score = score_dict[role_name]
        action = NormalScoreAction("特殊作战{}".format(role_name), score, description="特殊作战{}+{:d}".format(
            role_name, score
        ))
        action.set_timestamp(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
        self.shijian.append(action)

    def special_huangsha(self):
        score = 20

        if self.specialact_huangsha_wind_check.isChecked():
            score += 10
            des = '黄沙幻境（无漏）+'
        else:
            des = '黄沙幻境（无漏）'
        action = NormalScoreAction("特殊作战{}".format(des), score, des + "+{}".format(score))
        action.set_timestamp(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
        self.shijian.append(action)

    def special_zhengyi(self):
        """
        特殊作战：正义使者处理
        :return:
        """
        score = 70
        score += int(self.specialact_zhengyi_killed_count.text()) * 30
        score += 20 if self.specialact_zhengyi_wulou.isChecked() else 0
        des = "特殊作战正义使者"
        des += "杀鸭狗熊x{}".format(int(self.specialact_zhengyi_killed_count.text()))
        des += "无漏" if self.specialact_zhengyi_wulou.isChecked() else ""
        action = NormalScoreAction("特殊作战正义使者", score, des)
        action.set_timestamp(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
        self.shijian.append(action)

    def special_hero(self):
        """
        特殊作战：英雄无名处理
        :return:
        """
        score = 30
        score += int(self.specialact_yingxiong_kill_count.text()) * 15
        score += 20 if self.specialact_yingxiong_noexit.isChecked() else 0
        des = '特殊作战英雄无名'
        des += "击杀敌人x{}".format(int(self.specialact_yingxiong_kill_count.text()))
        des += "无漏 " if self.specialact_yingxiong_noexit.isChecked() else ""
        action = NormalScoreAction("特殊作战英雄无名",score,des)
        action.set_timestamp(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
        self.shijian.append(action)

    def log_gen(self):
        if hash(str(self.shijian)) == self.shijian_hash:
            return
        long_str = "事件\t事件\t分数\n"
        for act in self.shijian:
            small_str = "{}\t {}\t {}\n".format(act.time.split()[1],act.name,act.small_score)
            long_str+=small_str
        self.long_str = long_str
        self.score_log.setText(self.long_str)

        self.shijian_hash = hash(str(self.shijian))

    def save_one(self):
        save_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        school = self.canSchool.currentText()
        NickName = self.canNickName.toPlainText()
        if len(NickName) == 0:
            QMessageBox.critical(self,"错误","昵称不能为空",QMessageBox.Ok)
            return
        # 详细记录
        with open("../rogue_log.txt", 'a') as f:
            f.write("------------------------------------\n")
            f.write("完赛时间：{}\n".format(save_time))
            f.write("选手学校：{}\n".format(school))
            f.write("昵称：{}\n".format(NickName))
            f.write("总分：{}\n".format(self.total_score))
            f.write("完赛结局：{}\n".format(self.end_t.name))
            f.write("------------------------------------\n")
            f.write("详细计分过程\n")
            f.write("结局计分：\n")
            f.write("{}\t {}分\t {}\n".format(self.end_t.name,self.end_t.small_score,self.end_t.description))
            f.write("背包及干员计分\n")
            f.write("{}分\t {}\n".format(self.experience_t.small_score,self.experience_t.description))
            f.write("核心干员抓取情况计分：")
            f.write("{}分\t {}\n".format(self.no_core_operator_t.small_score,self.no_core_operator_t.description))
            f.write("取钱情况计分：")
            f.write("-{}分\t {}\n".format(self.invest_t.small_score,self.invest_t.description))
            f.write("流程计分：")
            # 详细计分过程
            for act in self.shijian:
                f.write("{}\t {}\t {}\t {}\n".format(act.time,act.name,act.small_score,act.description))
            f.close()
        # 精简记录
        with open("../rogue_fine.txt", 'a') as f:
            f.write("------------------------------------\n")
            f.write("完赛时间：{}\n".format(save_time))
            f.write("选手学校：{}\n".format(school))
            f.write("昵称：{}\n".format(NickName))
            f.write("总分：{}\n".format(self.total_score))
            f.write("完赛结局：{}\n".format(self.end_t.name))
            f.write("------------------------------------\n")
            f.close()
        if not os.path.exists('../pic'):
            os.mkdir("../pic")
        screenshot = QApplication.primaryScreen().grabWindow(self.winId())
        screenshot.save('pic/{}.png'.format(save_time+NickName))

    def clear_all(self):
        self.shijian = []
        # 定义分数变量
        self.total_score = 0  # 总分
        self.end_score = 0  # 结局分数
        self.experience_score = 0  # 过程加分
        self.invest_score = 0  # 取钱扣分
        self.no_core_operator_score = 0  # 核心干员控制分
        self.five_six_no_exit = 0  # 五六层紧急无漏怪分数
        self.Nickname = ''
        self.School = ''
        self.long_str = ""

        self.shijian_hash = None

        self.end_t = NormalScoreAction("结局")
        self.experience_t = NormalScoreAction()
        self.no_core_operator_t = NormalScoreAction()
        self.invest_t = NormalScoreAction()

        self.no_core_operator_count.setValue(0)
        self.tempcall_five_count.setValue(0)
        self.tempcall_six_count.setValue(0)
        self.tempcall_six_count.setValue(0)
        self.normal_collectible_count.setValue(0)
        self.special_collectible_count.setValue(0)
        self.secretspoke_times.setValue(0)
        self.touzi_get_count.setValue(0)

        self.end_one.setAutoExclusive(False)
        self.end_two.setAutoExclusive(False)
        self.end_one.setChecked(False)
        self.end_two.setChecked(False)
        self.end_one.setAutoExclusive(True)
        self.end_two.setAutoExclusive(True)
        self.end_one_plus.setAutoExclusive(False)
        self.end_two_plus.setAutoExclusive(False)
        self.end_no_plus.setAutoExclusive(False)
        self.end_one_plus.setChecked(False)
        self.end_two_plus.setChecked(False)
        self.end_no_plus.setChecked(False)
        self.end_one_plus.setAutoExclusive(True)
        self.end_two_plus.setAutoExclusive(True)
        self.end_no_plus.setAutoExclusive(True)
        self.end_three_checked.setChecked(0)
        self.end_four_checked.setChecked(0)
        self.end_three_plus.setChecked(0)
        self.end_four_plus.setChecked(0)
        self.end_no_cave.setChecked(0)
        self.end_collectible_wuyin.setChecked(0)
        self.end_collectible_shendu.setChecked(0)
        self.end_collectible_tansuo.setChecked(0)
        self.end_collectible_kongjian.setChecked(0)
        self.end_collectible_weidu.setChecked(0)
        self.end_collectible_shendu.setChecked(0)
        self.specialact_huangsha_wind_check.setChecked(0)
        self.specialact_zhengyi_wulou.setChecked(0)
        self.specialact_yingxiong_noexit.setChecked(0)



