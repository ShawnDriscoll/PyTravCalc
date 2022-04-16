#
#   PyTravCalc 3.4.0 Beta for Mongoose Traveller 2nd Edition
#   Written for Python 3.9.11
#
##############################################################

"""
PyTravCalc 3.4.0 Beta for Mongoose Traveller 2nd Edition
--------------------------------------------------------

This program rolls 6-sided dice and calculates their effects.

The Traveller game in all forms is owned by Far Future Enterprises.
Copyright 1977 - 2022 Far Future Enterprises.
Traveller is a registered trademark of Far Future Enterprises.
"""
#import vlc

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#from PyQt5 import uic
import PyQt5.QtMultimedia as MM
import time
from mainwindow import Ui_MainWindow
from aboutdialog import Ui_aboutDialog
from alertdialog import Ui_alertDialog
from random import randint
from rpg_tools.PyDiceroll import roll
import sys
import os
import numpy as np
from matplotlib import font_manager
import logging

__author__ = 'Shawn Driscoll <shawndriscoll@hotmail.com>\nshawndriscoll.blogspot.com'
__app__ = 'PyTravCalc 3.4.0 Beta'
__version__ = '3.4.0b'
__py_version__ = '3.9.11'
__expired_tag__ = False

#form_class = uic.loadUiType("mainwindow.ui")[0]

class aboutDialog(QDialog, Ui_aboutDialog):
    def __init__(self):
        '''
        Open the About dialog window
        '''
        super().__init__()
        log.info('PyQt5 aboutDialog initializing...')
        self.setWindowFlags(Qt.Drawer | Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.aboutOKButton.clicked.connect(self.acceptOKButtonClicked)
        log.info('PyQt5 aboutDialog initialized.')
        
    def acceptOKButtonClicked(self):
        '''
        Close the About dialog window
        '''
        log.info('PyQt5 aboutDialog closing...')
        self.close()

class alertDialog(QDialog, Ui_alertDialog):
    def __init__(self):
        '''
        Open the Alert dialog window
        '''
        super().__init__()
        log.info('PyQt5 alertDialog initializing...')
        self.setWindowFlags(Qt.Drawer | Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.aboutOKButton.clicked.connect(self.acceptOKButtonClicked)
        log.info('PyQt5 alertDialog initialized.')
        
    def acceptOKButtonClicked(self):
        '''
        Close the Alert dialog window
        '''
        log.info('PyQt5 alertDialog closing...')
        self.close()

#class MainWindow(QMainWindow):
#class MainWindow(QMainWindow, form_class):
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        '''
        Display the main app window.
        Connect all the buttons to their functions.
        Initialize their value ranges.
        '''
        super().__init__()
        
        #uic.loadUi("mainwindow.ui", self)
        
        log.info('PyQt5 MainWindow initializing...')
        self.setupUi(self)
        self.roll2D_Button.clicked.connect(self.roll2D_buttonClicked)
        self.actionRoll_2D.triggered.connect(self.roll2D_buttonClicked)
        self.rollBane_Button.clicked.connect(self.rollBane_buttonClicked)
        self.actionRoll_Bane.triggered.connect(self.rollBane_buttonClicked)
        self.rollBoon_Button.clicked.connect(self.rollBoon_buttonClicked)
        self.actionRoll_Boon.triggered.connect(self.rollBoon_buttonClicked)
        self.rollD66_Button.clicked.connect(self.rollD66_buttonClicked)
        self.actionRoll_D66.triggered.connect(self.rollD66_buttonClicked)
        self.clearAll_Button.clicked.connect(self.clearall_buttonClicked)
        self.action_ClearAll.triggered.connect(self.clearall_buttonClicked)
        self.clearDamage_Button.clicked.connect(self.cleardamage_buttonClicked)
        self.action_ClearDamage.triggered.connect(self.cleardamage_buttonClicked)
        self.inputarmor.valueChanged.connect(self.inputarmor_valueChanged)
        self.inputdice.valueChanged.connect(self.inputdice_valueChanged)
        self.damage_Button.clicked.connect(self.damage_buttonClicked)
        self.destructive_Button.clicked.connect(self.destructive_buttonClicked)
        self.inputDamageDM.valueChanged.connect(self.inputdamageDM_valueChanged)
        self.inputap.valueChanged.connect(self.inputap_valueChanged)
        self.actionMaleVoice.triggered.connect(self.MaleVoice_menu)
        self.actionFemaleVoice.triggered.connect(self.FemaleVoice_menu)
        self.actionRobotVoice.triggered.connect(self.RobotVoice_menu)
        self.actionPlaySample.triggered.connect(self.PlaySample_menu)
        self.actionMute.triggered.connect(self.Mute_menu)
        self.actionStandardDice.triggered.connect(self.StandardDice_menu)
        self.actionTravellerDice.triggered.connect(self.TravellerDice_menu)
        self.actionAKODice.triggered.connect(self.AKODice_menu)
        self.actionMetalDice.triggered.connect(self.MetalDice_menu)
        self.actionCUBBLEDice.triggered.connect(self.CUBBLEDice_menu)
        self.actionRomanDice.triggered.connect(self.RomanDice_menu)
        self.actionGridGrooveDice.triggered.connect(self.GridGrooveDice_menu)
        self.actionYellowDice.triggered.connect(self.YellowDice_menu)
        self.actionSHONNERDice.triggered.connect(self.SHONNERDice_menu)
        self.actionQuestionDice.triggered.connect(self.QuestionDice_menu)
        self.actionMixedDice.triggered.connect(self.MixedDice_menu)
        self.actionVisit_Blog.triggered.connect(self.Visit_Blog)
        self.actionFeedback.triggered.connect(self.Feedback)
        self.actionOverview.triggered.connect(self.Overview_menu)
        self.actionAbout_PyTravCalc.triggered.connect(self.actionAbout_triggered)
        self.actionQuit.triggered.connect(self.quitButton_clicked)
        self.inputtasks.valueChanged.connect(self.inputtasks_value_Changed)
        self.inputchar.valueChanged.connect(self.inputchar_valueChanged)
        self.charbox = True
        self.inputchar.setDisabled(self.charbox)
        self.inputlevel.valueChanged.connect(self.inputlevel_valueChanged)
        self.levelbox = True
        self.inputlevel.setDisabled(self.levelbox)
        self.inputDM.valueChanged.connect(self.inputDM_valueChanged)
        self.DMbox = True
        self.inputDM.setDisabled(self.DMbox)
        self.char_dm = [-3, -2, -2, -1, -1, -1, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10]
        self.charmod_value = 0
        self.chained_task = False
        self.selChained.toggled.connect(self.selChained_valueChanged)
        self.chainedbox = True
        self.selChained.setDisabled(self.chainedbox)
        self.previous_effect_DM = 0
        self.next_effect_DM = 0
        self.selDiff.addItem('         Choose One')
        self.selDiff.addItem('Simple (2+)')
        self.selDiff.addItem('Easy (4+)')
        self.selDiff.addItem('Routine (6+)')
        self.selDiff.addItem('Average (8+)')
        self.selDiff.addItem('Difficult (10+)')
        self.selDiff.addItem('Very Difficult (12+)')
        self.selDiff.addItem('Formidable (14+)')
        self.selDiff.addItem('Impossible (16+)')
        self.selDiff.addItem('Random')
        self.selDiff.addItem('Unknown')
        self.selDiff.setCurrentIndex(0)
        self.selDiff.currentIndexChanged.connect(self.selDiff_valueChanged)
        self.NumTasks = True
        self.inputtasks.setDisabled(self.NumTasks)
        self.NewNumTasks = 1
        self.PreviousNumTasks = 1
        self.selTimeframe.addItem('Choose One')
        self.selTimeframe.addItem('1D Seconds')
        self.selTimeframe.addItem('1D Cbt Rnds')
        self.selTimeframe.addItem('1D x 10 Sec')
        self.selTimeframe.addItem('1D Minutes')
        self.selTimeframe.addItem('1D x 10 Min')
        self.selTimeframe.addItem('1D Hours')
        self.selTimeframe.addItem('1D x 4 Hrs')
        self.selTimeframe.addItem('1D x 10 Hrs')
        self.selTimeframe.addItem('1D Days')
        self.selTimeframe.setCurrentIndex(0)
        self.selTimeframe.currentIndexChanged.connect(self.selTimeframe_valueChanged)
        self.Timeframe = True
        self.selTimeframe.setDisabled(self.Timeframe)
        self.selNewTimeframe.addItem('Choose One')
        self.selNewTimeframe.addItem('1D Seconds')
        self.selNewTimeframe.addItem('1D Cbt Rnds')
        self.selNewTimeframe.addItem('1D x 10 Sec')
        self.selNewTimeframe.addItem('1D Minutes')
        self.selNewTimeframe.addItem('1D x 10 Min')
        self.selNewTimeframe.addItem('1D Hours')
        self.selNewTimeframe.addItem('1D x 4 Hrs')
        self.selNewTimeframe.addItem('1D x 10 Hrs')
        self.selNewTimeframe.addItem('1D Days')
        self.selNewTimeframe.setCurrentIndex(0)
        self.selNewTimeframe.currentIndexChanged.connect(self.selNewTimeframe_valueChanged)
        self.NewTimeframe = True
        self.selNewTimeframe.setDisabled(self.NewTimeframe)
        self.selCover.addItem('        Choose One')
        self.selCover.addItem('Vegetation (+2)')
        self.selCover.addItem('Tree Trunk (+6)')
        self.selCover.addItem('Stone Wall (+8)')
        self.selCover.addItem('Civilian Vehicle (+10)')
        self.selCover.addItem('Armored Vehicle (+15)')
        self.selCover.addItem('Fortifications (+20)')
        self.selCover.setCurrentIndex(0)
        self.selCover.currentIndexChanged.connect(self.selCover_valueChanged)
        self.rollInput.returnPressed.connect(self.manual_roll)
        self.clearRollHistory.clicked.connect(self.clearRollHistoryClicked)
        self.action_ClearRollHistory.triggered.connect(self.clearRollHistoryClicked)

        #self.le = QLineEdit()
        #self.le.returnPressed.connect(self.append_text)
        
        # Will the app speak by default when used?
        self.muted = False

        # set the default roll type
        self.roll_type = '2D'

        # Is the difficulty known?
        self.unknown = False

        # Set difficulty to not chosen yet
        self.target_num = 0

        # Choose which cool-looking die to use and set it to True
        self.standard_dice = False
        self.traveller_dice = False
        self.ako_dice = True
        self.metal_dice = False
        self.cubble_dice = False
        self.roman_dice = False
        self.gridgroove_dice = False
        self.yellow_dice = False
        self.shonner_dice = False
        
        # Set the dice type to match the die chosen
        self.dice_type ='ak'
        self.dice_list = ['st', 'tr', 'ak', 'me', 'cu', 'ro', 'gg', 'ye', 'sh']
        self.question_dice = False
        self.mixed_dice = False

        # Set the default voice to True
        self.male_voice = False
        self.female_voice = True
        self.robot_voice = False
        self.actionMaleVoice.setDisabled(self.male_voice)
        self.actionFemaleVoice.setDisabled(self.female_voice)
        self.actionRobotVoice.setDisabled(self.robot_voice)

        # Voice can be 'female', 'male', or 'robot'
        self.voice_type = 'female'

        # Clear the graph
        self.blank_graph = True

        self.timeframe_DM = 0
        self.previous_timeframe_DM = 0
        self.DM_modifier = 0
        self.total_rolled = 0
        self.roll_effect = 0
        self.damage_amount = 0
        self.total_damage = 0
        self.actual_armor = 0
        self.cover_modifier = 0

        # Set active/deactive menu items
        self.actionPlaySample.setDisabled(self.muted)
        self.actionMute.setDisabled(self.muted)
        self.actionUnMute.setDisabled(not self.muted)
        self.actionStandardDice.setDisabled(self.standard_dice)
        self.actionTravellerDice.setDisabled(self.traveller_dice)
        self.actionAKODice.setDisabled(self.ako_dice)
        self.actionMetalDice.setDisabled(self.metal_dice)
        self.actionCUBBLEDice.setDisabled(self.cubble_dice)
        self.actionRomanDice.setDisabled(self.roman_dice)
        self.actionGridGrooveDice.setDisabled(self.gridgroove_dice)
        self.actionYellowDice.setDisabled(self.yellow_dice)
        self.actionSHONNERDice.setDisabled(self.shonner_dice)
        self.actionQuestionDice.setDisabled(self.question_dice)
        self.actionMixedDice.setDisabled(self.mixed_dice)

        # Set the About menu item
        self.popAboutDialog=aboutDialog()

        # Set the Alert menu item
        self.popAlertDialog=alertDialog()

        log.info('PyQt5 MainWindow initialized.')

        if __expired_tag__ == True:
            '''
            Beta for this app has expired!
            '''
            log.warning(__app__ + ' expiration detected...')
            self.alert_window()
            '''
            display alert message and disable all the things
            '''
            self.selDiff.setDisabled(True)
            self.roll2D_Button.setDisabled(True)
            self.rollBane_Button.setDisabled(True)
            self.rollBoon_Button.setDisabled(True)
            self.rollD66_Button.setDisabled(True)
            self.clearDamage_Button.setDisabled(True)
            self.inputarmor.setDisabled(True)
            self.selCover.setDisabled(True)
            self.inputap.setDisabled(True)
            self.inputdice.setDisabled(True)
            self.damage_Button.setDisabled(True)
            self.destructive_Button.setDisabled(True)
            self.inputDamageDM.setDisabled(True)
            self.clearAll_Button.setDisabled(True)
            self.actionRoll_2D.setDisabled(True)
            self.actionRoll_Boon.setDisabled(True)
            self.actionRoll_Bane.setDisabled(True)
            self.actionRoll_D66.setDisabled(True)
            self.action_ClearAll.setDisabled(True)
            self.action_ClearDamage.setDisabled(True)
            self.actionStandardDice.setDisabled(True)
            self.actionTravellerDice.setDisabled(True)
            self.actionMetalDice.setDisabled(True)
            self.actionCUBBLEDice.setDisabled(True)
            self.actionRomanDice.setDisabled(True)
            self.actionGridGrooveDice.setDisabled(True)
            self.actionYellowDice.setDisabled(True)
            self.actionSHONNERDice.setDisabled(True)
            self.actionMixedDice.setDisabled(True)
            self.actionQuestionDice.setDisabled(True)
            self.actionMute.setDisabled(True)
            self.actionMaleVoice.setDisabled(True)
            self.actionFemaleVoice.setDisabled(True)
            self.actionRobotVoice.setDisabled(True)
            self.actionPlaySample.setDisabled(True)
            self.actionVisit_Blog.setDisabled(True)
            self.actionFeedback.setDisabled(True)
            self.actionOverview.setDisabled(True)
            self.actionAbout_PyTravCalc.setDisabled(True)
            self.rollInput.setDisabled(True)
            self.clearRollHistory.setDisabled(True)
            self.rollBrowser.setDisabled(True)
            self.action_ClearRollHistory.setDisabled(True)

    def selDiff_valueChanged(self):
        '''
        Choose the difficulty for the roll
        '''
        difficulty_level = [0, 2, 4, 6, 8, 10, 12, 14, 16]
        if self.selDiff.currentIndex() == 0:
            self.target_num = 0
        elif self.selDiff.currentIndex() == 9:
            
            # A random difficulty has been asked for
            log.debug('Difficulty is random')
            self.unknown = False
            self.selDiff.setCurrentIndex(randint(1,8))
            self.target_num = difficulty_level[self.selDiff.currentIndex()]
        elif self.selDiff.currentIndex() == 10:
            
            # The difficulty is unknown to the player.
            # The Referee can see the difficulty shown on their console.
            self.unknown = True
            self.target_num = difficulty_level[randint(1,8)]
            log.debug('Difficulty is unknown: (%d+)' % self.target_num)
            print('The unknown Target Number is %d+' % self.target_num)
        elif self.selDiff.currentIndex() >= 1 and self.selDiff.currentIndex() <= 8:
            
            # A regular difficulty has been given to the player to input
            self.unknown = False
            self.target_num = difficulty_level[self.selDiff.currentIndex()]
            log.debug('Buttons initialized for difficulty: (%d+)' % self.target_num)
        
        # Reset the buttons and graph whenever a difficulty has been chosen
        self.roll_type = '2D'
        self.blank_graph = True
        self.update_graph()
        if self.target_num == 0:
            self.NumTasks = True
            self.Timeframe = True
            self.charbox = True
            self.levelbox = True
            self.DMbox = True
            self.chainedbox = True
            self.rollbox = True
        else:
            if self.unknown:
                self.NumTasks = True
            else:
                self.NumTasks = False
            self.Timeframe = False
            self.charbox = False
            self.levelbox = False
            self.DMbox = False
            self.chainedbox = False
            self.rollbox = False
        self.inputtasks.setDisabled(self.NumTasks)
        self.selNewTimeframe.setCurrentIndex(self.selTimeframe.currentIndex())
        self.selTimeframe.setDisabled(self.Timeframe)
        self.selNewTimeframe.setDisabled(self.NewTimeframe)
        self.inputchar.setDisabled(self.charbox)
        self.inputlevel.setDisabled(self.levelbox)
        self.inputDM.setDisabled(self.DMbox)
        self.selChained.setDisabled(self.chainedbox)
        self.selTimeframe.setCurrentIndex(0)
        self.inputchar.setValue(7)
        self.inputlevel.setValue(0)
        self.charmod_value = 0
        self.charmod.setText(str(self.charmod_value))
        self.inputDM.setValue(0)
        self.selChained.setChecked(False)
        self.rollresult.setText('')
        
        # Remove the dice from the display.
        self.die1Label.setPixmap(QPixmap(':/images/die1_0.png'))
        self.die2Label.setPixmap(QPixmap(':/images/die2_0.png'))
        self.die3Label.setPixmap(QPixmap(':/images/die3_0.png'))

        # Reset the screen
        self.tasktime_result.setText('')
        self.effect_result.setText('')
        self.effect_damage.setText('')
        self.inputdice.setValue(1)
        self.inputDamageDM.setValue(0)
        self.totalDamage.setText('')
        self.roll_effect = 0

    def inputtasks_value_Changed(self):
        '''
        A number of tasks was entered.
        Adjust the difficulty for that.
        '''
        self.NewNumTasks = self.inputtasks.value()
        self.target_num += (self.NewNumTasks - self.PreviousNumTasks) * 2
        if self.target_num > 16:
            self.target_num = 16
            self.NewNumTasks += -1
            self.inputtasks.setValue(self.NewNumTasks)
        if self.target_num < 2:
            self.target_num = 2
            self.NewNumTasks = 1
            self.inputtasks.setValue(self.NewNumTasks)
        self.PreviousNumTasks = self.NewNumTasks
        self.selDiff.setCurrentIndex(self.target_num / 2)
        log.debug('Number of tasks being performed: %d' % self.NewNumTasks)

    def selTimeframe_valueChanged(self):
        '''
        A timeframe was selected
        '''
        self.selNewTimeframe.setCurrentIndex(self.selTimeframe.currentIndex())
        if self.selTimeframe.currentIndex() == 0:
            self.NewTimeframe = True
        else:
            self.NewTimeframe = False
        self.selNewTimeframe.setDisabled(self.NewTimeframe)
        self.DM_modifier += -self.previous_timeframe_DM
        self.inputDM.setValue(self.DM_modifier)
        self.timeframe_DM = 0
        self.previous_timeframe_DM = self.timeframe_DM

        # reset the screen
        self.die1Label.setPixmap(QPixmap(':/images/die1_0.png'))
        self.die2Label.setPixmap(QPixmap(':/images/die2_0.png'))
        self.die3Label.setPixmap(QPixmap(':/images/die3_0.png'))
        self.rollresult.setText('')
        self.tasktime_result.setText('')
        self.effect_result.setText('')
        self.inputdice.setValue(1)
        self.effect_damage.setText('')
        self.roll_effect = 0
        self.blank_graph = True
        self.update_graph()
        
    def selNewTimeframe_valueChanged(self):
        '''
        A new timeframe was selected.
        Compare it with the initial timeframe to calculate a DM.
        '''
        self.timeframe_DM = (self.selNewTimeframe.currentIndex() - self.selTimeframe.currentIndex()) * 2
        self.DM_modifier += - self.previous_timeframe_DM
        self.DM_modifier += self.timeframe_DM
        self.inputDM.setValue(self.DM_modifier)
        self.previous_timeframe_DM = self.timeframe_DM

    def inputchar_valueChanged(self):
        '''
        A characteristic value was entered.
        Update the characteristic modifier if needed.
        '''
        self.charmod_value = self.char_dm[self.inputchar.value()]
        self.charmod.setText(str(self.charmod_value))
        if self.chained_task:
            self.totalDM.setText(str(self.inputlevel.value() + self.charmod_value + self.inputDM.value() + self.previous_effect_DM))
        else:
            self.totalDM.setText(str(self.inputlevel.value() + self.charmod_value + self.inputDM.value()))
        
        # reset the screen
        self.rollresult.setText('')
        self.die1Label.setPixmap(QPixmap(':/images/die1_0.png'))
        self.die2Label.setPixmap(QPixmap(':/images/die2_0.png'))
        self.die3Label.setPixmap(QPixmap(':/images/die3_0.png'))
        self.tasktime_result.setText('')
        self.effect_result.setText('')
        self.effect_damage.setText('')
        self.inputdice.setValue(1)
        self.inputDamageDM.setValue(0)
        self.totalDamage.setText('')
        self.roll_effect = 0
        self.blank_graph = True
        self.selChained.setChecked(False)
        self.update_graph()
    
    def inputlevel_valueChanged(self):
        '''
        A skill level was entered.
        Add it to the DM total.
        '''
        if self.chained_task:
            self.totalDM.setText(str(self.inputlevel.value() + self.charmod_value + self.inputDM.value() + self.previous_effect_DM))
        else:
            self.totalDM.setText(str(self.inputlevel.value() + self.charmod_value + self.inputDM.value()))
        
        # reset the screen
        self.rollresult.setText('')
        self.die1Label.setPixmap(QPixmap(':/images/die1_0.png'))
        self.die2Label.setPixmap(QPixmap(':/images/die2_0.png'))
        self.die3Label.setPixmap(QPixmap(':/images/die3_0.png'))
        self.tasktime_result.setText('')
        self.effect_result.setText('')
        self.effect_damage.setText('')
        self.inputdice.setValue(1)
        self.inputDamageDM.setValue(0)
        self.totalDamage.setText('')
        self.roll_effect = 0
        self.blank_graph = True
        self.selChained.setChecked(False)
        log.debug('Skill level set at: %d' % self.inputlevel.value())
        self.update_graph()
        
    def inputDM_valueChanged(self):
        '''
        A DM was entered.
        Add it to the DM total.
        '''
        if self.chained_task:
            self.totalDM.setText(str(self.inputlevel.value() + self.charmod_value + self.inputDM.value() + self.previous_effect_DM))
        else:
            self.totalDM.setText(str(self.inputlevel.value() + self.charmod_value + self.inputDM.value()))
        
        # reset the screen
        self.DM_modifier = self.inputDM.value()
        self.rollresult.setText('')
        self.die1Label.setPixmap(QPixmap(':/images/die1_0.png'))
        self.die2Label.setPixmap(QPixmap(':/images/die2_0.png'))
        self.die3Label.setPixmap(QPixmap(':/images/die3_0.png'))
        self.tasktime_result.setText('')
        self.effect_result.setText('')
        self.effect_damage.setText('')
        self.inputdice.setValue(1)
        self.inputDamageDM.setValue(0)
        self.totalDamage.setText('')
        self.roll_effect = 0
        self.blank_graph = True
        self.selChained.setChecked(False)
        self.update_graph()
        
    def selChained_valueChanged(self):
        '''
        Tasks are being chained.
        Use previous effect as a DM.
        '''
        self.chained_task = self.selChained.isChecked()
        if self.chained_task:
            self.previous_effect_DM = self.next_effect_DM
            self.chainedDM.setText(str(self.previous_effect_DM))
            self.totalDM.setText(str(self.inputlevel.value() + self.charmod_value + self.inputDM.value() + self.previous_effect_DM))
        else:
            self.previous_effect_DM = self.next_effect_DM
            self.chainedDM.setText('')
            self.totalDM.setText(str(self.inputlevel.value() + self.charmod_value + self.inputDM.value()))

        # reset the screen
        self.rollresult.setText('')
        self.die1Label.setPixmap(QPixmap(':/images/die1_0.png'))
        self.die2Label.setPixmap(QPixmap(':/images/die2_0.png'))
        self.die3Label.setPixmap(QPixmap(':/images/die3_0.png'))
        self.tasktime_result.setText('')
        self.effect_result.setText('')
        self.effect_damage.setText('')
        self.inputdice.setValue(1)
        self.inputDamageDM.setValue(0)
        self.totalDamage.setText('')
        self.roll_effect = 0
        self.blank_graph = True
        self.update_graph()
        
    def roll2D_buttonClicked(self):
        '''
        Do a 2D roll
        '''
        self.roll_type = '2D'
        self.natural_roll_1 = roll('1D6')
        self.natural_roll_2 = roll('1D6')
        log.debug('2D roll: %d %d' % (self.natural_roll_1, self.natural_roll_2))
        self.natural_roll = self.natural_roll_1 + self.natural_roll_2
        if self.chained_task:
            self.total_rolled = self.natural_roll + self.inputlevel.value() + self.charmod_value + self.inputDM.value() + self.previous_effect_DM
        else:
            self.total_rolled = self.natural_roll + self.inputlevel.value() + self.charmod_value + self.inputDM.value()
        self.rollresult.setText(str(self.total_rolled))
        if self.mixed_dice:
            self.die1Label.setPixmap(QPixmap(':/images/die1_' + str(self.natural_roll_1) + self.dice_list[randint(1, len(self.dice_list)) - 1] + '.png'))
            self.die2Label.setPixmap(QPixmap(':/images/die2_' + str(self.natural_roll_2) + self.dice_list[randint(1, len(self.dice_list)) - 1] + '.png'))
        else:
            self.die1Label.setPixmap(QPixmap(':/images/die1_' + str(self.natural_roll_1) + self.dice_type + '.png'))
            self.die2Label.setPixmap(QPixmap(':/images/die2_' + str(self.natural_roll_2) + self.dice_type + '.png'))
        self.die3Label.setPixmap(QPixmap(':/images/die3_0.png'))
        if self.target_num != 0:
            self.blank_graph = False
            self.roll_effect = self.total_rolled - self.target_num
            if self.roll_effect <= -6:
                self.effect_result.setText('%d: Exceptional Failure' % self.roll_effect)
                self.next_effect_DM = -3
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_exceptional_failure.mp3')))
                    m_media.play()
            if self.roll_effect >= -5 and self.roll_effect <= -2:
                self.effect_result.setText('%d: Average Failure' % self.roll_effect)
                self.next_effect_DM = -2
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_average_failure.mp3')))
                    m_media.play()
            if self.roll_effect == -1:
                self.effect_result.setText('%d: Marginal Failure' % self.roll_effect)
                self.next_effect_DM = -1
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_marginal_failure.mp3')))
                    m_media.play()
            if self.roll_effect == 0:
                self.effect_result.setText('%d: Marginal Success' % self.roll_effect)
                self.next_effect_DM = 0
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_marginal_success.mp3')))
                    m_media.play()
            if self.roll_effect >= 1 and self.roll_effect <= 5:
                self.effect_result.setText('%d: Average Success' % self.roll_effect)
                self.next_effect_DM = 1
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_average_success.mp3')))
                    m_media.play()
            if self.roll_effect >= 6:
                self.effect_result.setText('%d: Exceptional Success' % self.roll_effect)
                self.next_effect_DM = 2
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_exceptional_success.mp3')))
                    m_media.play()
            
            # reset the damage area at the bottom
            self.effect_damage.setText(str(self.roll_effect))
            self.inputdice.setValue(1)
            self.inputDamageDM.setValue(0)
            self.totalDamage.setText('')
            self.update_graph()

            # calculate the amount of time spent on the task
            task_time = self.selNewTimeframe.currentIndex()
            if task_time == 0:
                self.tasktime_result.setText('Not Available')
            if task_time == 1:
                self.tasktime_result.setText(str(roll('1D6')) + ' Seconds')
            if task_time == 2:
                self.tasktime_result.setText(str(roll('1D6')) + ' Combat Rnds')
            if task_time == 3:
                self.tasktime_result.setText(str(roll('1D6') * 10) + ' Seconds')
            if task_time == 4:
                self.tasktime_result.setText(str(roll('1D6')) + ' Minutes')
            if task_time == 5:
                self.tasktime_result.setText(str(roll('1D6') * 10) + ' Minutes')
            if task_time == 6:
                self.tasktime_result.setText(str(roll('1D6')) + ' Hours')
            if task_time == 7:
                self.tasktime_result.setText(str(roll('1D6') * 4) + ' Hours')
            if task_time == 8:
                self.tasktime_result.setText(str(roll('1D6') * 10) + ' Hours')
            if task_time == 9:
                self.tasktime_result.setText(str(roll('1D6')) + ' Days')
        else:
            if not self.muted:

                # Say the 2D roll. Only the female voice can say it for now.
                m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_' + str(self.natural_roll_1 + self.natural_roll_2) + '.mp3')))
                m_media.play()

    def rollBane_buttonClicked(self):
        '''
        Do a Bane roll
        '''
        die = [0, 0, 0]
        die[0] = roll('1D6')
        die[1] = roll('1D6')
        die[2] = roll('1D6')
        #print die[0], die[1], die[2]
        log.debug('Start Bane roll: %d %d %d' % (die[0], die[1], die[2]))
        die_swap = True
        while die_swap == True:
            die_swap = False
            for j in range(2):
                if die[j] > die[j+1]:
                    temp_die = die[j]
                    die[j] = die[j+1]
                    die[j+1] = temp_die
                    die_swap = True
        #print die[0], die[1], die[2]
        self.roll_type = 'Bane'
        self.natural_roll_1 = die[0]
        self.natural_roll_2 = die[1]
        self.natural_roll_3 = die[2]
        log.debug('Sorted Bane roll: %d %d %d' % (die[0], die[1], die[2]))
        self.natural_roll = self.natural_roll_1 + self.natural_roll_2
        if self.chained_task:
            self.total_rolled = self.natural_roll + self.inputlevel.value() + self.charmod_value + self.inputDM.value() + self.previous_effect_DM
        else:
            self.total_rolled = self.natural_roll + self.inputlevel.value() + self.charmod_value + self.inputDM.value()
        self.rollresult.setText(str(self.total_rolled))
        if self.mixed_dice:
            self.die1Label.setPixmap(QPixmap(':/images/die1_' + str(self.natural_roll_1) + self.dice_list[randint(1, len(self.dice_list)) - 1] + '.png'))
            self.die2Label.setPixmap(QPixmap(':/images/die2_' + str(self.natural_roll_2) + self.dice_list[randint(1, len(self.dice_list)) - 1] + '.png'))
            self.die3Label.setPixmap(QPixmap(':/images/die3_' + str(self.natural_roll_3) + self.dice_list[randint(1, len(self.dice_list)) - 1] + '.png'))
        else:
            self.die1Label.setPixmap(QPixmap(':/images/die1_' + str(self.natural_roll_1) + self.dice_type + '.png'))
            self.die2Label.setPixmap(QPixmap(':/images/die2_' + str(self.natural_roll_2) + self.dice_type + '.png'))
            self.die3Label.setPixmap(QPixmap(':/images/die3_' + str(self.natural_roll_3) + self.dice_type + '.png'))
        if self.target_num != 0:
            self.blank_graph = False
            self.roll_effect = self.total_rolled - self.target_num
            if self.roll_effect <= -6:
                self.effect_result.setText('%d: Exceptional Failure' % self.roll_effect)
                self.next_effect_DM = -3
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_exceptional_failure.mp3')))
                    m_media.play()
            if self.roll_effect >= -5 and self.roll_effect <= -2:
                self.effect_result.setText('%d: Average Failure' % self.roll_effect)
                self.next_effect_DM = -2
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_average_failure.mp3')))
                    m_media.play()
            if self.roll_effect == -1:
                self.effect_result.setText('%d: Marginal Failure' % self.roll_effect)
                self.next_effect_DM = -1
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_marginal_failure.mp3')))
                    m_media.play()
            if self.roll_effect == 0:
                self.effect_result.setText('%d: Marginal Success' % self.roll_effect)
                self.next_effect_DM = 0
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_marginal_success.mp3')))
                    m_media.play()
            if self.roll_effect >= 1 and self.roll_effect <= 5:
                self.effect_result.setText('%d: Average Success' % self.roll_effect)
                self.next_effect_DM = 1
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_average_success.mp3')))
                    m_media.play()
            if self.roll_effect >= 6:
                self.effect_result.setText('%d: Exceptional Success' % self.roll_effect)
                self.next_effect_DM = 2
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_exceptional_success.mp3')))
                    m_media.play()

            # reset the damage area at the bottom
            self.effect_damage.setText(str(self.roll_effect))
            self.inputdice.setValue(1)
            self.inputDamageDM.setValue(0)
            self.totalDamage.setText('')
            self.update_graph()

            # calculate the amount of time spent on the task
            task_time = self.selNewTimeframe.currentIndex()
            if task_time == 0:
                self.tasktime_result.setText('Not Available')
            if task_time == 1:
                self.tasktime_result.setText(str(roll('1D6')) + ' Seconds')
            if task_time == 2:
                self.tasktime_result.setText(str(roll('1D6')) + ' Combat Rnds')
            if task_time == 3:
                self.tasktime_result.setText(str(roll('1D6') * 10) + ' Seconds')
            if task_time == 4:
                self.tasktime_result.setText(str(roll('1D6')) + ' Minutes')
            if task_time == 5:
                self.tasktime_result.setText(str(roll('1D6') * 10) + ' Minutes')
            if task_time == 6:
                self.tasktime_result.setText(str(roll('1D6')) + ' Hours')
            if task_time == 7:
                self.tasktime_result.setText(str(roll('1D6') * 4) + ' Hours')
            if task_time == 8:
                self.tasktime_result.setText(str(roll('1D6') * 10) + ' Hours')
            if task_time == 9:
                self.tasktime_result.setText(str(roll('1D6')) + ' Days')
        else:
            if not self.muted:

                # Say the Bane roll. Only the female voice can say it for now.
                m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_' + str(self.natural_roll_1 + self.natural_roll_2) + '.mp3')))
                m_media.play()

    def rollBoon_buttonClicked(self):
        '''
        Do a Boon roll
        '''
        die = [0, 0, 0]
        die[0] = roll('1D6')
        die[1] = roll('1D6')
        die[2] = roll('1D6')
        #print die[0], die[1], die[2]
        log.debug('Start Boon roll: %d %d %d' % (die[0], die[1], die[2]))
        die_swap = True
        while die_swap == True:
            die_swap = False
            for j in range(2):
                if die[j] < die[j+1]:
                    temp_die = die[j]
                    die[j] = die[j+1]
                    die[j+1] = temp_die
                    die_swap = True
        #print die[0], die[1], die[2]
        self.roll_type = 'Boon'
        self.natural_roll_1 = die[0]
        self.natural_roll_2 = die[1]
        self.natural_roll_3 = die[2]
        log.debug('Sorted Boon roll: %d %d %d' % (die[0], die[1], die[2]))
        self.natural_roll = self.natural_roll_1 + self.natural_roll_2
        if self.chained_task:
            self.total_rolled = self.natural_roll + self.inputlevel.value() + self.charmod_value + self.inputDM.value() + self.previous_effect_DM
        else:
            self.total_rolled = self.natural_roll + self.inputlevel.value() + self.charmod_value + self.inputDM.value()
        self.rollresult.setText(str(self.total_rolled))
        if self.mixed_dice:
            self.die1Label.setPixmap(QPixmap(':/images/die1_' + str(self.natural_roll_1) + self.dice_list[randint(1, len(self.dice_list)) - 1] + '.png'))
            self.die2Label.setPixmap(QPixmap(':/images/die2_' + str(self.natural_roll_2) + self.dice_list[randint(1, len(self.dice_list)) - 1] + '.png'))
            self.die3Label.setPixmap(QPixmap(':/images/die3_' + str(self.natural_roll_3) + self.dice_list[randint(1, len(self.dice_list)) - 1] + '.png'))
        else:
            self.die1Label.setPixmap(QPixmap(':/images/die1_' + str(self.natural_roll_1) + self.dice_type + '.png'))
            self.die2Label.setPixmap(QPixmap(':/images/die2_' + str(self.natural_roll_2) + self.dice_type + '.png'))
            self.die3Label.setPixmap(QPixmap(':/images/die3_' + str(self.natural_roll_3) + self.dice_type + '.png'))
        if self.target_num != 0:
            self.blank_graph = False
            self.roll_effect = self.total_rolled - self.target_num
            if self.roll_effect <= -6:
                self.effect_result.setText('%d: Exceptional Failure' % self.roll_effect)
                self.next_effect_DM = -3
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_exceptional_failure.mp3')))
                    m_media.play()
            if self.roll_effect >= -5 and self.roll_effect <= -2:
                self.effect_result.setText('%d: Average Failure' % self.roll_effect)
                self.next_effect_DM = -2
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_average_failure.mp3')))
                    m_media.play()
            if self.roll_effect == -1:
                self.effect_result.setText('%d: Marginal Failure' % self.roll_effect)
                self.next_effect_DM = -1
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_marginal_failure.mp3')))
                    m_media.play()
            if self.roll_effect == 0:
                self.effect_result.setText('%d: Marginal Success' % self.roll_effect)
                self.next_effect_DM = 0
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_marginal_success.mp3')))
                    m_media.play()
            if self.roll_effect >= 1 and self.roll_effect <= 5:
                self.effect_result.setText('%d: Average Success' % self.roll_effect)
                self.next_effect_DM = 1
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_average_success.mp3')))
                    m_media.play()
            if self.roll_effect >= 6:
                self.effect_result.setText('%d: Exceptional Success' % self.roll_effect)
                self.next_effect_DM = 2
                if not self.muted:
                    m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_exceptional_success.mp3')))
                    m_media.play()

            # reset the damage area at the bottom
            self.effect_damage.setText(str(self.roll_effect))
            self.inputdice.setValue(1)
            self.inputDamageDM.setValue(0)
            self.totalDamage.setText('')
            self.update_graph()

            # calculate the amount of time spent on the task
            task_time = self.selNewTimeframe.currentIndex()
            if task_time == 0:
                self.tasktime_result.setText('Not Available')
            if task_time == 1:
                self.tasktime_result.setText(str(roll('1D6')) + ' Seconds')
            if task_time == 2:
                self.tasktime_result.setText(str(roll('1D6')) + ' Combat Rnds')
            if task_time == 3:
                self.tasktime_result.setText(str(roll('1D6') * 10) + ' Seconds')
            if task_time == 4:
                self.tasktime_result.setText(str(roll('1D6')) + ' Minutes')
            if task_time == 5:
                self.tasktime_result.setText(str(roll('1D6') * 10) + ' Minutes')
            if task_time == 6:
                self.tasktime_result.setText(str(roll('1D6')) + ' Hours')
            if task_time == 7:
                self.tasktime_result.setText(str(roll('1D6') * 4) + ' Hours')
            if task_time == 8:
                self.tasktime_result.setText(str(roll('1D6') * 10) + ' Hours')
            if task_time == 9:
                self.tasktime_result.setText(str(roll('1D6')) + ' Days')
        else:
            if not self.muted:

                # Say the Boon roll. Only the female voice can say it for now.
                m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_' + str(self.natural_roll_1 + self.natural_roll_2) + '.mp3')))
                m_media.play()

    def rollD66_buttonClicked(self):
        '''
        Do a D66 roll
        '''
        self.target_num = 0
        self.selDiff.setCurrentIndex(self.target_num)
        self.unknown = False
        self.inputchar.setValue(7)
        self.inputlevel.setValue(0)
        self.charmod_value = 0
        self.charmod.setText(str(self.charmod_value))
        self.inputDM.setValue(0)
        self.previous_effect_DM = 0
        self.next_effect_DM = 0
        self.selChained.setChecked(False)
        self.roll_type = '2D'
        self.natural_roll_1 = roll('1D6')
        self.natural_roll_2 = roll('1D6')
        log.debug('D66 roll: %d%d' % (self.natural_roll_1, self.natural_roll_2))
        self.total_rolled = self.natural_roll_1 * 10 + self.natural_roll_2
        self.rollresult.setText(str(self.total_rolled))
        if self.mixed_dice:
            self.die1Label.setPixmap(QPixmap(':/images/die1_' + str(self.natural_roll_1) + self.dice_list[randint(1, len(self.dice_list)) - 1] + '.png'))
            self.die2Label.setPixmap(QPixmap(':/images/die2_' + str(self.natural_roll_2) + self.dice_list[randint(1, len(self.dice_list)) - 1] + '.png'))
        else:
            self.die1Label.setPixmap(QPixmap(':/images/die1_' + str(self.natural_roll_1) + self.dice_type + '.png'))
            self.die2Label.setPixmap(QPixmap(':/images/die2_' + str(self.natural_roll_2) + self.dice_type + '.png'))
        self.die3Label.setPixmap(QPixmap(':/images/die3_0.png'))
        if not self.muted:

            # Say the D66 roll. Only the female voice can say it for now.
            m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_' + str(self.natural_roll_1) + str(self.natural_roll_2) + '.mp3')))
            m_media.play()
        
        # reset the screen
        self.effect_result.setText('')
        self.effect_damage.setText('')
        self.blank_graph = True
        self.inputarmor.setValue(0)
        self.inputdice.setValue(1)
        self.inputDamageDM.setValue(0)
        self.inputap.setValue(0)
        self.totalDamage.setText('')
        self.roll_effect = 0

    def clearall_buttonClicked(self):
        '''
        Clear all the fields
        '''
        log.debug('Clear all fields')
        self.target_num = 0
        self.selDiff.setCurrentIndex(self.target_num)
        self.unknown = False
        self.inputchar.setValue(7)
        self.inputlevel.setValue(0)
        self.charmod_value = 0
        self.charmod.setText(str(self.charmod_value))
        self.inputDM.setValue(0)
        self.die1Label.setPixmap(QPixmap(':/images/die1_0.png'))
        self.die2Label.setPixmap(QPixmap(':/images/die2_0.png'))
        self.die3Label.setPixmap(QPixmap(':/images/die3_0.png'))
        self.rollresult.setText('')
        self.tasktime_result.setText('')
        self.effect_result.setText('')
        self.effect_damage.setText('')
        self.roll_type = '2D'
        self.blank_graph = True
        self.previous_effect_DM = 0
        self.next_effect_DM = 0
        self.inputarmor.setValue(0)
        self.selCover.setCurrentIndex(0)
        self.inputdice.setValue(1)
        self.inputDamageDM.setValue(0)
        self.inputap.setValue(0)
        self.totalDamage.setText('')
        self.roll_effect = 0
        self.rollInput.clear()
        self.rollBrowser.clear()

    def cleardamage_buttonClicked(self):
        '''
        Clear just the damage fields
        '''
        log.debug('Clear damage fields')
        self.inputarmor.setValue(0)
        self.selCover.setCurrentIndex(0)
        self.inputdice.setValue(1)
        self.inputDamageDM.setValue(0)
        self.inputap.setValue(0)
        self.totalDamage.setText('')

    def inputarmor_valueChanged(self):
        '''
        An armor value was entered
        '''
        self.totalDamage.setText('')
        
    def inputdice_valueChanged(self):
        '''
        The number of damage dice was entered
        '''
        self.totalDamage.setText('')

    def damage_buttonClicked(self):
        '''
        The "D" damage button was clicked/rolled
        '''
        self.effect_damage.setText(str(self.roll_effect))
        self.actual_armor = self.inputarmor.value() + self.cover_modifier - self.inputap.value()
        if self.actual_armor < 0:
            self.actual_armor = 0
        self.damage_amount = roll(str(self.inputdice.value()) + 'D6') + self.inputDamageDM.value() + self.roll_effect
        self.total_damage = self.damage_amount - self.actual_armor
        if self.total_damage < 0:
            self.total_damage = 0
        if self.roll_effect >= 6:
            if self.total_damage == 0:
                self.total_damage = 1
        self.totalDamage.setText(str(self.total_damage))

    def destructive_buttonClicked(self):
        '''
        The "DD" damage button was clicked/rolled
        '''
        self.effect_damage.setText('')
        self.actual_armor = self.inputarmor.value() + self.cover_modifier - self.inputap.value() * 10
        if self.actual_armor < 0:
            self.actual_armor = 0
        if self.inputDamageDM.value() < 0:
            self.damage_amount = roll(str(self.inputdice.value()) + 'DD' + str(self.inputDamageDM.value()))
        else:
            self.damage_amount = roll(str(self.inputdice.value()) + 'DD+' + str(self.inputDamageDM.value()))
        self.total_damage = self.damage_amount - self.actual_armor
        if self.total_damage < 0:
            self.total_damage = 0
#         if self.roll_effect >= 6:
#             if self.total_damage == 0:
#                 self.total_damage = 1
        self.totalDamage.setText(str(self.total_damage))

    def inputdamageDM_valueChanged(self):
        '''
        The DM for damage was entered
        '''
        self.totalDamage.setText('')

    def inputap_valueChanged(self):
        '''
        A value for AP (armor piercing trait) was entered
        '''
        self.totalDamage.setText('')
    
    def selCover_valueChanged(self):
        '''
        A hidden cover value was selected
        '''
        cover_amount = [0, 2, 6, 8, 10, 15, 20]
        if self.selCover.currentIndex() == 0:
            self.cover_modifier = 0
        elif self.selCover.currentIndex() >= 1 and self.selCover.currentIndex() <= 6:
            self.cover_modifier = cover_amount[self.selCover.currentIndex()]
            log.debug('Cover Modifier added: (+%d)' % self.cover_modifier)
        
    def MaleVoice_menu(self):
        '''
        Use a male voice
        '''
        self.male_voice = True
        self.female_voice = False
        self.robot_voice = False
        self.actionMaleVoice.setDisabled(self.male_voice)
        self.actionFemaleVoice.setDisabled(self.female_voice)
        self.actionRobotVoice.setDisabled(self.robot_voice)
        self.voice_type = 'male'
        m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_activated.mp3')))
        m_media.play()
        self.muted = False
        self.actionPlaySample.setDisabled(self.muted)
        self.actionMute.setDisabled(self.muted)
        log.debug('Male voice selected')

    def FemaleVoice_menu(self):
        '''
        Use a female voice
        '''
        self.male_voice = False
        self.female_voice = True
        self.robot_voice = False
        self.actionMaleVoice.setDisabled(self.male_voice)
        self.actionFemaleVoice.setDisabled(self.female_voice)
        self.actionRobotVoice.setDisabled(self.robot_voice)
        self.voice_type = 'female'
        m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_activated.mp3')))
        m_media.play()
        self.muted = False
        self.actionPlaySample.setDisabled(self.muted)
        self.actionMute.setDisabled(self.muted)
        log.debug('Female voice selected')

    def RobotVoice_menu(self):
        '''
        Use a robot voice
        '''
        self.male_voice = False
        self.female_voice = False
        self.robot_voice = True
        self.actionMaleVoice.setDisabled(self.male_voice)
        self.actionFemaleVoice.setDisabled(self.female_voice)
        self.actionRobotVoice.setDisabled(self.robot_voice)
        self.voice_type = 'robot'
        m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_activated.mp3')))
        m_media.play()
        self.muted = False
        self.actionPlaySample.setDisabled(self.muted)
        self.actionMute.setDisabled(self.muted)
        log.debug('Robot voice selected')

    def PlaySample_menu(self):
        m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_travcalc.mp3')))
        m_media.play()
        
    def Mute_menu(self):
        '''
        Don't use any voice (muted voice)
        '''
        m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_running_silent.mp3')))
        m_media.play()
        self.muted = True
        self.actionPlaySample.setDisabled(self.muted)
        self.actionMute.setDisabled(self.muted)
        self.voice_type = 'none'
        self.male_voice = False
        self.female_voice = False
        self.robot_voice = False
        self.actionMaleVoice.setDisabled(self.male_voice)
        self.actionFemaleVoice.setDisabled(self.female_voice)
        self.actionRobotVoice.setDisabled(self.robot_voice)
        log.debug('Muted voice')
        
    def StandardDice_menu(self):
        '''
        set flags for standard dice use
        '''
        self.standard_dice = True
        self.traveller_dice = False
        self.ako_dice = False
        self.metal_dice = False
        self.cubble_dice = False
        self.roman_dice = False
        self.gridgroove_dice = False
        self.yellow_dice = False
        self.shonner_dice = False
        self.question_dice = False
        self.mixed_dice = False
        self.actionStandardDice.setDisabled(self.standard_dice)
        self.actionTravellerDice.setDisabled(self.traveller_dice)
        self.actionAKODice.setDisabled(self.ako_dice)
        self.actionMetalDice.setDisabled(self.metal_dice)
        self.actionCUBBLEDice.setDisabled(self.cubble_dice)
        self.actionRomanDice.setDisabled(self.roman_dice)
        self.actionGridGrooveDice.setDisabled(self.gridgroove_dice)
        self.actionYellowDice.setDisabled(self.yellow_dice)
        self.actionSHONNERDice.setDisabled(self.shonner_dice)
        self.actionQuestionDice.setDisabled(self.question_dice)
        self.actionMixedDice.setDisabled(self.mixed_dice)
        self.dice_type = 'st'
        log.debug('Standard dice selected')
        
    def TravellerDice_menu(self):
        '''
        set flags for Traveller dice use
        '''
        self.standard_dice = False
        self.traveller_dice = True
        self.ako_dice = False
        self.metal_dice = False
        self.cubble_dice = False
        self.roman_dice = False
        self.gridgroove_dice = False
        self.yellow_dice = False
        self.shonner_dice = False
        self.question_dice = False
        self.mixed_dice = False
        self.actionStandardDice.setDisabled(self.standard_dice)
        self.actionTravellerDice.setDisabled(self.traveller_dice)
        self.actionAKODice.setDisabled(self.ako_dice)
        self.actionMetalDice.setDisabled(self.metal_dice)
        self.actionCUBBLEDice.setDisabled(self.cubble_dice)
        self.actionRomanDice.setDisabled(self.roman_dice)
        self.actionGridGrooveDice.setDisabled(self.gridgroove_dice)
        self.actionYellowDice.setDisabled(self.yellow_dice)
        self.actionSHONNERDice.setDisabled(self.shonner_dice)
        self.actionQuestionDice.setDisabled(self.question_dice)
        self.actionMixedDice.setDisabled(self.mixed_dice)
        self.dice_type = 'tr'
        log.debug('Traveller dice selected')

    def AKODice_menu(self):
        '''
        set flags for AKO dice use
        '''
        self.standard_dice = False
        self.traveller_dice = False
        self.ako_dice = True
        self.metal_dice = False
        self.cubble_dice = False
        self.roman_dice = False
        self.gridgroove_dice = False
        self.yellow_dice = False
        self.shonner_dice = False
        self.question_dice = False
        self.mixed_dice = False
        self.actionStandardDice.setDisabled(self.standard_dice)
        self.actionTravellerDice.setDisabled(self.traveller_dice)
        self.actionAKODice.setDisabled(self.ako_dice)
        self.actionMetalDice.setDisabled(self.metal_dice)
        self.actionCUBBLEDice.setDisabled(self.cubble_dice)
        self.actionRomanDice.setDisabled(self.roman_dice)
        self.actionGridGrooveDice.setDisabled(self.gridgroove_dice)
        self.actionYellowDice.setDisabled(self.yellow_dice)
        self.actionSHONNERDice.setDisabled(self.shonner_dice)
        self.actionQuestionDice.setDisabled(self.question_dice)
        self.actionMixedDice.setDisabled(self.mixed_dice)
        self.dice_type = 'ak'
        log.debug('AKO dice selected')

    def MetalDice_menu(self):
        '''
        set flags for metal dice use
        '''
        self.standard_dice = False
        self.traveller_dice = False
        self.ako_dice = False
        self.metal_dice = True
        self.cubble_dice = False
        self.roman_dice = False
        self.gridgroove_dice = False
        self.yellow_dice = False
        self.shonner_dice = False
        self.question_dice = False
        self.mixed_dice = False
        self.actionStandardDice.setDisabled(self.standard_dice)
        self.actionTravellerDice.setDisabled(self.traveller_dice)
        self.actionAKODice.setDisabled(self.ako_dice)
        self.actionMetalDice.setDisabled(self.metal_dice)
        self.actionCUBBLEDice.setDisabled(self.cubble_dice)
        self.actionRomanDice.setDisabled(self.roman_dice)
        self.actionGridGrooveDice.setDisabled(self.gridgroove_dice)
        self.actionYellowDice.setDisabled(self.yellow_dice)
        self.actionSHONNERDice.setDisabled(self.shonner_dice)
        self.actionQuestionDice.setDisabled(self.question_dice)
        self.actionMixedDice.setDisabled(self.mixed_dice)
        self.dice_type = 'me'
        log.debug('Metal dice selected')

    def CUBBLEDice_menu(self):
        '''
        set flags for CUBBLED dice use
        '''
        self.standard_dice = False
        self.traveller_dice = False
        self.ako_dice = False
        self.metal_dice = False
        self.cubble_dice = True
        self.roman_dice = False
        self.gridgroove_dice = False
        self.yellow_dice = False
        self.shonner_dice = False
        self.question_dice = False
        self.mixed_dice = False
        self.actionStandardDice.setDisabled(self.standard_dice)
        self.actionTravellerDice.setDisabled(self.traveller_dice)
        self.actionAKODice.setDisabled(self.ako_dice)
        self.actionMetalDice.setDisabled(self.metal_dice)
        self.actionCUBBLEDice.setDisabled(self.cubble_dice)
        self.actionRomanDice.setDisabled(self.roman_dice)
        self.actionGridGrooveDice.setDisabled(self.gridgroove_dice)
        self.actionYellowDice.setDisabled(self.yellow_dice)
        self.actionSHONNERDice.setDisabled(self.shonner_dice)
        self.actionQuestionDice.setDisabled(self.question_dice)
        self.actionMixedDice.setDisabled(self.mixed_dice)
        self.dice_type = 'cu'
        log.debug('CUBBLE dice selected')
        
    def RomanDice_menu(self):
        '''
        set flags for Roman dice use
        '''
        self.standard_dice = False
        self.traveller_dice = False
        self.ako_dice = False
        self.metal_dice = False
        self.cubble_dice = False
        self.roman_dice = True
        self.gridgroove_dice = False
        self.yellow_dice = False
        self.shonner_dice = False
        self.question_dice = False
        self.mixed_dice = False
        self.actionStandardDice.setDisabled(self.standard_dice)
        self.actionTravellerDice.setDisabled(self.traveller_dice)
        self.actionAKODice.setDisabled(self.ako_dice)
        self.actionMetalDice.setDisabled(self.metal_dice)
        self.actionCUBBLEDice.setDisabled(self.cubble_dice)
        self.actionRomanDice.setDisabled(self.roman_dice)
        self.actionGridGrooveDice.setDisabled(self.gridgroove_dice)
        self.actionYellowDice.setDisabled(self.yellow_dice)
        self.actionSHONNERDice.setDisabled(self.shonner_dice)
        self.actionQuestionDice.setDisabled(self.question_dice)
        self.actionMixedDice.setDisabled(self.mixed_dice)
        self.dice_type = 'ro'
        log.debug('Roman dice selected')
        
    def GridGrooveDice_menu(self):
        '''
        set flags for GridGroove dice use
        '''
        self.standard_dice = False
        self.traveller_dice = False
        self.ako_dice = False
        self.metal_dice = False
        self.cubble_dice = False
        self.roman_dice = False
        self.gridgroove_dice = True
        self.yellow_dice = False
        self.shonner_dice = False
        self.question_dice = False
        self.mixed_dice = False
        self.actionStandardDice.setDisabled(self.standard_dice)
        self.actionTravellerDice.setDisabled(self.traveller_dice)
        self.actionAKODice.setDisabled(self.ako_dice)
        self.actionMetalDice.setDisabled(self.metal_dice)
        self.actionCUBBLEDice.setDisabled(self.cubble_dice)
        self.actionRomanDice.setDisabled(self.roman_dice)
        self.actionGridGrooveDice.setDisabled(self.gridgroove_dice)
        self.actionYellowDice.setDisabled(self.yellow_dice)
        self.actionSHONNERDice.setDisabled(self.shonner_dice)
        self.actionQuestionDice.setDisabled(self.question_dice)
        self.actionMixedDice.setDisabled(self.mixed_dice)
        self.dice_type = 'gg'
        log.debug('Grid Groove dice selected')
    
    def YellowDice_menu(self):
        '''
        set flags for Yellow dice use
        '''
        self.standard_dice = False
        self.traveller_dice = False
        self.ako_dice = False
        self.metal_dice = False
        self.cubble_dice = False
        self.roman_dice = False
        self.gridgroove_dice = False
        self.yellow_dice = True
        self.shonner_dice = False
        self.question_dice = False
        self.mixed_dice = False
        self.actionStandardDice.setDisabled(self.standard_dice)
        self.actionTravellerDice.setDisabled(self.traveller_dice)
        self.actionAKODice.setDisabled(self.ako_dice)
        self.actionMetalDice.setDisabled(self.metal_dice)
        self.actionCUBBLEDice.setDisabled(self.cubble_dice)
        self.actionRomanDice.setDisabled(self.roman_dice)
        self.actionGridGrooveDice.setDisabled(self.gridgroove_dice)
        self.actionYellowDice.setDisabled(self.yellow_dice)
        self.actionSHONNERDice.setDisabled(self.shonner_dice)
        self.actionQuestionDice.setDisabled(self.question_dice)
        self.actionMixedDice.setDisabled(self.mixed_dice)
        self.dice_type = 'ye'
        log.debug('Yellow dice selected')
    
    def SHONNERDice_menu(self):
        '''
        set flags for SHONNER dice use
        '''
        self.standard_dice = False
        self.traveller_dice = False
        self.ako_dice = False
        self.metal_dice = False
        self.cubble_dice = False
        self.roman_dice = False
        self.gridgroove_dice = False
        self.yellow_dice = False
        self.shonner_dice = True
        self.question_dice = False
        self.mixed_dice = False
        self.actionStandardDice.setDisabled(self.standard_dice)
        self.actionTravellerDice.setDisabled(self.traveller_dice)
        self.actionAKODice.setDisabled(self.ako_dice)
        self.actionMetalDice.setDisabled(self.metal_dice)
        self.actionCUBBLEDice.setDisabled(self.cubble_dice)
        self.actionRomanDice.setDisabled(self.roman_dice)
        self.actionGridGrooveDice.setDisabled(self.gridgroove_dice)
        self.actionYellowDice.setDisabled(self.yellow_dice)
        self.actionSHONNERDice.setDisabled(self.shonner_dice)
        self.actionQuestionDice.setDisabled(self.question_dice)
        self.actionMixedDice.setDisabled(self.mixed_dice)
        self.dice_type = 'sh'
        log.debug('SHONNER dice selected')

    def QuestionDice_menu(self):
        '''
        set flags for Question Mark dice use
        '''
        self.standard_dice = False
        self.traveller_dice = False
        self.ako_dice = False
        self.metal_dice = False
        self.cubble_dice = False
        self.roman_dice = False
        self.gridgroove_dice = False
        self.yellow_dice = False
        self.shonner_dice = False
        self.question_dice = True
        self.mixed_dice = False
        self.actionStandardDice.setDisabled(self.standard_dice)
        self.actionTravellerDice.setDisabled(self.traveller_dice)
        self.actionAKODice.setDisabled(self.ako_dice)
        self.actionMetalDice.setDisabled(self.metal_dice)
        self.actionCUBBLEDice.setDisabled(self.cubble_dice)
        self.actionRomanDice.setDisabled(self.roman_dice)
        self.actionGridGrooveDice.setDisabled(self.gridgroove_dice)
        self.actionYellowDice.setDisabled(self.yellow_dice)
        self.actionSHONNERDice.setDisabled(self.shonner_dice)
        self.actionQuestionDice.setDisabled(self.question_dice)
        self.actionMixedDice.setDisabled(self.mixed_dice)
        self.dice_type = 'qu'
        log.debug('Question dice selected')
        
    def MixedDice_menu(self):
        '''
        set flags for mixed-use dice
        '''
        self.standard_dice = False
        self.traveller_dice = False
        self.ako_dice = False
        self.metal_dice = False
        self.cubble_dice = False
        self.roman_dice = False
        self.gridgroove_dice = False
        self.yellow_dice = False
        self.shonner_dice = False
        self.question_dice = False
        self.mixed_dice = True
        self.actionStandardDice.setDisabled(self.standard_dice)
        self.actionTravellerDice.setDisabled(self.traveller_dice)
        self.actionAKODice.setDisabled(self.ako_dice)
        self.actionMetalDice.setDisabled(self.metal_dice)
        self.actionCUBBLEDice.setDisabled(self.cubble_dice)
        self.actionRomanDice.setDisabled(self.roman_dice)
        self.actionGridGrooveDice.setDisabled(self.gridgroove_dice)
        self.actionYellowDice.setDisabled(self.yellow_dice)
        self.actionSHONNERDice.setDisabled(self.shonner_dice)
        self.actionQuestionDice.setDisabled(self.question_dice)
        self.actionMixedDice.setDisabled(self.mixed_dice)
        self.dice_type = ''
        log.debug('Mixed dice selected')
        
    def Visit_Blog(self):
        '''
        open web browser to blog URL
        '''
        os.startfile('http://shawndriscoll.blogspot.com')
        
    def Feedback(self):
        '''
        open an email letter to send as feedback to the author
        '''
        os.startfile('mailto:shawndriscoll@hotmail.com?subject=Feedback: ' + __app__ + ' for Mongoose Traveller 2nd Edition')
        
    def Overview_menu(self):
        '''
        open this app's PDF manual
        '''
        log.info(__app__ + ' looking for PDF manual...')
        os.startfile('pytravcalc_manual.pdf')
        #os.startfile(CURRENT_DIR + '\images\die1_2q.png')
        log.info(__app__ + ' found PDF manual. Opening...')
        
    def actionAbout_triggered(self):
        '''
        open the About window
        '''
        if not self.muted:
            m_media.setMedia(MM.QMediaContent(QUrl('qrc:/sounds/' + self.voice_type + '_traveller_ownership.mp3')))
            #m_media.setMedia(MM.QMediaContent(QUrl.fromLocalFile(CURRENT_DIR + '\sounds\\' + 'female' + '_traveller_ownership.mp3')))
            m_media.play()
            #p = vlc.MediaPlayer("file:///path/to/track.mp3")
            #p = vlc.MediaPlayer('file:///' + CURRENT_DIR + '/sounds/' + 'female' + '_traveller_ownership.mp3')
            #p.play()
        log.info(__app__ + ' show about...')
        self.popAboutDialog.show()
    
    def manual_roll(self):
        '''
        A roll was inputed manually
        '''
        log.debug('Manually entered')
        dice_entered = self.rollInput.text()
        roll_returned = roll(dice_entered)
        if roll_returned == -9999:
            returned_line = dice_entered + ' = ' + '<span style=" color:#ff0000;">' + str(roll_returned) + '</span>'
        else:
            returned_line = dice_entered + ' = ' + str(roll_returned)
        self.rollBrowser.append(returned_line)

    def clearRollHistoryClicked(self):
        '''
        Clear the roll history
        '''
        log.debug('Clear roll history')
        self.rollInput.clear()
        self.rollBrowser.clear()
    
    def alert_window(self):
        '''
        open the Alert window
        '''
        log.warning(__app__ + ' show Beta expired PyQt5 alertDialog...')
        self.popAlertDialog.show()

    def quitButton_clicked(self):
        '''
        select "Quit" from the drop-down menu
        '''
        log.info(__app__ + ' quiting...')
        log.info(__app__ + ' DONE.')
        self.close()
        
    def update_graph(self):
        '''
        display a 2D, Boon, or Bane graph of the dice roll result
        '''
        if self.roll_type == '2D':
            log.debug('Access 2D (default) graph')
            xper_range = '100  97.2  91.7  83.3  72.2  58.3  41.7  27.8  16.7  8.3  2.8'
            percent = [2.778419, 5.5540770000000004, 8.3340270000000007, 11.111444000000001, 13.898837, 16.663181999999999, 13.891541999999999, 11.105839, 8.3293949999999999, 5.5563149999999997, 2.776923]
        else:
            if self.roll_type == 'Boon':
                log.debug('Access Boon graph')
                xper_range = '100  99.5  98.1  94.9  89.3  80.6  68.1  52.3  35.7  20.0  7.4'
                percent = [0.46429999999999999, 1.38855, 3.2388499999999998, 5.5849500000000001, 8.827, 12.52575, 15.7102, 16.633199999999999, 15.7501, 12.461499999999999, 7.4156000000000004]
            else:
                log.debug('Access Bane graph')
                xper_range = '100  92.6  80.1  64.4  47.7  31.9  19.5  10.7  5.1  1.9  0.5'
                percent = [7.4225500000000002, 12.512600000000001, 15.69895, 16.665050000000001, 15.7624, 12.502649999999999, 8.7778500000000008, 5.5618999999999996, 3.2383000000000002, 1.40065, 0.45710000000000001]

        if not self.blank_graph:
            die_range = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            yper_range = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']
            bar_height = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
          
            count_offset = self.total_rolled - self.natural_roll
            
            for i in range(len(die_range)):
                die_range[i] = i + count_offset + 2
            
            for i in range(len(percent)):
                if i + 2 == self.natural_roll:
                    bar_height[i] = percent[i]

        else:

            die_range = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            xper_range = ''
            yper_range = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']
            percent = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            
        self.mpl.canvas.ax.clear()
        self.mpl.canvas.ax.bar(np.arange(len(die_range)), percent, width=0.6, alpha=.3, color='b')
        self.mpl.canvas.ax.set_xlim(xmin=-0.25, xmax=len(die_range)-0.75)
        self.mpl.canvas.ax.set_xticks(range(len(die_range)))
        self.mpl.canvas.ax.set_xticklabels(die_range)
        ticks_font = font_manager.FontProperties(family='Optima', style='normal', size=12, weight='normal', stretch='normal')
        for label in self.mpl.canvas.ax.get_xticklabels():
            label.set_fontproperties(ticks_font)
        title_font = font_manager.FontProperties(family='Optima', style='normal', size=6, weight='normal', stretch='normal')
        label = self.mpl.canvas.ax.set_title(xper_range)
        label.set_fontproperties(title_font)
        self.mpl.canvas.ax.set_yticks(range(0,19,1))
        self.mpl.canvas.ax.set_yticklabels(yper_range)
        ticks_font = font_manager.FontProperties(family='Optima', style='normal', size=6, weight='normal', stretch='normal')
        for label in self.mpl.canvas.ax.get_yticklabels():
            label.set_fontproperties(ticks_font)
        ylabel_font = font_manager.FontProperties(family='Optima', style='normal', size=10, weight='normal', stretch='normal')
        #self.mpl.canvas.ax.set_ylabel('Percentages')
        label = self.mpl.canvas.ax.set_ylabel('Percentages')
        label.set_fontproperties(ylabel_font)
        #self.mpl.canvas.ax.get_xaxis().grid(True)
        self.mpl.canvas.ax.get_yaxis().grid(True)
        
        #self.mpl.canvas.draw()
        
        if not self.blank_graph:        
            if self.roll_effect <= -6:
                self.mpl.canvas.ax.bar(np.arange(len(die_range)), bar_height, width=0.6, alpha=1.0, color='r')
            if self.roll_effect >= -5 and self.roll_effect <= -2:
                self.mpl.canvas.ax.bar(np.arange(len(die_range)), bar_height, width=0.6, alpha=.6, color='orange')
            if self.roll_effect == -1:
                self.mpl.canvas.ax.bar(np.arange(len(die_range)), bar_height, width=0.6, alpha=.4, color='orange')
            if self.roll_effect == 0:
                self.mpl.canvas.ax.bar(np.arange(len(die_range)), bar_height, width=0.6, alpha=.4, color='g')
            if self.roll_effect >= 1 and self.roll_effect <= 5:
                self.mpl.canvas.ax.bar(np.arange(len(die_range)), bar_height, width=0.6, alpha=.6, color='g')
            if self.roll_effect >= 6:
                self.mpl.canvas.ax.bar(np.arange(len(die_range)), bar_height, width=0.6, alpha=1.0, color='c')
                
            self.mpl.canvas.ax.set_xlim(xmin=-0.25, xmax=len(die_range)-0.75)
            self.mpl.canvas.ax.set_xticks(range(len(die_range)))
            self.mpl.canvas.ax.set_xticklabels(die_range)
            ticks_font = font_manager.FontProperties(family='Optima', style='normal', size=12, weight='normal', stretch='normal')
            for label in self.mpl.canvas.ax.get_xticklabels():
                label.set_fontproperties(ticks_font)
            title_font = font_manager.FontProperties(family='Optima', style='normal', size=6, weight='normal', stretch='normal')
            label = self.mpl.canvas.ax.set_title(xper_range)
            label.set_fontproperties(title_font)
            self.mpl.canvas.ax.set_yticks(range(0,19,1))
            self.mpl.canvas.ax.set_yticklabels(yper_range)
            ticks_font = font_manager.FontProperties(family='Optima', style='normal', size=6, weight='normal', stretch='normal')
            for label in self.mpl.canvas.ax.get_yticklabels():
                label.set_fontproperties(ticks_font)
            ylabel_font = font_manager.FontProperties(family='Optima', style='normal', size=10, weight='normal', stretch='normal')
            #self.mpl.canvas.ax.set_ylabel('Percentages')
            label = self.mpl.canvas.ax.set_ylabel('Percentages')
            label.set_fontproperties(ylabel_font)
            #self.mpl.canvas.ax.get_xaxis().grid(True)
            self.mpl.canvas.ax.get_yaxis().grid(True)

        self.mpl.canvas.draw()


if __name__ == '__main__':

    '''
    Technically, this program starts right here when run.
    If this program is imported instead of run, none of the code below is executed.
    '''

#     logging.basicConfig(filename = 'PyTravCalc.log',
#                         level = logging.DEBUG,
#                         format = '%(asctime)s %(levelname)s %(name)s - %(message)s',
#                         datefmt='%a, %d %b %Y %H:%M:%S',
#                         filemode = 'w')

    log = logging.getLogger('PyTravCalc')
    log.setLevel(logging.DEBUG)

    if not os.path.exists('Logs'):
        os.mkdir('Logs')
    
    fh = logging.FileHandler('Logs/PyTravCalc.log', 'w')
 
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s - %(message)s', datefmt = '%a, %d %b %Y %H:%M:%S')
    fh.setFormatter(formatter)
    log.addHandler(fh)

    log.info('Logging started.')
    log.info(__app__ + ' starting...')

    trange = time.localtime()

    log.info(__app__ + ' started, and running...')
    
    if len(sys.argv) < 2:

        if trange[0] > 2022 or trange[1] > 7:
            __expired_tag__ = True
            __app__ += ' [EXPIRED]'

        app = QApplication(sys.argv)
        
        # Use print(QStyleFactory.keys()) to find a setStyle you like, instead of 'Fusion'

        # app.setStyle('Fusion')
        
        # darkPalette = QPalette()
        # darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
        # darkPalette.setColor(QPalette.WindowText, Qt.white)
        # darkPalette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
        # darkPalette.setColor(QPalette.Base, QColor(42, 42, 42))
        # darkPalette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        # darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
        # darkPalette.setColor(QPalette.ToolTipText, Qt.white)
        # darkPalette.setColor(QPalette.Text, Qt.white)
        # darkPalette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
        # darkPalette.setColor(QPalette.Dark, QColor(35, 35, 35))
        # darkPalette.setColor(QPalette.Shadow, QColor(20, 20, 20))
        # darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
        # darkPalette.setColor(QPalette.ButtonText, Qt.white)
        # darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
        # darkPalette.setColor(QPalette.BrightText, Qt.red)
        # darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))
        # darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        # darkPalette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
        # darkPalette.setColor(QPalette.HighlightedText, Qt.white)
        # darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127))
        
        mainApp = MainWindow()
        mainApp.show()

        # app.setPalette(darkPalette)

        #CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
        #print(CURRENT_DIR)

        m_media = MM.QMediaPlayer()        

        app.exec_()
    
    elif trange[0] > 2022 or trange[1] > 7:
        __app__ += ' [EXPIRED]'
        '''
        Beta for this app has expired!
        '''
        log.warning(__app__)
        print()
        print(__app__)
        
    elif sys.argv[1] in ['-h', '/h', '--help', '-?', '/?']:
        print()
        print('     Using the CMD prompt to make dice rolls:')
        print("     C:\>PyTravCalc.py roll('2d6')")
        print()
        print('     Or just:')
        print('     C:\>PyTravCalc.py 2d6')
    elif sys.argv[1] in ['-v', '/v', '--version']:
        print()
        print('     PyTravCalc, release version ' + __version__ + ' for Python ' + __py_version__)
    else:
        print()
        dice = ''
        if len(sys.argv) > 2:
            for i in range(len(sys.argv)):
                if i > 0:
                    dice += sys.argv[i]
        else:
            dice = sys.argv[1]
        if "roll('" in dice:
            num = dice.find("')")
            if num != -1:
                dice = dice[6:num]
                dice = str(dice).upper().strip()
                num = roll(dice)
                if dice != 'TEST' and dice != 'INFO':
                    print("Your '%s' roll is %d." % (dice, num))
                    log.info("The direct call to PyTravCalc with '%s' resulted in %d." % (dice, num))
                elif dice == 'INFO':
                    print('PyTravCalc, release version ' + __version__ + ' for Python ' + __py_version__)
        else:
            dice = str(dice).upper().strip()
            num = roll(dice)
            if dice != 'TEST' and dice != 'INFO':
                print("Your '%s' roll is %d." % (dice, num))
                log.info("The direct call to PyTravCalc with '%s' resulted in %d." % (dice, num))
            elif dice == 'INFO':
                print('PyTravCalc, release version ' + __version__ + ' for Python ' + __py_version__)
