import time
import os
import shutil
import pyreportjasper
import webbrowser
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import loadconfirmation_settings as LCSettings
from all_persistence_class import (LoadConfirmationInstance, ConsigneeRefInstance,
                                   ShipperRefInstance, CarrierInstance, BrokerInstance,
                                   CurrencyInstance, LoadTypeInstance, ConsigneeInstance,
                                   ShipperInstance, UserInstance)
from core.newdialog.choosedialog.allchoosedialog import (ChooseCarrierDialog, ChooseShipperDialog,
                                                         ChooseConsigneeDialog, ChooseBrokerDialog)
from core.newdialog.choosedialog.alldataframes import (CarrierFrame, ShipperFrame,
                                                       ConsigneeFrame, BrokerFrame)
from loadconfirmation_errors import (MissingBrokerInfoError, MissingCarrierInfoError,
                                     MissingConsigneeInfoError, MissingShipperInfoError,
                                     MissingChosenImageError, ImageDimensionError)
from core.workers.allqueries import (LoadTypeQueries, CurrencyQueries)


class NewBrokerDialog(qtw.QDialog):

    def __init__(self, app_settings, dialog_flag, input_broker_instance=None, broker_queries=None):
        super().__init__()
        self.setup_supporting_vars(app_settings, dialog_flag, input_broker_instance, broker_queries)
        self.setup_gui()

    def setup_supporting_vars(self, app_settings, dialog_flag, input_broker_instance, broker_queries):
        self.app_settings = app_settings
        self.dialog_flag = dialog_flag
        self.input_broker_instance = input_broker_instance
        self.broker_queries = broker_queries

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        # frames and layouts
        self.main_box = qtw.QVBoxLayout()
        self.title_frame = qtw.QFrame()
        self.data_frame = qtw.QFrame()
        self.spacer_frame = qtw.QFrame()
        self.buttons_frame = qtw.QFrame()
        self.title_frame_box = qtw.QHBoxLayout()
        self.data_frame_box = qtw.QGridLayout()
        self.button_frame_box = qtw.QHBoxLayout()

        # other controls
        #Labels
        self.title_label = qtw.QLabel('Add New Broker')
        self.broker_name_label = qtw.QLabel("Broker's name")
        self.broker_phone_label = qtw.QLabel('Phone #')
        self.broker_fax_label = qtw.QLabel('Fax')
        self.broker_toll_free_label = qtw.QLabel('Toll Free')
        self.broker_contact_label = qtw.QLabel('Contact Names')
        #EditLines
        self.broker_name_editline = qtw.QLineEdit()
        self.broker_phone_editline = qtw.QLineEdit()
        self.broker_fax_edit_line = qtw.QLineEdit()
        self.broker_toll_free_editline = qtw.QLineEdit()
        self.broker_contact_editline = qtw.QLineEdit()
        #buttons
        self.cncl_button = qtw.QPushButton('     Cancel     ')
        self.ok_button = qtw.QPushButton('     Create      ')

    def setup_gui_object_style_names(self):
        self.title_label.setObjectName('title')
        self.spacer_frame.setObjectName('spacerFrame')

    def layout_gui_objects(self):
        self.setLayout(self.main_box)

        self.main_box.addWidget(self.title_frame)
        self.main_box.addWidget(self.data_frame, stretch=1)
        self.main_box.addWidget(self.buttons_frame)

        self.title_frame.setLayout(self.title_frame_box)
        self.data_frame.setLayout(self.data_frame_box)
        self.buttons_frame.setLayout(self.button_frame_box)

        self.title_frame_box.addWidget(self.title_label, 1, qtc.Qt.AlignCenter)
        self.data_frame_box.addWidget(self.broker_name_label, 0, 0, 1, 1)
        self.data_frame_box.addWidget(self.broker_name_editline, 0, 1, 1, 1)
        self.data_frame_box.addWidget(self.broker_phone_label, 1, 0, 1, 1)
        self.data_frame_box.addWidget(self.broker_phone_editline, 1, 1, 1, 1)
        self.data_frame_box.addWidget(self.broker_fax_label, 2, 0, 1, 1)
        self.data_frame_box.addWidget(self.broker_fax_edit_line, 2, 1, 1, 1)
        self.data_frame_box.addWidget(self.broker_toll_free_label, 3, 0, 1, 1)
        self.data_frame_box.addWidget(self.broker_toll_free_editline, 3, 1, 1, 1)
        self.data_frame_box.addWidget(self.broker_contact_label, 4, 0, 1, 1)
        self.data_frame_box.addWidget(self.broker_contact_editline, 4, 1, 1, 1)
        self.data_frame_box.addWidget(self.spacer_frame, 5, 0, 1, 2)

        self.button_frame_box.addStretch()
        self.button_frame_box.addWidget(self.cncl_button, alignment=qtc.Qt.AlignRight)
        self.button_frame_box.addWidget(self.ok_button, alignment=qtc.Qt.AlignRight)

    def feature_gui_objects(self):
        self.setup_window_geometry()

        #setting up window depending on flagDialog
        # insert, delete, modify or view
        if self.dialog_flag == LCSettings.Settings.INSERT:
            self.title_label.setText('Add New Load Broker')
            self.ok_button.setText('Create')
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.title_label.setText('Delete Broker')
            self.ok_button.setText('Delete')
            self.load_current_data()
            self.disable_editing()
        elif self.dialog_flag == LCSettings.Settings.MODIFY:
            self.title_label.setText('Modify Broker')
            self.ok_button.setText('Modify')
            self.load_current_data()
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.title_label.setText('View Broker')
            self.cncl_button.setVisible(False)
            self.ok_button.setText('Close')
            self.load_current_data()
            self.disable_editing()

    def setup_window_geometry(self):
        window_x_coord = int(self.app_settings.screen_width / 2 - self.app_settings.smallnewwindow_width / 2)
        window_y_coord = int(self.app_settings.screen_height / 2 - self.app_settings.smallnewwindow_height / 2)
        self.setGeometry(window_x_coord, window_y_coord,
                         self.app_settings.smallnewwindow_width, self.app_settings.smallnewwindow_height)
        self.setMinimumSize(self.app_settings.smallnewwindow_width, self.app_settings.smallnewwindow_height)

    def disable_editing(self):
        self.broker_name_editline.setEnabled(False)
        self.broker_phone_editline.setEnabled(False)
        self.broker_fax_edit_line.setEnabled(False)
        self.broker_toll_free_editline.setEnabled(False)
        self.broker_contact_editline.setEnabled(False)

    def load_current_data(self):
        if self.dialog_flag == LCSettings.Settings.INSERT:
            pass
        elif (self.dialog_flag == LCSettings.Settings.DELETE or
            self.dialog_flag == LCSettings.Settings.MODIFY or
            self.dialog_flag == LCSettings.Settings.VIEW):
            self.broker_name_editline.setText(self.input_broker_instance.custombrokername)
            self.broker_phone_editline.setText(self.input_broker_instance.custombrokerphone)
            self.broker_fax_edit_line.setText(self.input_broker_instance.custombrokerfax)
            self.broker_toll_free_editline.setText(self.input_broker_instance.custombrokertollfree)
            self.broker_contact_editline.setText(self.input_broker_instance.custombrokercontact)

    def setup_gui_object_events(self):
        self.cncl_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.process_user_data)

    def process_user_data(self):
        if self.dialog_flag == LCSettings.Settings.INSERT:
            self.new_broker_instance = BrokerInstance(
                custombrokername=self.broker_name_editline.text(),
                custombrokerphone=self.broker_phone_editline.text(),
                custombrokerfax=self.broker_fax_edit_line.text(),
                custombrokertollfree=self.broker_toll_free_editline.text(),
                custombrokercontact=self.broker_contact_editline.text()
            )
            operation_returm_code = self.broker_queries.insert_broker(self.new_broker_instance)
            if operation_returm_code == 0:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Success", "New broker was created",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.accept()
            elif operation_returm_code == 1:
                retry = qtw.QMessageBox.question(self,
                                                 'Fail',
                                                 "Such Broker already exist.\n"
                                                 "Try again?",
                                                 qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)
                if retry == qtw.QMessageBox.Yes:
                    self.broker_name_editline.setFocus()
                else:
                    self.reject()
        elif self.dialog_flag == LCSettings.Settings.MODIFY:
            self.modify_broker_instance = BrokerInstance(
                self.input_broker_instance.custombrokerid,
                self.broker_name_editline.text(),
                self.broker_phone_editline.text(),
                self.broker_fax_edit_line.text(),
                self.broker_toll_free_editline.text(),
                self.broker_contact_editline.text()
            )
            operation_returm_code = self.broker_queries.modify_broker(self.modify_broker_instance)
            if operation_returm_code == 0:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Success", "Broker was modified",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.accept()
            elif operation_returm_code == 1:
                retry = qtw.QMessageBox.question(self,
                                                 'Fail',
                                                 "Such broker already exists.\n"
                                                 "Try again?",
                                                 qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)
                if retry == qtw.QMessageBox.Yes:
                    self.broker_name_editline.setFocus()
                else:
                    self.reject()
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.accept()
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.accept()


class NewCarrierDialog(qtw.QDialog):

    def __init__(self, app_settings, dialog_flag, input_carrier_instance=None, carrier_queries=None):
        super().__init__()
        self.setup_supporting_vars(app_settings, dialog_flag, input_carrier_instance, carrier_queries)
        self.setup_gui()

    def setup_supporting_vars(self, app_settings, dialog_flag, input_carrier_instance, carrier_queries):
        self.app_settings = app_settings
        self.dialog_flag = dialog_flag
        self.input_carrier_instance = input_carrier_instance
        self.carrier_queries = carrier_queries

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        # frames and layouts
        self.main_box = qtw.QVBoxLayout()
        self.title_frame = qtw.QFrame()
        self.data_frame = qtw.QFrame()
        self.spacer_frame = qtw.QFrame()
        self.buttons_frame = qtw.QFrame()
        self.title_frame_box = qtw.QHBoxLayout()
        self.data_frame_box = qtw.QGridLayout()
        self.button_frame_box = qtw.QHBoxLayout()

        # other controls
        #Labels
        self.title_label = qtw.QLabel('Add New Carrier')
        self.carrier_name_label = qtw.QLabel("Carrier Name")
        self.carrier_address_label = qtw.QLabel("Address")
        self.carrier_city_label = qtw.QLabel("City")
        self.carrier_state_label = qtw.QLabel("State")
        self.carrier_country_label = qtw.QLabel("Country")
        self.carrier_postalcode_label = qtw.QLabel("Postal Code")
        self.carrier_phone_label = qtw.QLabel('Phone #')
        self.carrier_fax_label = qtw.QLabel('Fax')
        self.carrier_toll_free_label = qtw.QLabel('Toll Free')
        self.carrier_contact_label = qtw.QLabel('Contact Names')
        #EditLines
        self.carrier_name_editline = qtw.QLineEdit()
        self.carrier_address_editline = qtw.QLineEdit()
        self.carrier_city_editline = qtw.QLineEdit()
        self.carrier_state_editline = qtw.QLineEdit()
        self.carrier_country_edit_line = qtw.QLineEdit()
        self.carrier_postalcode_editline = qtw.QLineEdit()
        self.carrier_phone_editline = qtw.QLineEdit()
        self.carrier_fax_editline = qtw.QLineEdit()
        self.carrier_toll_free_editline = qtw.QLineEdit()
        self.carrier_contact_editline = qtw.QLineEdit()
        #buttons
        self.cncl_button = qtw.QPushButton('     Cancel     ')
        self.ok_button = qtw.QPushButton('     Create     ')

    def setup_gui_object_style_names(self):
        self.title_label.setObjectName('title')
        self.spacer_frame.setObjectName('spacerFrame')

    def layout_gui_objects(self):
        self.setLayout(self.main_box)

        self.main_box.addWidget(self.title_frame)
        self.main_box.addWidget(self.data_frame, stretch=1)
        self.main_box.addWidget(self.buttons_frame)

        self.title_frame.setLayout(self.title_frame_box)
        self.data_frame.setLayout(self.data_frame_box)
        self.buttons_frame.setLayout(self.button_frame_box)

        self.title_frame_box.addWidget(self.title_label, 1, qtc.Qt.AlignCenter)
        self.data_frame_box.addWidget(self.carrier_name_label, 0, 0, 1, 1)
        self.data_frame_box.addWidget(self.carrier_name_editline, 0, 1, 1, 1)
        self.data_frame_box.addWidget(self.carrier_address_label, 1, 0, 1, 1)
        self.data_frame_box.addWidget(self.carrier_address_editline, 1, 1, 1, 1)
        self.data_frame_box.addWidget(self.carrier_city_label, 2, 0, 1, 1)
        self.data_frame_box.addWidget(self.carrier_city_editline, 2, 1, 1, 1)
        self.data_frame_box.addWidget(self.carrier_state_label, 3, 0, 1, 1)
        self.data_frame_box.addWidget(self.carrier_state_editline, 3, 1, 1, 1)
        self.data_frame_box.addWidget(self.carrier_country_label, 4, 0, 1, 1)
        self.data_frame_box.addWidget(self.carrier_country_edit_line, 4, 1, 1, 1)
        self.data_frame_box.addWidget(self.carrier_postalcode_label, 5, 0, 1, 1)
        self.data_frame_box.addWidget(self.carrier_postalcode_editline, 5, 1, 1, 1)
        self.data_frame_box.addWidget(self.carrier_phone_label, 6, 0, 1, 1)
        self.data_frame_box.addWidget(self.carrier_phone_editline, 6, 1, 1, 1)
        self.data_frame_box.addWidget(self.carrier_fax_label, 7, 0, 1, 1)
        self.data_frame_box.addWidget(self.carrier_fax_editline, 7, 1, 1, 1)
        self.data_frame_box.addWidget(self.carrier_toll_free_label, 8, 0, 1, 1)
        self.data_frame_box.addWidget(self.carrier_toll_free_editline, 8, 1, 1, 1)
        self.data_frame_box.addWidget(self.carrier_contact_label, 9, 0, 1, 1)
        self.data_frame_box.addWidget(self.carrier_contact_editline, 9, 1, 1, 1)
        self.data_frame_box.addWidget(self.spacer_frame, 10, 0, 1, 2)

        self.button_frame_box.addStretch()
        self.button_frame_box.addWidget(self.cncl_button, alignment=qtc.Qt.AlignRight)
        self.button_frame_box.addWidget(self.ok_button, alignment=qtc.Qt.AlignRight)

    def feature_gui_objects(self):
        self.setup_window_geometry()

        #setting up window depending on flagDialog
        # insert, delete, modify or view
        if self.dialog_flag == LCSettings.Settings.INSERT:
            self.title_label.setText('Add New Carrier')
            self.ok_button.setText('Create')
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.title_label.setText('Delete Carrier')
            self.ok_button.setText('Delete')
            self.load_current_data()
            self.disable_editing()
        elif self.dialog_flag == LCSettings.Settings.MODIFY:
            self.title_label.setText('Modify Carrier')
            self.ok_button.setText('Modify')
            self.load_current_data()
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.title_label.setText('View Carrier')
            self.cncl_button.setVisible(False)
            self.ok_button.setText('Close')
            self.load_current_data()
            self.disable_editing()

    def setup_window_geometry(self):
        window_x_coord = int(self.app_settings.screen_width / 2 - self.app_settings.smallnewwindow_width / 2)
        window_y_coord = int(self.app_settings.screen_height / 2 - self.app_settings.smallnewwindow_height / 2)
        self.setGeometry(window_x_coord, window_y_coord,
                         self.app_settings.newwindow_width, self.app_settings.newwindow_height)
        self.setMinimumSize(self.app_settings.newwindow_width, self.app_settings.newwindow_height)

    def disable_editing(self):
        self.carrier_name_editline.setEnabled(False)
        self.carrier_address_editline.setEnabled(False)
        self.carrier_city_editline.setEnabled(False)
        self.carrier_state_editline.setEnabled(False)
        self.carrier_country_edit_line.setEnabled(False)
        self.carrier_postalcode_editline.setEnabled(False)
        self.carrier_phone_editline.setEnabled(False)
        self.carrier_fax_editline.setEnabled(False)
        self.carrier_toll_free_editline.setEnabled(False)
        self.carrier_contact_editline.setEnabled(False)

    def load_current_data(self):
        if self.dialog_flag == LCSettings.Settings.INSERT:
            pass
        elif (self.dialog_flag == LCSettings.Settings.DELETE or
              self.dialog_flag == LCSettings.Settings.MODIFY or
              self.dialog_flag == LCSettings.Settings.VIEW):
            self.carrier_name_editline.setText(self.input_carrier_instance.carriername)
            self.carrier_address_editline.setText(self.input_carrier_instance.carrieraddress)
            self.carrier_city_editline.setText(self.input_carrier_instance.carriercity)
            self.carrier_state_editline.setText(self.input_carrier_instance.carrierstate)
            self.carrier_country_edit_line.setText(self.input_carrier_instance.carriercountry)
            self.carrier_postalcode_editline.setText(self.input_carrier_instance.carrierpostalcode)
            self.carrier_phone_editline.setText(self.input_carrier_instance.carrierphone)
            self.carrier_fax_editline.setText(self.input_carrier_instance.carrierfax)
            self.carrier_toll_free_editline.setText(self.input_carrier_instance.carriertollfree)
            self.carrier_contact_editline.setText(self.input_carrier_instance.carriercontact)

    def setup_gui_object_events(self):
        self.cncl_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.process_user_data)

    def process_user_data(self):
        if self.dialog_flag == LCSettings.Settings.INSERT:
            self.new_carrier_instance = CarrierInstance(
                carriername=self.carrier_name_editline.text(),
                carrieraddress=self.carrier_address_editline.text(),
                carriercity=self.carrier_city_editline.text(),
                carrierstate=self.carrier_state_editline.text(),
                carriercountry=self.carrier_country_edit_line.text(),
                carrierpostalcode=self.carrier_postalcode_editline.text(),
                carrierphone=self.carrier_phone_editline.text(),
                carrierfax=self.carrier_fax_editline.text(),
                carriertollfree=self.carrier_toll_free_editline.text(),
                carriercontact=self.carrier_contact_editline.text()
            )
            operation_returm_code = self.carrier_queries.insert_carrier(self.new_carrier_instance)
            if operation_returm_code == 0:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Success", "New carrier was created",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.accept()
            elif operation_returm_code == 1:
                retry = qtw.QMessageBox.question(self,
                                                 'Fail',
                                                 "Such Carrier already exist.\n"
                                                 "Try again?",
                                                 qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)
                if retry == qtw.QMessageBox.Yes:
                    self.carrier_name_editline.setFocus()
                else:
                    self.reject()
        elif self.dialog_flag == LCSettings.Settings.MODIFY:
            self.modify_carrier_instance = CarrierInstance(
                self.input_carrier_instance.carrierid,
                self.carrier_name_editline.text(),
                self.carrier_address_editline.text(),
                self.carrier_city_editline.text(),
                self.carrier_state_editline.text(),
                self.carrier_country_edit_line.text(),
                self.carrier_postalcode_editline.text(),
                self.carrier_phone_editline.text(),
                self.carrier_fax_editline.text(),
                self.carrier_toll_free_editline.text(),
                self.carrier_contact_editline.text()
            )
            operation_returm_code = self.carrier_queries.modify_carrier(self.modify_carrier_instance)
            if operation_returm_code == 0:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Success", "Carrier was modified",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.accept()
            elif operation_returm_code == 1:
                retry = qtw.QMessageBox.question(self,
                                                 'Fail',
                                                 "Such carrier already exists.\n"
                                                 "Try again?",
                                                 qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)
                if retry == qtw.QMessageBox.Yes:
                    self.carrier_name_editline.setFocus()
                else:
                    self.reject()
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.accept()
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.accept()


class NewConsigneeDialog(qtw.QDialog):

    def __init__(self, app_settings, dialog_flag, input_consignee_instance=None, consignee_queries=None):
        super().__init__()
        self.setup_supporting_vars(app_settings, dialog_flag, input_consignee_instance, consignee_queries)
        self.setup_gui()

    def setup_supporting_vars(self, app_settings, dialog_flag, input_consignee_instance, consignee_queries):
        self.app_settings = app_settings
        self.dialog_flag = dialog_flag
        self.input_consignee_instance = input_consignee_instance
        self.consignee_queries = consignee_queries

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        # frames and layouts
        self.main_box = qtw.QVBoxLayout()
        self.title_frame = qtw.QFrame()
        self.data_frame = qtw.QFrame()
        self.spacer_frame = qtw.QFrame()
        self.buttons_frame = qtw.QFrame()
        self.title_frame_box = qtw.QHBoxLayout()
        self.data_frame_box = qtw.QGridLayout()
        self.button_frame_box = qtw.QHBoxLayout()

        # other controls
        #Labels
        self.title_label = qtw.QLabel('Add New Consignee')
        self.consignee_name_label = qtw.QLabel("Consignee Name")
        self.consignee_address_label = qtw.QLabel("Address")
        self.consignee_city_label = qtw.QLabel("City")
        self.consignee_state_label = qtw.QLabel("State")
        self.consignee_country_label = qtw.QLabel("Country")
        self.consignee_postalcode_label = qtw.QLabel("Postal Code")
        self.consignee_phone_label = qtw.QLabel('Phone #')
        self.consignee_fax_label = qtw.QLabel('Fax')
        self.consignee_toll_free_label = qtw.QLabel('Toll Free')
        self.consignee_contact_label = qtw.QLabel('Contact Names')
        #EditLines
        self.consignee_name_editline = qtw.QLineEdit()
        self.consignee_address_editline = qtw.QLineEdit()
        self.consignee_city_editline = qtw.QLineEdit()
        self.consignee_state_editline = qtw.QLineEdit()
        self.consignee_country_editline = qtw.QLineEdit()
        self.consignee_postalcode_editline = qtw.QLineEdit()
        self.consignee_phone_editline = qtw.QLineEdit()
        self.consignee_fax_editline = qtw.QLineEdit()
        self.consignee_toll_free_editline = qtw.QLineEdit()
        self.consignee_contact_editline = qtw.QLineEdit()
        #buttons
        self.cncl_button = qtw.QPushButton('     Cancel     ')
        self.ok_button = qtw.QPushButton('     Create     ')

    def setup_gui_object_style_names(self):
        self.title_label.setObjectName('title')
        self.spacer_frame.setObjectName('spacerFrame')

    def layout_gui_objects(self):
        self.setLayout(self.main_box)

        self.main_box.addWidget(self.title_frame)
        self.main_box.addWidget(self.data_frame, stretch=1)
        self.main_box.addWidget(self.buttons_frame)

        self.title_frame.setLayout(self.title_frame_box)
        self.data_frame.setLayout(self.data_frame_box)
        self.buttons_frame.setLayout(self.button_frame_box)

        self.title_frame_box.addWidget(self.title_label, 1, qtc.Qt.AlignCenter)
        self.data_frame_box.addWidget(self.consignee_name_label, 0, 0, 1, 1)
        self.data_frame_box.addWidget(self.consignee_name_editline, 0, 1, 1, 1)
        self.data_frame_box.addWidget(self.consignee_address_label, 1, 0, 1, 1)
        self.data_frame_box.addWidget(self.consignee_address_editline, 1, 1, 1, 1)
        self.data_frame_box.addWidget(self.consignee_city_label, 2, 0, 1, 1)
        self.data_frame_box.addWidget(self.consignee_city_editline, 2, 1, 1, 1)
        self.data_frame_box.addWidget(self.consignee_state_label, 3, 0, 1, 1)
        self.data_frame_box.addWidget(self.consignee_state_editline, 3, 1, 1, 1)
        self.data_frame_box.addWidget(self.consignee_country_label, 4, 0, 1, 1)
        self.data_frame_box.addWidget(self.consignee_country_editline, 4, 1, 1, 1)
        self.data_frame_box.addWidget(self.consignee_postalcode_label, 5, 0, 1, 1)
        self.data_frame_box.addWidget(self.consignee_postalcode_editline, 5, 1, 1, 1)
        self.data_frame_box.addWidget(self.consignee_phone_label, 6, 0, 1, 1)
        self.data_frame_box.addWidget(self.consignee_phone_editline, 6, 1, 1, 1)
        self.data_frame_box.addWidget(self.consignee_fax_label, 7, 0, 1, 1)
        self.data_frame_box.addWidget(self.consignee_fax_editline, 7, 1, 1, 1)
        self.data_frame_box.addWidget(self.consignee_toll_free_label, 8, 0, 1, 1)
        self.data_frame_box.addWidget(self.consignee_toll_free_editline, 8, 1, 1, 1)
        self.data_frame_box.addWidget(self.consignee_contact_label, 9, 0, 1, 1)
        self.data_frame_box.addWidget(self.consignee_contact_editline, 9, 1, 1, 1)
        self.data_frame_box.addWidget(self.spacer_frame, 10, 0, 1, 2)

        self.button_frame_box.addStretch()
        self.button_frame_box.addWidget(self.cncl_button, alignment=qtc.Qt.AlignRight)
        self.button_frame_box.addWidget(self.ok_button, alignment=qtc.Qt.AlignRight)

    def feature_gui_objects(self):
        self.setup_window_geometry()

        #setting up window depending on flagDialog
        # insert, delete, modify or view
        if self.dialog_flag == LCSettings.Settings.INSERT:
            self.title_label.setText('Add New Consignee')
            self.ok_button.setText('Create')
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.title_label.setText('Delete Consignee')
            self.ok_button.setText('Delete')
            self.load_current_data()
            self.disable_editing()
        elif self.dialog_flag == LCSettings.Settings.MODIFY:
            self.title_label.setText('Modify Consignee')
            self.ok_button.setText('Modify')
            self.load_current_data()
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.title_label.setText('View Consignee')
            self.cncl_button.setVisible(False)
            self.ok_button.setText('Close')
            self.load_current_data()
            self.disable_editing()

    def setup_window_geometry(self):
        window_x_coord = int(self.app_settings.screen_width / 2 - self.app_settings.smallnewwindow_width / 2)
        window_y_coord = int(self.app_settings.screen_height / 2 - self.app_settings.smallnewwindow_height / 2)
        self.setGeometry(window_x_coord, window_y_coord,
                         self.app_settings.newwindow_width, self.app_settings.newwindow_height)
        self.setMinimumSize(self.app_settings.newwindow_width, self.app_settings.newwindow_height)

    def disable_editing(self):
        self.consignee_name_editline.setEnabled(False)
        self.consignee_address_editline.setEnabled(False)
        self.consignee_city_editline.setEnabled(False)
        self.consignee_state_editline.setEnabled(False)
        self.consignee_country_editline.setEnabled(False)
        self.consignee_postalcode_editline.setEnabled(False)
        self.consignee_phone_editline.setEnabled(False)
        self.consignee_fax_editline.setEnabled(False)
        self.consignee_toll_free_editline.setEnabled(False)
        self.consignee_contact_editline.setEnabled(False)

    def load_current_data(self):
        if self.dialog_flag == LCSettings.Settings.INSERT:
            pass
        elif (self.dialog_flag == LCSettings.Settings.DELETE or
              self.dialog_flag == LCSettings.Settings.MODIFY or
              self.dialog_flag == LCSettings.Settings.VIEW):
            self.consignee_name_editline.setText(self.input_consignee_instance.consigneename)
            self.consignee_address_editline.setText(self.input_consignee_instance.consigneeaddress)
            self.consignee_city_editline.setText(self.input_consignee_instance.consigneecity)
            self.consignee_state_editline.setText(self.input_consignee_instance.consigneestate)
            self.consignee_country_editline.setText(self.input_consignee_instance.consigneecountry)
            self.consignee_postalcode_editline.setText(self.input_consignee_instance.consigneepostalcode)
            self.consignee_phone_editline.setText(self.input_consignee_instance.consigneephone)
            self.consignee_fax_editline.setText(self.input_consignee_instance.consigneefax)
            self.consignee_toll_free_editline.setText(self.input_consignee_instance.consigneetollfree)
            self.consignee_contact_editline.setText(self.input_consignee_instance.consigneecontact)

    def setup_gui_object_events(self):
        self.cncl_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.process_user_data)

    def process_user_data(self):
        if self.dialog_flag == LCSettings.Settings.INSERT:
            self.new_consignee_instance = ConsigneeInstance(
                consigneename=self.consignee_name_editline.text(),
                consigneeaddress=self.consignee_address_editline.text(),
                consigneecity=self.consignee_city_editline.text(),
                consigneestate=self.consignee_state_editline.text(),
                consigneecountry=self.consignee_country_editline.text(),
                consigneepostalcode=self.consignee_postalcode_editline.text(),
                consigneephone=self.consignee_phone_editline.text(),
                consigneefax=self.consignee_fax_editline.text(),
                consigneetollfree=self.consignee_toll_free_editline.text(),
                consigneecontact=self.consignee_contact_editline.text()
            )
            operation_returm_code = self.consignee_queries.insert_consignee(self.new_consignee_instance)
            if operation_returm_code == 0:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Success", "New consignee was created",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.accept()
            elif operation_returm_code == 1:
                retry = qtw.QMessageBox.question(self,
                                                 'Fail',
                                                 "Such Consignee already exists.\n"
                                                 "Try again?",
                                                 qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)
                if retry == qtw.QMessageBox.Yes:
                    self.consignee_name_editline.setFocus()
                else:
                    self.reject()
        elif self.dialog_flag == LCSettings.Settings.MODIFY:
            self.modify_consignee_instance = ConsigneeInstance(
                self.input_consignee_instance.consigneeid,
                self.consignee_name_editline.text(),
                self.consignee_address_editline.text(),
                self.consignee_city_editline.text(),
                self.consignee_state_editline.text(),
                self.consignee_country_editline.text(),
                self.consignee_postalcode_editline.text(),
                self.consignee_phone_editline.text(),
                self.consignee_fax_editline.text(),
                self.consignee_toll_free_editline.text(),
                self.consignee_contact_editline.text()
            )
            operation_returm_code = self.consignee_queries.modify_consignee(self.modify_consignee_instance)
            if operation_returm_code == 0:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Success", "Consignee was modified",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.accept()
            elif operation_returm_code == 1:
                retry = qtw.QMessageBox.question(self,
                                                 'Fail',
                                                 "Such consignee already exists.\n"
                                                 "Try again?",
                                                 qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)
                if retry == qtw.QMessageBox.Yes:
                    self.consignee_name_editline.setFocus()
                else:
                    self.reject()
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.accept()
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.accept()


class NewCurrencyDialog(qtw.QDialog):

    def __init__(self, app_settings, dialog_flag, input_currency_instance=None, currency_queries=None):
        super().__init__()
        self.setup_supporting_vars(app_settings, dialog_flag, input_currency_instance, currency_queries)
        self.setup_gui()

    def setup_supporting_vars(self, app_settings, dialog_flag, input_currency_instance, currency_queries):
        self.app_settings = app_settings
        self.dialog_flag = dialog_flag
        self.input_currency_instance = input_currency_instance
        self.currency_queries = currency_queries

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        # frames and layouts
        self.main_box = qtw.QVBoxLayout()
        self.title_frame = qtw.QFrame()
        self.data_frame = qtw.QFrame()
        self.spacer_frame = qtw.QFrame()
        self.buttons_frame = qtw.QFrame()
        self.title_frame_box = qtw.QHBoxLayout()
        self.data_frame_box = qtw.QGridLayout()
        self.button_frame_box = qtw.QHBoxLayout()

        # other controls
        self.title_label = qtw.QLabel('Add New Currency')
        self.currency_short_name_label = qtw.QLabel('Currency Short Name:')
        self.currency_short_name_editline = qtw.QLineEdit()
        self.currency_name_label = qtw.QLabel('Currency Full Name:')
        self.currency_image_label = qtw.QLabel('Currency Icon:')
        self.currency_name_editline = qtw.QLineEdit()
        self.currency_pixmap = None
        self.currency_image = qtw.QLabel()
        self.currency_image.chosen_image_relative_path = None
        self.currency_image_button = qtw.QPushButton('  Choose Image  ')
        self.cncl_button = qtw.QPushButton('     Cancel     ')
        self.ok_button = qtw.QPushButton('     Create     ')

    def setup_gui_object_style_names(self):
        self.title_label.setObjectName('title')
        self.spacer_frame.setObjectName('spacerFrame')

    def layout_gui_objects(self):
        self.setLayout(self.main_box)

        self.main_box.addWidget(self.title_frame)
        self.main_box.addWidget(self.data_frame, stretch=1)
        self.main_box.addWidget(self.buttons_frame)

        self.title_frame.setLayout(self.title_frame_box)
        self.data_frame.setLayout(self.data_frame_box)
        self.buttons_frame.setLayout(self.button_frame_box)

        self.title_frame_box.addWidget(self.title_label, 1, qtc.Qt.AlignCenter)
        self.data_frame_box.addWidget(self.currency_short_name_label, 0, 0, 1, 1)
        self.data_frame_box.addWidget(self.currency_short_name_editline, 0, 1, 1, 1)
        self.data_frame_box.addWidget(self.currency_name_label, 1, 0, 1, 1)
        self.data_frame_box.addWidget(self.currency_name_editline, 1, 1, 1, 1)
        self.data_frame_box.addWidget(self.currency_image_label, 2, 0, 1, 1)
        self.data_frame_box.addWidget(self.currency_image, 2, 1, 1, 1)
        self.data_frame_box.addWidget(self.spacer_frame, 3, 0, 1, 2)

        self.button_frame_box.addWidget(self.currency_image_button, alignment=qtc.Qt.AlignLeft)
        self.button_frame_box.addStretch()
        self.button_frame_box.addWidget(self.cncl_button, alignment=qtc.Qt.AlignRight)
        self.button_frame_box.addWidget(self.ok_button, alignment=qtc.Qt.AlignRight)

    def feature_gui_objects(self):
        self.setup_window_geometry()

        #setting up window depending on flagDialog
        # insert, delete, modify or view
        if self.dialog_flag == LCSettings.Settings.INSERT:
            self.title_label.setText('Add New Currency')
            self.ok_button.setText('Create')
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.title_label.setText('Delete Currency')
            self.ok_button.setText('Delete')
            self.currency_image_button.setVisible(False)
            self.load_current_data()
            self.disable_editing()
        elif self.dialog_flag == LCSettings.Settings.MODIFY:
            self.title_label.setText('Modify Currency')
            self.ok_button.setText('Modify')
            self.load_current_data()
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.title_label.setText('View Currency')
            self.cncl_button.setVisible(False)
            self.currency_image_button.setVisible(False)
            self.ok_button.setText('Close')
            self.load_current_data()
            self.disable_editing()

    def setup_window_geometry(self):
        window_x_coord = int(self.app_settings.screen_width / 2 - self.app_settings.smallnewwindow_width / 2)
        window_y_coord = int(self.app_settings.screen_height / 2 - self.app_settings.smallnewwindow_height / 2)
        self.setGeometry(window_x_coord, window_y_coord,
                         self.app_settings.smallnewwindow_width, self.app_settings.smallnewwindow_height)
        self.setMinimumSize(self.app_settings.smallnewwindow_width, self.app_settings.smallnewwindow_height)

    def disable_editing(self):
        self.currency_short_name_editline.setEnabled(False)
        self.currency_name_editline.setEnabled(False)

    def load_current_data(self):
        self.currency_short_name_editline.setText(self.input_currency_instance.currencyshortname)
        self.currency_name_editline.setText(self.input_currency_instance.currencyname)
        self.load_image_data()

    def load_image_data(self):
        image_path = os.path.join(
            self.app_settings.application_folderpath,
            self.input_currency_instance.currencyimagepath
            )
        self.display_chosen_image(image_path)

    def display_chosen_image(self, image_path):
        try:
            self.currency_pixmap = qtg.QPixmap(image_path)
            if self.currency_pixmap.width() != 60 or self.currency_pixmap.height() != 28:
                raise ImageDimensionError(self.currency_queries)
            else:
                self.currency_image.setPixmap(self.currency_pixmap)
                self.currency_image.chosen_image_relative_path = \
                    os.path.join(
                        self.app_settings.images_relativepath,
                        os.path.basename(image_path)
                    )
                self.currency_image.resize(self.currency_pixmap.width(), self.currency_pixmap.height())
        except ImageDimensionError:
            qtw.QMessageBox(
                qtw.QMessageBox.Critical,
                "Fail", "You must adjust selected image's  dimension: W-60 X H-28.",
                qtw.QMessageBox.Yes
            ).exec_()
        except Exception:
            qtw.QMessageBox(
                qtw.QMessageBox.Critical,
                "Fail", "Error loading image",
                qtw.QMessageBox.Yes
            ).exec_()


    def setup_gui_object_events(self):
        self.currency_image_button.clicked.connect(self.choose_currency_image_path)
        self.cncl_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.process_user_data)

    def process_user_data(self):
        if self.dialog_flag == LCSettings.Settings.INSERT:
            try :
                if self.currency_image.chosen_image_relative_path is None:
                    raise MissingChosenImageError(self.currency_queries)
                self.new_currency_instance = CurrencyInstance(
                    currencyshortname=self.currency_short_name_editline.text(),
                    currencyname=self.currency_name_editline.text(),
                    currencyimagepath=self.currency_image.chosen_image_relative_path
                )
                operation_returm_code = self.currency_queries.insert_currency(self.new_currency_instance)
                if operation_returm_code == 0:
                    qtw.QMessageBox(
                        qtw.QMessageBox.Information,
                        "Success", "New currency was created",
                        qtw.QMessageBox.Yes
                    ).exec_()
                    self.accept()
                elif operation_returm_code == 1:
                    retry = qtw.QMessageBox.question(self,
                                                     'Fail',
                                                     "Such currency already exist.\n"
                                                     "Try again?",
                                                     qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)
                    if retry == qtw.QMessageBox.Yes:
                        self.currency_short_name_editline.setFocus()
                    else:
                        self.reject()
            except MissingChosenImageError:
                print('Do some logging ')

        elif self.dialog_flag == LCSettings.Settings.MODIFY:
            self.modify_currency_instance = CurrencyInstance(
                self.input_currency_instance.currencyid,
                self.currency_short_name_editline.text(),
                self.currency_name_editline.text(),
                self.currency_image.chosen_image_relative_path
            )
            operation_returm_code = self.currency_queries.modify_currency(self.modify_currency_instance)
            if operation_returm_code == 0:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Success", "Currency was modified",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.accept()
            elif operation_returm_code == 1:
                retry = qtw.QMessageBox.question(self,
                                                 'Fail',
                                                 "Such currency already exists.\n"
                                                 "Try again?",
                                                 qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)
                if retry == qtw.QMessageBox.Yes:
                    self.currency_short_name_editline.setFocus()
                else:
                    self.reject()
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.accept()
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.accept()

    def choose_currency_image_path(self):
        image_path, _ = qtw.QFileDialog.getOpenFileName(self,
                                                     'Pick image file for currency',
                                                     self.app_settings.application_folderpath,
                                                     "Image files (*.jpg)",
                                                     "(*.jpg)"
                                                     )
        # if image was chosen, extract relative path from the full path
        if image_path:
            designated_folder = os.path.join(
                self.app_settings.application_folderpath,
                self.app_settings.images_relativepath
                )
            if designated_folder != os.path.dirname(image_path):
                ## if selected file is not located in designated location
                ## then copy it there....
                shutil.copy2(image_path, designated_folder)
            self.currency_image.chosen_image_relative_path = \
                os.path.join(
                    self.app_settings.images_relativepath,
                    os.path.basename(image_path)
                )
            self.display_chosen_image(os.path.join(
                designated_folder,
                os.path.basename(image_path)
            ))


class NewLoadTypeDialog(qtw.QDialog):

    def __init__(self, app_settings, dialog_flag, input_loadtype_instance=None, loadtype_queries=None):
        super().__init__()
        self.setup_supporting_vars(app_settings, dialog_flag, input_loadtype_instance, loadtype_queries)
        self.setup_gui()

    def setup_supporting_vars(self, app_settings, dialog_flag, input_loadtype_instance, loadtype_queries):
        self.app_settings = app_settings
        self.dialog_flag = dialog_flag
        self.input_loadtype_instance = input_loadtype_instance
        self.loadtype_queries= loadtype_queries

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        # frames and layouts
        self.main_box = qtw.QVBoxLayout()
        self.title_frame = qtw.QFrame()
        self.data_frame = qtw.QFrame()
        self.spacer_frame = qtw.QFrame()
        self.buttons_frame = qtw.QFrame()
        self.title_frame_box = qtw.QHBoxLayout()
        self.data_frame_box = qtw.QGridLayout()
        self.button_frame_box = qtw.QHBoxLayout()

        # other controls
        self.title_label = qtw.QLabel('Add New Type Of Load(Measure)')
        self.loadtype_label = qtw.QLabel('Type of Load(Measure):')
        self.loadtype_name_editline = qtw.QLineEdit()
        self.cncl_button = qtw.QPushButton('Cancel')
        self.ok_button = qtw.QPushButton('Create')

    def setup_gui_object_style_names(self):
        self.title_label.setObjectName('title')
        self.spacer_frame.setObjectName('spacerFrame')

    def layout_gui_objects(self):
        self.setLayout(self.main_box)

        self.main_box.addWidget(self.title_frame)
        self.main_box.addWidget(self.data_frame, stretch=1)
        self.main_box.addWidget(self.buttons_frame)

        self.title_frame.setLayout(self.title_frame_box)
        self.data_frame.setLayout(self.data_frame_box)
        self.buttons_frame.setLayout(self.button_frame_box)

        self.title_frame_box.addWidget(self.title_label, 1, qtc.Qt.AlignCenter)
        self.data_frame_box.addWidget(self.loadtype_label, 0, 0, 1, 1)
        self.data_frame_box.addWidget(self.loadtype_name_editline, 0, 1, 1, 1)
        self.data_frame_box.addWidget(self.spacer_frame, 2, 0, 1, 2)

        self.button_frame_box.addStretch()
        self.button_frame_box.addWidget(self.cncl_button, alignment=qtc.Qt.AlignRight)
        self.button_frame_box.addWidget(self.ok_button, alignment=qtc.Qt.AlignRight)

    def feature_gui_objects(self):
        self.setup_window_geometry()

        #setting up window depending on flagDialog
        # insert, delete, modify or view
        if self.dialog_flag == LCSettings.Settings.INSERT:
            self.title_label.setText('Add New Load Type')
            self.ok_button.setText('Create')
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.title_label.setText('Delete Load Type')
            self.ok_button.setText('Delete')
            self.load_current_data()
            self.disable_editing()
        elif self.dialog_flag == LCSettings.Settings.MODIFY:
            self.title_label.setText('Modify Load Type')
            self.ok_button.setText('Modify')
            self.load_current_data()
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.title_label.setText('View Load Type')
            self.cncl_button.setVisible(False)
            self.ok_button.setText('Close')
            self.load_current_data()
            self.disable_editing()

    def setup_window_geometry(self):
        window_x_coord = int(self.app_settings.screen_width / 2 - self.app_settings.smallnewwindow_width / 2)
        window_y_coord = int(self.app_settings.screen_height / 2 - self.app_settings.smallnewwindow_height / 2)
        self.setGeometry(window_x_coord, window_y_coord,
                         self.app_settings.smallnewwindow_width, self.app_settings.smallnewwindow_height)
        self.setMinimumSize(self.app_settings.smallnewwindow_width, self.app_settings.smallnewwindow_height)

    def disable_editing(self):
        self.loadtype_name_editline.setEnabled(False)

    def load_current_data(self):
        if self.dialog_flag == LCSettings.Settings.INSERT:
            pass
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.loadtype_name_editline.setText(self.input_loadtype_instance.loadtypename)
        elif self.dialog_flag == LCSettings.Settings.MODIFY:
            self.loadtype_name_editline.setText(self.input_loadtype_instance.loadtypename)
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.loadtype_name_editline.setText(self.input_loadtype_instance.loadtypename)

    def setup_gui_object_events(self):
        self.cncl_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.process_user_data)

    def process_user_data(self):
        if self.dialog_flag == LCSettings.Settings.INSERT:
            self.new_loadtype_instance = LoadTypeInstance(
                loadtypename=self.loadtype_name_editline.text()
            )
            operation_returm_code = self.loadtype_queries.insert_loadtype(self.new_loadtype_instance)
            if operation_returm_code == 0:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Success", "New type was created",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.accept()
            elif operation_returm_code == 1:
                retry = qtw.QMessageBox.question(self,
                                                 'Fail',
                                                 "Such Type already exist.\n"
                                                 "Try again?",
                                                 qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)
                if retry == qtw.QMessageBox.Yes:
                    self.loadtype_name_editline.setFocus()
                else:
                    self.reject()
        elif self.dialog_flag == LCSettings.Settings.MODIFY:
            self.modify_loadtype_instance = LoadTypeInstance(
                self.input_loadtype_instance.loadtypeid,
                self.loadtype_name_editline.text()
            )
            operation_returm_code = self.loadtype_queries.modify_loadtype(self.modify_loadtype_instance)
            if operation_returm_code == 0:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Success", "Type was modified",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.accept()
            elif operation_returm_code == 1:
                retry = qtw.QMessageBox.question(self,
                                                 'Fail',
                                                 "Such type already exists.\n"
                                                 "Try again?",
                                                 qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)
                if retry == qtw.QMessageBox.Yes:
                    self.loadtype_name_editline.setFocus()
                else:
                    self.reject()
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.accept()
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.accept()


class NewPasswordDialog(qtw.QDialog):

    def __init__(self, app_settings, forcepassword_flag=False, new_user_instance=None, users_queries=None):
        super().__init__()
        self.setup_supporting_vars(app_settings, forcepassword_flag, new_user_instance, users_queries)
        self.setup_gui()

    def setup_supporting_vars(self, app_settings, forcepasswordFlag, new_user_instance, usersWorker):
        self.app_settings = app_settings
        self.forcepassword_flag = forcepasswordFlag
        self.new_user_instance = new_user_instance
        self.users_queries = usersWorker

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.main_box = qtw.QVBoxLayout()
        self.title_frame = qtw.QFrame()
        self.data_frame = qtw.QFrame()
        self.spacer_frame = qtw.QFrame()
        self.buttons_frame = qtw.QFrame()
        self.title_frame_box = qtw.QHBoxLayout()
        self.data_frame_box = qtw.QGridLayout()
        self.button_frame_box = qtw.QHBoxLayout()

        # Depending on flagDialog titleLabel might be also modifying or viewing.
        self.title_label = qtw.QLabel('Change Password')
        self.oldpassword_label = qtw.QLabel('Old Password')
        self.newpassword_label = qtw.QLabel('New Password')
        self.reenterpassword_label = qtw.QLabel('Re-enter Password')
        self.oldpassword_editline = qtw.QLineEdit()
        self.newpassword_editline = qtw.QLineEdit()
        self.reenterpassword_editline = qtw.QLineEdit()
        self.cncl_button = qtw.QPushButton('   Cancel   ')
        self.ok_button = qtw.QPushButton('   Change   ')


    def setup_gui_object_style_names(self):
        self.title_label.setObjectName('title')
        self.spacer_frame.setObjectName('spacerFrame')

    def layout_gui_objects(self):
        self.setLayout(self.main_box)

        self.main_box.addWidget(self.title_frame)
        self.main_box.addWidget(self.data_frame, stretch=1)
        self.main_box.addWidget(self.buttons_frame)

        self.title_frame.setLayout(self.title_frame_box)
        self.data_frame.setLayout(self.data_frame_box)
        self.buttons_frame.setLayout(self.button_frame_box)

        self.title_frame_box.addWidget(self.title_label, 1, qtc.Qt.AlignCenter)
        self.data_frame_box.addWidget(self.oldpassword_label, 0, 0, 1, 1)
        self.data_frame_box.addWidget(self.oldpassword_editline, 0, 1, 1, 1)
        self.data_frame_box.addWidget(self.newpassword_label, 1, 0, 1, 1)
        self.data_frame_box.addWidget(self.newpassword_editline, 1, 1, 1, 1)
        self.data_frame_box.addWidget(self.reenterpassword_label, 2, 0, 1, 1)
        self.data_frame_box.addWidget(self.reenterpassword_editline, 2, 1, 1, 1)
        self.data_frame_box.addWidget(self.spacer_frame, 4, 0, 1, 2)

        self.button_frame_box.addStretch()
        self.button_frame_box.addWidget(self.cncl_button, alignment=qtc.Qt.AlignRight)
        self.button_frame_box.addWidget(self.ok_button, alignment=qtc.Qt.AlignRight)

    def feature_gui_objects(self):
        self.setup_window_geometry()
        self.oldpassword_editline.setEchoMode(qtw.QLineEdit.Password)
        self.newpassword_editline.setEchoMode(qtw.QLineEdit.Password)
        self.reenterpassword_editline.setEchoMode(qtw.QLineEdit.Password)
        #setting up window depending on flagDialog
        # insert, delete, modify or view
        if self.forcepassword_flag == True:
            self.title_label.setText('New User Password')
            self.oldpassword_label.setVisible(False)
            self.oldpassword_editline.setVisible(False)
        elif self.forcepassword_flag == False:
            self.title_label.setText('Change My Password')

    def setup_window_geometry(self):
        window_x_coord = int(self.app_settings.screen_width / 2 - self.app_settings.smallnewwindow_width / 2)
        window_y_coord = int(self.app_settings.screen_height / 2 - self.app_settings.smallnewwindow_height / 2)
        self.setGeometry(window_x_coord, window_y_coord,
                         self.app_settings.smallnewwindow_width, self.app_settings.smallnewwindow_height)
        self.setMinimumSize(self.app_settings.smallnewwindow_width, self.app_settings.smallnewwindow_height)

    def setup_gui_object_events(self):
        self.cncl_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.process_user_data)

    def process_user_data(self):
        if self.forcepassword_flag == True:
            if self.newpassword_editline.text() == self.reenterpassword_editline.text():
                operation_returm_code = self.users_queries.modify_user_password_byid(
                    self.new_user_instance,
                    self.newpassword_editline.text()
                )
                if operation_returm_code == 0:
                    qtw.QMessageBox(
                        qtw.QMessageBox.Information,
                        "Success", "New password was set",
                        qtw.QMessageBox.Yes
                    ).exec_()
                    self.accept()
                elif operation_returm_code == 1:
                    qtw.QMessageBox.critical(
                        self,
                        'Fail',
                        'Error changing password. \n'
                        'User record was corrupted.',
                        qtw.QMessageBox.Yes
                    ).exec_()
                    self.reject()
            else:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Fail", "Re-typed password is not matching.",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.newpassword_editline.setText('')
                self.reenterpassword_editline.setText('')
                self.newpassword_editline.setFocus()
        elif self.forcepassword_flag == False:
            if self.newpassword_editline.text() == self.reenterpassword_editline.text():
                operation_returm_code = self.users_queries.modify_login_user_password(
                    self.oldpassword_editline.text(),
                    self.reenterpassword_editline.text()
                )
                if operation_returm_code == 0:
                    qtw.QMessageBox(
                        qtw.QMessageBox.Information,
                        "Success", "New password was set",
                        qtw.QMessageBox.Yes
                    ).exec_()
                    self.accept()
                elif operation_returm_code == 1:
                    retry = qtw.QMessageBox.question(
                        self,
                        'Fail',
                        "Either old password does not match,\n"
                        "Or user record was corrupted.\n"
                        "Try again?",
                        qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes
                    )
                    if retry == qtw.QMessageBox.Yes:
                        self.oldpassword_editline.setText('')
                        self.newpassword_editline.setText('')
                        self.reenterpassword_editline.setText('')
                        self.oldpassword_editline.setFocus()
                    else:
                        self.reject()
            else:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Fail", "Re-typed password is not matching.",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.oldpassword_editline.setText('')
                self.newpassword_editline.setText('')
                self.reenterpassword_editline.setText('')


class NewShipperDialog(qtw.QDialog):

    def __init__(self, app_settings, dialog_flag, input_shipper_instance=None, shipper_queries=None):
        super().__init__()
        self.setup_supporting_vars(app_settings, dialog_flag, input_shipper_instance, shipper_queries)
        self.setup_gui()

    def setup_supporting_vars(self, app_settings, dialog_flag, input_shipper_instance, shipper_queries):
        self.app_settings = app_settings
        self.dialog_flag = dialog_flag
        self.input_shipper_instance = input_shipper_instance
        self.shipper_queries = shipper_queries

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        # frames and layouts
        self.main_box = qtw.QVBoxLayout()
        self.title_frame = qtw.QFrame()
        self.data_frame = qtw.QFrame()
        self.spacer_frame = qtw.QFrame()
        self.buttons_frame = qtw.QFrame()
        self.title_frame_box = qtw.QHBoxLayout()
        self.data_frame_box = qtw.QGridLayout()
        self.button_frame_box = qtw.QHBoxLayout()

        # other controls
        #Labels
        self.title_label = qtw.QLabel('Add New Shipper')
        self.shipper_name_label = qtw.QLabel("Shipper Name")
        self.shipper_address_label = qtw.QLabel("Address")
        self.shipper_city_label = qtw.QLabel("City")
        self.shipper_state_label = qtw.QLabel("State")
        self.shipper_country_label = qtw.QLabel("Country")
        self.shipper_postalcode_label = qtw.QLabel("Postal Code")
        self.shipper_phone_label = qtw.QLabel('Phone #')
        self.shipper_fax_label = qtw.QLabel('Fax')
        self.shipper_toll_free_label = qtw.QLabel('Toll Free')
        self.shipper_contact_label = qtw.QLabel('Contact Names')
        #EditLines
        self.shipper_name_edit_line = qtw.QLineEdit()
        self.shipper_address_edit_line = qtw.QLineEdit()
        self.shipper_city_editline = qtw.QLineEdit()
        self.shipper_state_editline = qtw.QLineEdit()
        self.shipper_country_editline = qtw.QLineEdit()
        self.shipper_postalcode_editline = qtw.QLineEdit()
        self.shipper_phone_editline = qtw.QLineEdit()
        self.shipper_fax_editline = qtw.QLineEdit()
        self.shipper_toll_free_editline = qtw.QLineEdit()
        self.shipper_contact_editline = qtw.QLineEdit()
        #buttons
        self.cncl_button = qtw.QPushButton('Cancel')
        self.ok_button = qtw.QPushButton('Create')

    def setup_gui_object_style_names(self):
        self.title_label.setObjectName('title')
        self.spacer_frame.setObjectName('spacerFrame')

    def layout_gui_objects(self):
        self.setLayout(self.main_box)

        self.main_box.addWidget(self.title_frame)
        self.main_box.addWidget(self.data_frame, stretch=1)
        self.main_box.addWidget(self.buttons_frame)

        self.title_frame.setLayout(self.title_frame_box)
        self.data_frame.setLayout(self.data_frame_box)
        self.buttons_frame.setLayout(self.button_frame_box)

        self.title_frame_box.addWidget(self.title_label, 1, qtc.Qt.AlignCenter)
        self.data_frame_box.addWidget(self.shipper_name_label, 0, 0, 1, 1)
        self.data_frame_box.addWidget(self.shipper_name_edit_line, 0, 1, 1, 1)
        self.data_frame_box.addWidget(self.shipper_address_label, 1, 0, 1, 1)
        self.data_frame_box.addWidget(self.shipper_address_edit_line, 1, 1, 1, 1)
        self.data_frame_box.addWidget(self.shipper_city_label, 2, 0, 1, 1)
        self.data_frame_box.addWidget(self.shipper_city_editline, 2, 1, 1, 1)
        self.data_frame_box.addWidget(self.shipper_state_label, 3, 0, 1, 1)
        self.data_frame_box.addWidget(self.shipper_state_editline, 3, 1, 1, 1)
        self.data_frame_box.addWidget(self.shipper_country_label, 4, 0, 1, 1)
        self.data_frame_box.addWidget(self.shipper_country_editline, 4, 1, 1, 1)
        self.data_frame_box.addWidget(self.shipper_postalcode_label, 5, 0, 1, 1)
        self.data_frame_box.addWidget(self.shipper_postalcode_editline, 5, 1, 1, 1)
        self.data_frame_box.addWidget(self.shipper_phone_label, 6, 0, 1, 1)
        self.data_frame_box.addWidget(self.shipper_phone_editline, 6, 1, 1, 1)
        self.data_frame_box.addWidget(self.shipper_fax_label, 7, 0, 1, 1)
        self.data_frame_box.addWidget(self.shipper_fax_editline, 7, 1, 1, 1)
        self.data_frame_box.addWidget(self.shipper_toll_free_label, 8, 0, 1, 1)
        self.data_frame_box.addWidget(self.shipper_toll_free_editline, 8, 1, 1, 1)
        self.data_frame_box.addWidget(self.shipper_contact_label, 9, 0, 1, 1)
        self.data_frame_box.addWidget(self.shipper_contact_editline, 9, 1, 1, 1)
        self.data_frame_box.addWidget(self.spacer_frame, 10, 0, 1, 2)

        self.button_frame_box.addStretch()
        self.button_frame_box.addWidget(self.cncl_button, alignment=qtc.Qt.AlignRight)
        self.button_frame_box.addWidget(self.ok_button, alignment=qtc.Qt.AlignRight)

    def feature_gui_objects(self):
        self.setup_window_geometry()

        #setting up window depending on flagDialog
        # insert, delete, modify or view
        if self.dialog_flag == LCSettings.Settings.INSERT:
            self.title_label.setText('Add New Shipper')
            self.ok_button.setText('Create')
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.title_label.setText('Delete Shipper')
            self.ok_button.setText('Delete')
            self.load_current_data()
            self.disable_editing()
        elif self.dialog_flag == LCSettings.Settings.MODIFY:
            self.title_label.setText('Modify Shipper')
            self.ok_button.setText('Modify')
            self.load_current_data()
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.title_label.setText('View Shipper')
            self.cncl_button.setVisible(False)
            self.ok_button.setText('Close')
            self.load_current_data()
            self.disable_editing()

    def setup_window_geometry(self):
        window_x_coord = int(self.app_settings.screen_width / 2 - self.app_settings.smallnewwindow_width / 2)
        window_y_coord = int(self.app_settings.screen_height / 2 - self.app_settings.smallnewwindow_height / 2)
        self.setGeometry(window_x_coord, window_y_coord,
                         self.app_settings.newwindow_width, self.app_settings.newwindow_height)
        self.setMinimumSize(self.app_settings.newwindow_width, self.app_settings.newwindow_height)

    def disable_editing(self):
        self.shipper_name_edit_line.setEnabled(False)
        self.shipper_address_edit_line.setEnabled(False)
        self.shipper_city_editline.setEnabled(False)
        self.shipper_state_editline.setEnabled(False)
        self.shipper_country_editline.setEnabled(False)
        self.shipper_postalcode_editline.setEnabled(False)
        self.shipper_phone_editline.setEnabled(False)
        self.shipper_fax_editline.setEnabled(False)
        self.shipper_toll_free_editline.setEnabled(False)
        self.shipper_contact_editline.setEnabled(False)

    def load_current_data(self):
        if self.dialog_flag == LCSettings.Settings.INSERT:
            pass
        elif (self.dialog_flag == LCSettings.Settings.DELETE or
              self.dialog_flag == LCSettings.Settings.MODIFY or
              self.dialog_flag == LCSettings.Settings.VIEW):
            self.shipper_name_edit_line.setText(self.input_shipper_instance.shippername)
            self.shipper_address_edit_line.setText(self.input_shipper_instance.shipperaddress)
            self.shipper_city_editline.setText(self.input_shipper_instance.shippercity)
            self.shipper_state_editline.setText(self.input_shipper_instance.shipperstate)
            self.shipper_country_editline.setText(self.input_shipper_instance.shippercountry)
            self.shipper_postalcode_editline.setText(self.input_shipper_instance.shipperpostalcode)
            self.shipper_phone_editline.setText(self.input_shipper_instance.shipperphone)
            self.shipper_fax_editline.setText(self.input_shipper_instance.shipperfax)
            self.shipper_toll_free_editline.setText(self.input_shipper_instance.shippertollfree)
            self.shipper_contact_editline.setText(self.input_shipper_instance.shippercontact)

    def setup_gui_object_events(self):
        self.cncl_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.process_user_data)

    def process_user_data(self):
        if self.dialog_flag == LCSettings.Settings.INSERT:
            self.new_shipper_instance = ShipperInstance(
                shippername=self.shipper_name_edit_line.text(),
                shipperaddress=self.shipper_address_edit_line.text(),
                shippercity=self.shipper_city_editline.text(),
                shipperstate=self.shipper_state_editline.text(),
                shippercountry=self.shipper_country_editline.text(),
                shipperpostalcode=self.shipper_postalcode_editline.text(),
                shipperphone=self.shipper_phone_editline.text(),
                shipperfax=self.shipper_fax_editline.text(),
                shippertollfree=self.shipper_toll_free_editline.text(),
                shippercontact=self.shipper_contact_editline.text()
            )
            operation_returm_code = self.shipper_queries.insert_shipper(self.new_shipper_instance)
            if operation_returm_code == 0:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Success", "New shipper was created",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.accept()
            elif operation_returm_code == 1:
                retry = qtw.QMessageBox.question(self,
                                                 'Fail',
                                                 "Such Shipper already exists.\n"
                                                 "Try again?",
                                                 qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)
                if retry == qtw.QMessageBox.Yes:
                    self.shipper_name_edit_line.setFocus()
                else:
                    self.reject()
        elif self.dialog_flag == LCSettings.Settings.MODIFY:
            self.modify_shipper_instance = ShipperInstance(
                self.input_shipper_instance.shipperid,
                self.shipper_name_edit_line.text(),
                self.shipper_address_edit_line.text(),
                self.shipper_city_editline.text(),
                self.shipper_state_editline.text(),
                self.shipper_country_editline.text(),
                self.shipper_postalcode_editline.text(),
                self.shipper_phone_editline.text(),
                self.shipper_fax_editline.text(),
                self.shipper_toll_free_editline.text(),
                self.shipper_contact_editline.text()
            )
            operation_returm_code = self.shipper_queries.modify_shipper(self.modify_shipper_instance)
            if operation_returm_code == 0:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Success", "Shipper was modified",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.accept()
            elif operation_returm_code == 1:
                retry = qtw.QMessageBox.question(self,
                                                 'Fail',
                                                 "Such shipper already exists.\n"
                                                 "Try again?",
                                                 qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)
                if retry == qtw.QMessageBox.Yes:
                    self.shipper_name_edit_line.setFocus()
                else:
                    self.reject()
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.accept()
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.accept()


class NewUserDialog(qtw.QDialog):

    def __init__(self, app_settings, dialog_flag, input_user_instance=None, users_queries=None):
        super().__init__()
        self.setup_supporting_vars(app_settings, dialog_flag,  input_user_instance, users_queries)
        self.setup_gui()

    def setup_supporting_vars(self, app_settings, dialog_flag, input_user_instance, users_queries):
        self.app_settings = app_settings
        self.dialog_flag = dialog_flag
        self.input_user_instance = input_user_instance
        self.users_queries = users_queries

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.main_box = qtw.QVBoxLayout()
        self.title_frame = qtw.QFrame()
        self.data_frame = qtw.QFrame()
        self.spacer_frame = qtw.QFrame()
        self.buttons_frame = qtw.QFrame()
        self.title_frame_box = qtw.QHBoxLayout()
        self.data_frame_box = qtw.QGridLayout()
        self.button_frame_box = qtw.QHBoxLayout()

        # Depending on flagDialog titleLabel might be also modifying or viewing.
        self.title_label = qtw.QLabel('Add New User')
        self.fname_label = qtw.QLabel('First Name')
        self.sname_label = qtw.QLabel('Last Name')
        self.password_label = qtw.QLabel('Password')
        self.newpassword_label = qtw.QLabel('Re-enter Password')
        self.fname_edit_line = qtw.QLineEdit()
        self.sname_editline = qtw.QLineEdit()
        self.password_editline = qtw.QLineEdit()
        self.newpassword_editline = qtw.QLineEdit()
        self.cncl_button = qtw.QPushButton('Cancel')
        self.ok_button = qtw.QPushButton('Create')


    def setup_gui_object_style_names(self):
        self.title_label.setObjectName('title')
        self.spacer_frame.setObjectName('spacerFrame')

    def layout_gui_objects(self):
        self.setLayout(self.main_box)

        self.main_box.addWidget(self.title_frame)
        self.main_box.addWidget(self.data_frame, stretch=1)
        self.main_box.addWidget(self.buttons_frame)

        self.title_frame.setLayout(self.title_frame_box)
        self.data_frame.setLayout(self.data_frame_box)
        self.buttons_frame.setLayout(self.button_frame_box)

        self.title_frame_box.addWidget(self.title_label, 1, qtc.Qt.AlignCenter)
        self.data_frame_box.addWidget(self.fname_label, 0, 0, 1, 1)
        self.data_frame_box.addWidget(self.fname_edit_line, 0, 1, 1, 1)
        self.data_frame_box.addWidget(self.sname_label, 1, 0, 1, 1)
        self.data_frame_box.addWidget(self.sname_editline, 1, 1, 1, 1)
        self.data_frame_box.addWidget(self.password_label, 2, 0, 1, 1)
        self.data_frame_box.addWidget(self.password_editline, 2, 1, 1, 1)
        self.data_frame_box.addWidget(self.newpassword_label, 3, 0, 1, 1)
        self.data_frame_box.addWidget(self.newpassword_editline, 3, 1, 1, 1)
        self.data_frame_box.addWidget(self.spacer_frame, 4, 0, 1, 2)

        self.button_frame_box.addStretch()
        self.button_frame_box.addWidget(self.cncl_button, alignment=qtc.Qt.AlignRight)
        self.button_frame_box.addWidget(self.ok_button, alignment=qtc.Qt.AlignRight)

    def feature_gui_objects(self):
        self.setup_window_geometry()
        self.password_editline.setEchoMode(qtw.QLineEdit.Password)
        self.newpassword_editline.setEchoMode(qtw.QLineEdit.Password)
        #setting up window depending on flagDialog
        # insert, delete, modify or view
        if self.dialog_flag == LCSettings.Settings.INSERT:
            self.title_label.setText('Add New User')
            self.ok_button.setText('Create')
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.title_label.setText('Delete User')
            self.ok_button.setText('Delete')
            self.remove_password_editline()
            self.load_current_data()
            self.disable_editing()
        elif self.dialog_flag == LCSettings.Settings.MODIFY:
            self.title_label.setText('Modify User')
            self.ok_button.setText('Modify')
            self.remove_password_editline()
            self.load_current_data()
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.title_label.setText('View User')
            self.cncl_button.setVisible(False)
            self.ok_button.setText('Close')
            self.remove_password_editline()
            self.load_current_data()
            self.disable_editing()

    def setup_window_geometry(self):
        window_x_coord = int(self.app_settings.screen_width / 2 - self.app_settings.smallnewwindow_width / 2)
        window_y_coord = int(self.app_settings.screen_height / 2 - self.app_settings.smallnewwindow_height / 2)
        self.setGeometry(window_x_coord, window_y_coord,
                         self.app_settings.smallnewwindow_width, self.app_settings.smallnewwindow_height)
        self.setMinimumSize(self.app_settings.smallnewwindow_width, self.app_settings.smallnewwindow_height)

    def disable_editing(self):
        self.fname_edit_line.setEnabled(False)
        self.sname_editline.setEnabled(False)

    def load_current_data(self):
        if self.dialog_flag == LCSettings.Settings.INSERT:
            pass
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.fname_edit_line.setText(self.input_user_instance.userfname)
            self.sname_editline.setText(self.input_user_instance.usersname)
        elif self.dialog_flag == LCSettings.Settings.MODIFY:
            self.fname_edit_line.setText(self.input_user_instance.userfname)
            self.sname_editline.setText(self.input_user_instance.usersname)
            self.password_editline.setText(self.input_user_instance.password)
            self.newpassword_editline.setText(self.input_user_instance.password)
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.fname_edit_line.setText(self.input_user_instance.userfname)
            self.sname_editline.setText(self.input_user_instance.usersname)

    def remove_password_editline(self):
        self.password_label.setVisible(False)
        self.password_editline.setVisible(False)
        self.newpassword_label.setVisible(False)
        self.newpassword_editline.setVisible(False)

    def setup_gui_object_events(self):
        self.cncl_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.process_user_data)

    def process_user_data(self):
        if self.dialog_flag == LCSettings.Settings.INSERT:
            if self.newpassword_editline.text() == self.password_editline.text():
                self.new_user_instance = UserInstance(
                    userfname=self.fname_edit_line.text(),
                    usersname=self.sname_editline.text(),
                    password=self.password_editline.text()
                )
                operation_returm_code = self.users_queries.insert_user(self.new_user_instance)
                if operation_returm_code == 0:
                    qtw.QMessageBox(
                        qtw.QMessageBox.Information,
                        "Success", "New user was created",
                        qtw.QMessageBox.Yes
                    ).exec_()
                    self.accept()
                elif operation_returm_code == 1:
                    retry = qtw.QMessageBox.question(self,
                                                     'Fail',
                                                     "Such user already exists.\n"
                                                     "Try again?",
                                                     qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)
                    if retry == qtw.QMessageBox.Yes:
                        self.fname_edit_line.setFocus()
                    else:
                        self.reject()
            else:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Fail", "Re-typed password is not matching.",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.password_editline.setText('')
                self.newpassword_editline.setText('')
        elif self.dialog_flag == LCSettings.Settings.MODIFY:
            self.modify_user_instance = UserInstance(
                userid=self.input_user_instance.userid,
                userfname=self.fname_edit_line.text(),
                usersname=self.sname_editline.text(),
                password=self.input_user_instance.password
            )
            operation_returm_code = self.users_queries.modify_user(self.modify_user_instance)
            if operation_returm_code == 0:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Success", "User was modified",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.accept()
            elif operation_returm_code == 1:
                retry = qtw.QMessageBox.question(self,
                                                 'Fail',
                                                 "Either you are trying to modify Administrator acount,\n"
                                                 "Try again?",
                                                 qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)
                if retry == qtw.QMessageBox.Yes:
                    self.fname_edit_line.setFocus()
                else:
                    self.reject()
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.accept()
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.accept()


class NewLoadConfirmationDialog(qtw.QDialog):

    def __init__(self, app_settings, dialog_flag, input_loadconfirmation_instance=None, loadconfirmation_queries=None):
        super().__init__()
        self.setup_supporting_vars(
            app_settings,
            dialog_flag,
            input_loadconfirmation_instance,
            loadconfirmation_queries
            )
        self.setup_gui()

    def setup_supporting_vars(
            self,
            app_settings,
            dialog_flag,
            input_loadconfirmation_instance,
            loadconfirmation_queries
            ):
        self.app_settings = app_settings
        self.dialog_flag = dialog_flag
        self.input_loadconfirmation_instance = input_loadconfirmation_instance
        self.loadconfirmation_queries = loadconfirmation_queries
        self.loadtypecombolist = []
        self.currencycombolist = []

        self.chosen_carrier = None
        self.chosen_broker = None
        self.chosen_shippers = []
        self.chosen_consignees = []

        self.lcnumber_regex = qtc.QRegExp("^[a-z0-9]*$")
        self.quantity_regex = qtc.QRegExp("^[0-9]*$")
        self.agreedrate_regex = qtc.QRegExp("^[0-9]+(\.[0-9]{1,2})?$")

        # self.setup_database_connection_for_reporting()


    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.main_box = qtw.QVBoxLayout()
        self.title_frame = qtw.QFrame()
        self.central_frame = qtw.QFrame()
        self.data_frame = qtw.QFrame()
        self.buttons_frame = qtw.QFrame()
        self.title_frame_box = qtw.QHBoxLayout()
        self.central_frame_box = qtw.QVBoxLayout()
        self.data_frame_box = qtw.QVBoxLayout()
        self.button_frame_box = qtw.QHBoxLayout()
        self.data_scroll_area = qtw.QScrollArea()
        self.numberratequantity_frame = qtw.QFrame()
        self.numberratequantity_frame_box = qtw.QGridLayout()

        # Depending on flagDialog titleLabel might be also modifying or viewing.
        self.title_label = qtw.QLabel('Add New Load Confirmation')
        self.lcnumber_label = qtw.QLabel('Load Confirmation #')
        self.lcagreedrate_label = qtw.QLabel('Agreed Rate')
        self.lccurrency_label = qtw.QLabel('Currency')
        self.lcquantity_label = qtw.QLabel('Quantity')
        self.lcloadtype_label = qtw.QLabel('Load Type')
        self.lcnumber_lineedit = qtw.QLineEdit()
        self.lcagreedrate_lineedit = qtw.QLineEdit()
        self.lccurrency_comboedit = qtw.QComboBox()
        self.lcquantity_lineedit = qtw.QLineEdit()
        self.lcloadtype_comboedit = qtw.QComboBox()

        self.lcnote_textedit = qtw.QTextEdit()

        self.addcarrier_button = qtw.QPushButton(' Add Carrier  ')
        self.addshipper_button = qtw.QPushButton('Add Shipper ')
        self.addconsignee_button = qtw.QPushButton('Add Consignee')
        self.addbroker_button = qtw.QPushButton(' Add Broker  ')
        self.test_button = qtw.QPushButton('TEST!!!!')
        self.generate_report_button = qtw.QPushButton(' Generate report ')
        self.cncl_button = qtw.QPushButton('   Cancel    ')
        self.ok_button = qtw.QPushButton('   Create    ')

        self.lcnumber_validator = qtg.QRegExpValidator(self.lcnumber_regex, self)
        self.quantity_validator = qtg.QRegExpValidator(self.quantity_regex, self)
        self.agreedrate_validator = qtg.QRegExpValidator(self.agreedrate_regex, self)

    def setup_gui_object_style_names(self):
        self.title_label.setObjectName('title')
        self.data_frame.setObjectName('spacerFrame')
        self.numberratequantity_frame.setObjectName('dataFrame')

    def layout_gui_objects(self):
        self.setLayout(self.main_box)

        self.main_box.addWidget(self.title_frame)
        self.main_box.addWidget(self.central_frame, stretch=1)
        self.main_box.addWidget(self.buttons_frame)

        self.title_frame.setLayout(self.title_frame_box)
        self.central_frame.setLayout(self.central_frame_box)
        self.buttons_frame.setLayout(self.button_frame_box)

        self.title_frame_box.addWidget(self.title_label, 1, qtc.Qt.AlignCenter)

        self.central_frame_box.addWidget(self.data_scroll_area)
        # self.central_frame_box.addStretch()

        self.button_frame_box.addWidget(self.addcarrier_button, alignment=qtc.Qt.AlignLeft)
        self.button_frame_box.addWidget(self.addshipper_button, alignment=qtc.Qt.AlignLeft)
        self.button_frame_box.addWidget(self.addconsignee_button, alignment=qtc.Qt.AlignLeft)
        self.button_frame_box.addWidget(self.addbroker_button, alignment=qtc.Qt.AlignLeft)
        self.button_frame_box.addWidget(self.test_button, alignment=qtc.Qt.AlignLeft)
        self.button_frame_box.addStretch()
        self.button_frame_box.addWidget(self.generate_report_button, alignment=qtc.Qt.AlignRight)
        self.button_frame_box.addWidget(self.cncl_button, alignment=qtc.Qt.AlignRight)
        self.button_frame_box.addWidget(self.ok_button, alignment=qtc.Qt.AlignRight)

        self.data_scroll_area.setWidget(self.data_frame)
        self.data_scroll_area.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.data_scroll_area.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.data_scroll_area.setWidgetResizable(True)

        self.data_frame.setLayout(self.data_frame_box)
        self.data_frame_box.addStretch()
        self.data_frame_box.addWidget(self.numberratequantity_frame, alignment=qtc.Qt.AlignTop)

        self.numberratequantity_frame.setLayout(self.numberratequantity_frame_box)
        self.numberratequantity_frame_box.addWidget(self.lcnumber_label, 0, 0, 1, 1)
        self.numberratequantity_frame_box.addWidget(self.lcnumber_lineedit, 0, 1, 1, 1)
        self.numberratequantity_frame_box.addWidget(self.lcagreedrate_label, 0, 2, 1, 1)
        self.numberratequantity_frame_box.addWidget(self.lcagreedrate_lineedit, 0, 3, 1, 1)
        self.numberratequantity_frame_box.addWidget(self.lcquantity_label, 0, 4, 1, 1)
        self.numberratequantity_frame_box.addWidget(self.lcquantity_lineedit, 0, 5, 1, 1)
        self.numberratequantity_frame_box.addWidget(self.lccurrency_label, 1, 2, 1, 1)
        self.numberratequantity_frame_box.addWidget(self.lccurrency_comboedit, 1, 3, 1, 1)
        self.numberratequantity_frame_box.addWidget(self.lcloadtype_label, 1, 4, 1, 1)
        self.numberratequantity_frame_box.addWidget(self.lcloadtype_comboedit, 1, 5, 1, 1)
        self.numberratequantity_frame_box.addWidget(self.lcnote_textedit, 2, 0, 1, 6)

    def feature_gui_objects(self):
        self.setup_window_geometry()
        self.lcnumber_lineedit.setValidator(self.lcnumber_validator)
        self.lcquantity_lineedit.setValidator(self.quantity_validator)
        self.lcagreedrate_lineedit.setValidator(self.agreedrate_validator)
        self.load_currency_combo()
        self.load_loadtype_combo()
        self.data_scroll_area.setWidgetResizable(True)

        # setting up window depending on flagDialog
        # insert, delete, modify or view
        if self.dialog_flag == LCSettings.Settings.INSERT:
            self.title_label.setText('Add Load Confirmation')
            self.ok_button.setText('  Create    ')
            self.generate_report_button.setEnabled(False)
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.title_label.setText('Delete Load Confirmation')
            self.ok_button.setText('  Delete    ')
            self.load_current_data()
            self.disable_editing()
        elif self.dialog_flag == LCSettings.Settings.MODIFY:
            self.title_label.setText('Modify Load Confirmation')
            self.ok_button.setText('  Modify    ')
            self.addbroker_button.setEnabled(False)
            self.addcarrier_button.setEnabled(False)
            self.generate_report_button.setEnabled(False)
            self.load_current_data()
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.title_label.setText('View Load Confirmation')
            self.ok_button.setText('   Close    ')
            self.load_current_data()
            self.disable_editing()

    def setup_window_geometry(self):
        window_x_coord = int(
            self.app_settings.screen_width / 2
            - self.app_settings.loadconfirmationwindow_width / 2
        )
        window_y_coord = int(
            self.app_settings.screen_height / 2
            - self.app_settings.loadconfirmationwindow_height / 2
        )
        self.setGeometry(window_x_coord,
                         0,
                         self.app_settings.loadconfirmationwindow_width,
                         self.app_settings.screen_height
                         )
        self.setMinimumSize(
            self.app_settings.loadconfirmationwindow_width,
            self.app_settings.loadconfirmationwindow_height
        )

    def load_loadtype_combo(self):
        self.loadtypecombolist = self.loadconfirmation_queries.get_all_loadtypes()
        self.lcloadtype_comboedit.addItems([
            loadtype.loadtypename for loadtype
            in self.loadtypecombolist
        ])

    def load_currency_combo(self):
        self.currencycombolist = self.loadconfirmation_queries.get_all_currencies()
        self.lccurrency_comboedit.addItems([
            currency.currencyshortname for currency
            in self.currencycombolist
        ])

    def disable_editing(self):
        self.lcnumber_lineedit.setEnabled(False)
        self.lcagreedrate_lineedit.setEnabled(False)
        self.lcquantity_lineedit.setEnabled(False)
        self.lccurrency_comboedit.setEnabled(False)
        self.lcloadtype_comboedit.setEnabled(False)
        self.cncl_button.setVisible(False)
        self.addcarrier_button.setVisible(False)
        self.addbroker_button.setVisible(False)
        self.addshipper_button.setVisible(False)
        self.addconsignee_button.setVisible(False)

    def load_current_data(self):
        if self.dialog_flag == LCSettings.Settings.INSERT:
            pass
        elif (self.dialog_flag == LCSettings.Settings.DELETE or
              self.dialog_flag == LCSettings.Settings.MODIFY or
              self.dialog_flag == LCSettings.Settings.VIEW):
            self.load_number_rate_quantity_note()
            self.load_loadtype()
            self.load_currency()
            self.load_carrier()
            self.load_broker()
            self.load_shippers()
            self.load_consignees()

    def load_number_rate_quantity_note(self):
        self.lcnumber_lineedit.setText(self.input_loadconfirmation_instance.lcno)
        self.lcagreedrate_lineedit.setText(str(self.input_loadconfirmation_instance.lcagreedrate))
        self.lcquantity_lineedit.setText(str(self.input_loadconfirmation_instance.lcquantity))
        self.lcnote_textedit.setText(self.input_loadconfirmation_instance.lcnote)

    def load_loadtype(self):
        currectloadtype = [
            loadtype for loadtype
            in self.loadtypecombolist
            if loadtype.loadtypeid == self.input_loadconfirmation_instance.lcloadtypeid
        ]
        if len(currectloadtype) == 1:
            self.lcloadtype_comboedit.setCurrentText(currectloadtype[0].loadtypename)
        else:
            self.loadconfirmation_queries.emit(
                -100000,
                'Error has occurred during population of currency combobox. '
                'Check your log.'
            )

    def load_currency(self):
        currectcurrency = [
            currency for currency
            in self.currencycombolist
            if currency.currencyid == self.input_loadconfirmation_instance.lccurrencyid
        ]
        if len(currectcurrency) == 1:
            self.lccurrency_comboedit.setCurrentText(currectcurrency[0].currencyshortname)
        else:
            self.loadconfirmation_queries.emit(
                -100000,
                'Error has occurred during population of currency combobox. '
                'Check your log.'
            )

    def load_carrier(self):
        self.chosen_carrier = self.loadconfirmation_queries.get_carrier_by_lcid(self.input_loadconfirmation_instance.lcid)
        if isinstance(self.chosen_carrier, CarrierInstance):
            if (self.dialog_flag == LCSettings.Settings.DELETE or
                    self.dialog_flag == LCSettings.Settings.VIEW):
                carrier_frame = CarrierFrame(delete_button_bool=False, input_carrier_instance=self.chosen_carrier)
                self.data_frame_box.addWidget(carrier_frame, alignment=qtc.Qt.AlignTop)
                self.addcarrier_button.setEnabled(False)
            elif (self.dialog_flag == LCSettings.Settings.MODIFY):
                carrier_frame = CarrierFrame(delete_button_bool=True, input_carrier_instance=self.chosen_carrier)
                self.data_frame_box.addWidget(carrier_frame, alignment=qtc.Qt.AlignTop)
                carrier_frame.delete_button.clicked.connect(self.delete_carrier)
        else:
            qtw.QMessageBox(
                qtw.QMessageBox.Critical,
                "Fail", "Record of carrier for this load confirmation was corrupted",
                qtw.QMessageBox.Yes
            ).exec_()

    def load_broker(self):
        self.chosen_broker = self.loadconfirmation_queries.get_broker_by_lcid(self.input_loadconfirmation_instance.lcid)
        if isinstance(self.chosen_broker, BrokerInstance):
            if (self.dialog_flag == LCSettings.Settings.DELETE or
                    self.dialog_flag == LCSettings.Settings.VIEW):
                broker_frame = BrokerFrame(delete_button_bool=False, input_broker_instance=self.chosen_broker)
                self.data_frame_box.addWidget(broker_frame, alignment=qtc.Qt.AlignTop)
                self.addbroker_button.setEnabled(False)
            elif (self.dialog_flag == LCSettings.Settings.MODIFY):
                broker_frame = BrokerFrame(delete_button_bool=True, input_broker_instance=self.chosen_broker)
                self.data_frame_box.addWidget(broker_frame, alignment=qtc.Qt.AlignTop)
                broker_frame.delete_button.clicked.connect(self.delete_broker)
        else:
            qtw.QMessageBox(
                qtw.QMessageBox.Critical,
                "Fail", "Record of custom broker for this load confirmation was corrupted",
                qtw.QMessageBox.Yes
            ).exec_()

    def load_shippers(self):
        shippers_bindto_lc = \
            self.loadconfirmation_queries.get_all_shippers_by_lcid(self.input_loadconfirmation_instance.lcid)
        if len(shippers_bindto_lc) == 0:
            qtw.QMessageBox(
                qtw.QMessageBox.Critical,
                "Fail", "Records of shippers for this load confirmation were corrupted",
                qtw.QMessageBox.Yes
            ).exec_()
        else:
            for shipper_ref_item, shipper_item in shippers_bindto_lc:
                if (self.dialog_flag == LCSettings.Settings.DELETE or
                        self.dialog_flag == LCSettings.Settings.VIEW):
                    shipper_frame = ShipperFrame(
                        delete_button_bool=False,
                        input_shipper_instance=shipper_item,
                        input_shipperref_instance=shipper_ref_item
                    )
                    shipper_frame.change_sequence_number(len(self.chosen_shippers) + 1)
                    self.data_frame_box.addWidget(shipper_frame, alignment=qtc.Qt.AlignTop)
                    self.chosen_shippers.append(shipper_ref_item)
                elif (self.dialog_flag == LCSettings.Settings.MODIFY):
                    shipper_frame = ShipperFrame(
                        delete_button_bool=True,
                        input_shipper_instance=shipper_item,
                        input_shipperref_instance=shipper_ref_item
                    )
                    shipper_frame.change_sequence_number(len(self.chosen_shippers) + 1)
                    shipper_frame.deleteframe_signal.connect(self.delete_shipper)
                    self.data_frame_box.addWidget(shipper_frame, alignment=qtc.Qt.AlignTop)
                    self.chosen_shippers.append(shipper_ref_item)

    def load_consignees(self):
        consignees_bindto_lc = \
            self.loadconfirmation_queries.get_all_consignees_by_lcid(self.input_loadconfirmation_instance.lcid)
        if len(consignees_bindto_lc) == 0:
            qtw.QMessageBox(
                qtw.QMessageBox.Critical,
                "Fail", "Records of consginees for this load confirmation were corrupted",
                qtw.QMessageBox.Yes
            ).exec_()
        else:
            for consignee_ref_item, consignee_item in consignees_bindto_lc:
                if (self.dialog_flag == LCSettings.Settings.DELETE or
                        self.dialog_flag == LCSettings.Settings.VIEW):
                    consignee_frame = ConsigneeFrame(
                        delete_button_bool=False,
                        input_consignee_instance=consignee_item,
                        input_consigneeref_instance=consignee_ref_item
                    )
                    consignee_frame.change_sequence_number(len(self.chosen_consignees) + 1)
                    self.data_frame_box.addWidget(consignee_frame, alignment=qtc.Qt.AlignTop)
                    self.chosen_consignees.append(consignee_ref_item)
                elif (self.dialog_flag == LCSettings.Settings.MODIFY):
                    consignee_frame = ConsigneeFrame(
                        delete_button_bool=True,
                        input_consignee_instance=consignee_item,
                        input_consigneeref_instance=consignee_ref_item
                    )
                    consignee_frame.change_sequence_number(len(self.chosen_consignees) + 1)
                    consignee_frame.deleteframe_signal.connect(self.delete_consignee)
                    self.data_frame_box.addWidget(consignee_frame, alignment=qtc.Qt.AlignTop)
                    self.chosen_consignees.append(consignee_ref_item)

    def setup_gui_object_events(self):
        self.cncl_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.process_loadconfirmation_data)
        self.addcarrier_button.clicked.connect(self.add_carrier_action)
        self.addshipper_button.clicked.connect(self.add_shipper_action)
        self.addconsignee_button.clicked.connect(self.add_consignee_action)
        self.addbroker_button.clicked.connect(self.add_broker_action)
        self.generate_report_button.clicked.connect(self.generate_report)

    def process_loadconfirmation_data(self):
        self.central_frame.setVisible(True)
        if self.dialog_flag == LCSettings.Settings.INSERT and self.is_all_info_entered():
            self.new_loadconfirmation_instance = LoadConfirmationInstance(
                lccurrencyid=
                self.currencycombolist[self.lccurrency_comboedit.currentIndex()].currencyid,
                lcloadtypeid=
                self.loadtypecombolist[self.lcloadtype_comboedit.currentIndex()].loadtypeid,
                lccarrierid=
                self.chosen_carrier.carrierid,
                lccustombrokerid=
                self.chosen_broker.custombrokerid,
                lcnote=
                self.lcnote_textedit.toPlainText(),
                lcno=
                self.lcnumber_lineedit.text(),
                lcagreedrate=
                float(self.lcagreedrate_lineedit.text()),
                lcquantity=
                int(self.lcquantity_lineedit.text()),
                lccurrencyshortname=
                self.currencycombolist[self.lccurrency_comboedit.currentIndex()].currencyshortname,
                lcloadtypename=
                self.loadtypecombolist[self.lcloadtype_comboedit.currentIndex()].loadtypename,
                lccarriername=
                self.chosen_carrier.carriername,
                lccustombrokername=
                self.chosen_broker.custombrokername,
                lcdatecreated=
                qtc.QDate().currentDate()
            )
            operation_returm_code = self.loadconfirmation_queries.insert_loadconfirmation(
                self.new_loadconfirmation_instance,
                self.chosen_shippers,
                self.chosen_consignees
            )
            if operation_returm_code == 0:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Success", "New load confirmation was created",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.accept()
            elif operation_returm_code == 1:
                retry = qtw.QMessageBox.question(self,
                                                 'Fail',
                                                 "Check if chosen load confirmation # was not used\n"
                                                 "Try again?",
                                                 qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)
                if retry == qtw.QMessageBox.Yes:
                    self.lcnumber_lineedit.setFocus()
                else:
                    self.reject()
        elif self.dialog_flag == LCSettings.Settings.MODIFY and self.is_all_info_entered():
            self.modify_loadconfirmation_instance = LoadConfirmationInstance(
                lcid=
                self.input_loadconfirmation_instance.lcid,
                lccurrencyid=
                self.currencycombolist[self.lccurrency_comboedit.currentIndex()].currencyid,
                lcloadtypeid=
                self.loadtypecombolist[self.lcloadtype_comboedit.currentIndex()].loadtypeid,
                lccarrierid=
                self.chosen_carrier.carrierid,
                lccustombrokerid=
                self.chosen_broker.custombrokerid,
                lcnote=
                self.lcnote_textedit.toPlainText(),
                lcno=
                self.lcnumber_lineedit.text(),
                lcagreedrate=
                float(self.lcagreedrate_lineedit.text()),
                lcquantity=
                int(self.lcquantity_lineedit.text()),
                lccurrencyshortname=
                self.currencycombolist[self.lccurrency_comboedit.currentIndex()].currencyshortname,
                lcloadtypename=
                self.loadtypecombolist[self.lcloadtype_comboedit.currentIndex()].loadtypename,
                lccarriername=
                self.chosen_carrier.carriername,
                lccustombrokername=
                self.chosen_broker.custombrokername,
                lcdatecreated=
                qtc.QDate().currentDate(),
                lccreatedby=
                self.input_loadconfirmation_instance.lccreatedby
            )
            operation_returm_code = self.loadconfirmation_queries.modify_loadconfirmation(
                self.modify_loadconfirmation_instance,
                self.chosen_shippers,
                self.chosen_consignees
            )
            if operation_returm_code == 0:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Success", "Load confirmation was updated",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.accept()
            elif operation_returm_code == 1:
                retry = qtw.QMessageBox.question(self,
                                                 'Fail',
                                                 "Check if chosen load confirmation # was not used\n"
                                                 'Or uniqueness of load confirmation number was not corrupted\n'
                                                 "Try again?",
                                                 qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)
                if retry == qtw.QMessageBox.Yes:
                    self.lcnumber_lineedit.setFocus()
                else:
                    self.reject()
        elif self.dialog_flag == LCSettings.Settings.VIEW:
            self.accept()
        elif self.dialog_flag == LCSettings.Settings.DELETE:
            self.delete_loadconfirmation_instance = LoadConfirmationInstance(
                lcid=
                self.input_loadconfirmation_instance.lcid,
                lccurrencyid=
                self.currencycombolist[self.lccurrency_comboedit.currentIndex()].currencyid,
                lcloadtypeid=
                self.loadtypecombolist[self.lcloadtype_comboedit.currentIndex()].loadtypeid,
                lccarrierid=
                self.chosen_carrier.carrierid,
                lccustombrokerid=
                self.chosen_broker.custombrokerid,
                lcnote=
                self.lcnote_textedit.toPlainText(),
                lcno=
                self.lcnumber_lineedit.text(),
                lcagreedrate=
                float(self.lcagreedrate_lineedit.text()),
                lcquantity=
                int(self.lcquantity_lineedit.text()),
                lccurrencyshortname=
                self.currencycombolist[self.lccurrency_comboedit.currentIndex()].currencyshortname,
                lcloadtypename=
                self.loadtypecombolist[self.lcloadtype_comboedit.currentIndex()].loadtypename,
                lccarriername=
                self.chosen_carrier.carriername,
                lccustombrokername=
                self.chosen_broker.custombrokername,
                lcdatecreated=
                qtc.QDate().currentDate(),
                lccreatedby=
                self.input_loadconfirmation_instance.lccreatedby
            )
            operation_returm_code = self.loadconfirmation_queries.deleteLoadconfirmation(
                self.delete_loadconfirmation_instance,
                self.chosen_shippers,
                self.chosen_consignees
            )
            if operation_returm_code == 0:
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Success", "Load confirmation was deleted",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.accept()
            elif operation_returm_code == 1:
                self.loadconfirmation_queries.update_windowmessage_signal.emit(
                    -100000,
                    "Check if chosen load confirmation # was not used\n"
                    'Or uniqueness of load confirmation number was not corrupted\n'
                )
                # self.statusbar.showMessage('Error code: -1. Error message: None selected row')
                #logging this error event
                qtw.QMessageBox(
                    qtw.QMessageBox.Information,
                    "Fail",
                    "Check if chosen load confirmation # was not used\n"
                    'Or uniqueness of load confirmation number was not corrupted\n'
                    "Try again?",
                    qtw.QMessageBox.Yes
                ).exec_()
                self.reject()

    def is_all_info_entered(self):
        if self.chosen_carrier is None:
            qtw.QMessageBox(
                qtw.QMessageBox.Critical,
                "Fail", "You must add carrier to newly created load confirmation",
                qtw.QMessageBox.Yes
            ).exec_()
            raise MissingCarrierInfoError(loadconfirmation_queries=self.loadconfirmation_queries)
        if self.chosen_broker is None:
            qtw.QMessageBox(
                qtw.QMessageBox.Critical,
                "Fail", "You must add broker to newly created load confirmation",
                qtw.QMessageBox.Yes
            ).exec_()
            raise MissingBrokerInfoError(loadconfirmation_queries=self.loadconfirmation_queries)
        if len(self.chosen_shippers) == 0:
            qtw.QMessageBox(
                qtw.QMessageBox.Critical,
                "Fail", "You must add at least one shipper to newly created load confirmation",
                qtw.QMessageBox.Yes
            ).exec_()
            raise MissingShipperInfoError(loadconfirmation_queries=self.loadconfirmation_queries)
        if len(self.chosen_consignees) == 0:
            qtw.QMessageBox(
                qtw.QMessageBox.Critical,
                "Fail", "You must add at least one consignee to newly created load confirmation",
                qtw.QMessageBox.Yes
            ).exec_()
            raise MissingConsigneeInfoError(loadconfirmation_queries=self.loadconfirmation_queries)
        if (self.lcnumber_lineedit.text() == ''
                or self.lcquantity_lineedit.text() == ''
                or self.lcagreedrate_lineedit.text() == ''):
            qtw.QMessageBox(
                qtw.QMessageBox.Critical,
                "Fail", "You must assign load confirmation number, quantity and agreed rate",
                qtw.QMessageBox.Yes
            ).exec_()
            raise MissingConsigneeInfoError(loadconfirmation_queries=self.loadconfirmation_queries)
        return True

    def add_carrier_action(self):
        input_all_carrier = self.loadconfirmation_queries.get_all_carriers()
        if len(input_all_carrier) > 0:
            choose_carrier_window = ChooseCarrierDialog(
                self.app_settings, input_all_carrier
            )
            if choose_carrier_window.exec_() == qtw.QDialog.Accepted:
                self.chosen_carrier = choose_carrier_window.selected_carrier
                carrier_frame = CarrierFrame(delete_button_bool=True, input_carrier_instance=self.chosen_carrier)
                carrier_frame.delete_button.clicked.connect(self.delete_carrier)
                self.data_frame_box.addWidget(carrier_frame, alignment=qtc.Qt.AlignTop)
                self.addcarrier_button.setEnabled(False)
        else:
            qtw.QMessageBox(
                qtw.QMessageBox.Information,
                "Fail", "There is not a single carrier in the database",
                qtw.QMessageBox.Yes
            ).exec_()

    def add_shipper_action(self):
        input_all_shipper = self.loadconfirmation_queries.get_all_shippers()
        if len(input_all_shipper) > 0:
            choose_shipper_window = ChooseShipperDialog(
                self.app_settings, input_all_shipper
            )
            if choose_shipper_window.exec_() == qtw.QDialog.Accepted:
                chosen_shipper = choose_shipper_window.selected_shipper
                chosen_date = choose_shipper_window.data_frame.shipper_date_editline.date().toPyDate()
                chosen_time = choose_shipper_window.data_frame.shipper_time_editline.text()
                shipper_ref_instance = ShipperRefInstance(
                    shipperid=chosen_shipper.shipperid,
                    shipperdate=chosen_date,
                    shippertime=chosen_time
                )
                shipper_frame = ShipperFrame(
                    delete_button_bool=True,
                    input_shipper_instance=chosen_shipper,
                    input_shipperref_instance=shipper_ref_instance
                )
                shipper_frame.change_sequence_number(len(self.chosen_shippers) + 1)
                shipper_frame.deleteframe_signal.connect(self.delete_shipper)
                self.data_frame_box.addWidget(shipper_frame, alignment=qtc.Qt.AlignTop)
                self.chosen_shippers.append(shipper_ref_instance)
        else:
            qtw.QMessageBox(
                qtw.QMessageBox.Information,
                "Fail", "There is not a single shipper in the database",
                qtw.QMessageBox.Yes
            ).exec_()

    def add_consignee_action(self):
        input_all_consignee = self.loadconfirmation_queries.get_all_consignees()
        if len(input_all_consignee) > 0:
            choose_consignee_window = ChooseConsigneeDialog(
                self.app_settings, input_all_consignee
            )
            if choose_consignee_window.exec_() == qtw.QDialog.Accepted:
                chosen_consignee = choose_consignee_window.selected_consignee
                chosen_date = choose_consignee_window.data_frame.consignee_date_editline.date().toPyDate()
                chosen_time = choose_consignee_window.data_frame.consignee_time_editline.text()
                consignee_ref_instance = ConsigneeRefInstance(
                    consigneeid=chosen_consignee.consigneeid,
                    consigneedate=chosen_date,
                    consigneetime=chosen_time
                )
                consignee_frame = ConsigneeFrame(
                    delete_button_bool=True,
                    input_consignee_instance=chosen_consignee,
                    input_consigneeref_instance=consignee_ref_instance
                )
                consignee_frame.change_sequence_number(len(self.chosen_consignees) + 1)
                consignee_frame.deleteframe_signal.connect(self.delete_consignee)
                self.data_frame_box.addWidget(consignee_frame, alignment=qtc.Qt.AlignTop)
                self.chosen_consignees.append(consignee_ref_instance)
        else:
            qtw.QMessageBox(
                qtw.QMessageBox.Information,
                "Fail", "There is not a single consignee in the database",
                qtw.QMessageBox.Yes
            ).exec_()

    def add_broker_action(self):
        input_all_broker = self.loadconfirmation_queries.get_all_brokers()
        if len(input_all_broker) > 0:
            choose_broker_window = ChooseBrokerDialog(
                self.app_settings, input_all_broker
            )
            if choose_broker_window.exec_() == qtw.QDialog.Accepted:
                self.chosen_broker = choose_broker_window.selected_broker
                broker_frame = BrokerFrame(delete_button_bool=True, input_broker_instance=self.chosen_broker)
                broker_frame.delete_button.clicked.connect(self.delete_broker)
                self.data_frame_box.addWidget(broker_frame, alignment=qtc.Qt.AlignTop)
                self.addbroker_button.setEnabled(False)
        else:
            qtw.QMessageBox(
                qtw.QMessageBox.Information,
                "Fail", "There is not a single broker in the database",
                qtw.QMessageBox.Yes
            ).exec_()

    def delete_carrier(self):
        self.chosen_carrier = None
        self.addcarrier_button.setEnabled(True)

    def delete_broker(self):
        self.chosen_broker = None
        self.addbroker_button.setEnabled(True)

    def delete_shipper(self, deleted_shipper):
        self.chosen_shippers.remove(deleted_shipper)
        self.rearrange_shippers_sequence()

    def rearrange_shippers_sequence(self):
        index_counter = 1
        for frame in self.data_frame.children():
            if (isinstance(frame, ShipperFrame)
                    and frame.input_shipperref_instance in self.chosen_shippers):
                frame.change_sequence_number(index_counter)
                index_counter += 1

    def delete_consignee(self, deleted_consignee):
        self.chosen_consignees.remove(deleted_consignee)
        self.rearrange_consignees_sequence()

    def rearrange_consignees_sequence(self):
        index_counter = 1
        for frame in self.data_frame.children():
            if (isinstance(frame, ConsigneeFrame)
                    and frame.input_consigneeref_instance in self.chosen_consignees):
                frame.change_sequence_number(index_counter)
                index_counter += 1

    # def setup_database_connection_for_reporting(self):
    #     if self.app_settings:
    #         self.database_connection = {
    #             'driver': 'oracle',
    #             'jdbc_driver': 'oracle.jdbc.driver.OracleDriver',
    #             'host': self.app_settings.server,
    #             'port': self.app_settings.port,
    #             'db_sid': self.app_settings.sid,
    #             'username': self.app_settings.user,
    #             'password': self.app_settings.password
    #         }

    def generate_report(self):
        self.generate_report_button.setEnabled(False)
        qtw.QApplication.processEvents()
        application_folderpath = \
            self.app_settings.application_folderpath
        report_template_folderpath = \
            os.path.join(application_folderpath, 'resources/report_templates/')
        report_template_filepath = \
            os.path.join(report_template_folderpath, self.app_settings.report_template_name)
        generated_report_filepath = \
            os.path.join(
                application_folderpath,
                f'resources/generated_reports/{(str(time.time()).replace(".", ""))}'
            )
        report_parameters = self.generate_report_parameters()
        print(report_parameters)
        pyreportjasper_instance = pyreportjasper.PyReportJasper()
        pyreportjasper_instance.config(
            report_template_filepath,
            generated_report_filepath,
            # db_connection=self.database_connection,
            parameters=report_parameters,
            output_formats=["pdf"],
            locale='en_US'
        )
        pyreportjasper_instance.process_report()
        open_generated_report_answer = qtw.QMessageBox.question(
            self,
            'Report', 'Report was generated.\n Do you want to open it?',
            qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes
            )
        if open_generated_report_answer == qtw.QMessageBox.Yes:
            self.open_generated_report(generated_report_filepath)
        self.generate_report_button.setEnabled(True)

    def open_generated_report(self, generated_report_filepath):
        webbrowser.open_new(generated_report_filepath + '.pdf')

    def generate_report_parameters(self):
        parameter_dict = {}
        self.setup_carrier_parameters(parameter_dict)
        self.setup_broker_parameters(parameter_dict)
        self.setup_additional_parameters(parameter_dict)
        self.setup_shippers_parameters(parameter_dict)
        self.setup_consignee_parameters(parameter_dict)
        return parameter_dict

    def setup_shippers_parameters(self, parameter_dict):
        shipper_bindto_lc = \
            self.loadconfirmation_queries.get_all_shippers_by_lcid(self.input_loadconfirmation_instance.lcid)
        for shipper_index in range(1, len(shipper_bindto_lc)+1):
            parameter_dict[f'shipper{str(shipper_index)}_name'] = \
                shipper_bindto_lc[shipper_index-1][1].shippername
            parameter_dict[f'shipper{str(shipper_index)}_address'] = \
                shipper_bindto_lc[shipper_index-1][1].shipperaddress
            parameter_dict[f'shipper{str(shipper_index)}_city'] = \
                shipper_bindto_lc[shipper_index-1][1].shippercity
            parameter_dict[f'shipper{str(shipper_index)}_state'] = \
                shipper_bindto_lc[shipper_index-1][1].shipperstate
            parameter_dict[f'shipper{str(shipper_index)}_phone'] = \
                shipper_bindto_lc[shipper_index-1][1].shipperphone
            parameter_dict[f'shipper{str(shipper_index)}_fax'] = \
                shipper_bindto_lc[shipper_index-1][1].shipperfax
            parameter_dict[f'shipper{str(shipper_index)}_tollfree'] = \
                shipper_bindto_lc[shipper_index-1][1].shippertollfree
            parameter_dict[f'shipper{str(shipper_index)}_contact'] = \
                shipper_bindto_lc[shipper_index-1][1].shippercontact
            parameter_dict[f'pickup{str(shipper_index)}_date'] = \
                qtc.QDateTime(
                    shipper_bindto_lc[shipper_index-1][0].shipperdate
                    ).toString('yyyy-MM-dd')
            parameter_dict[f'pickup{str(shipper_index)}_time'] = \
                shipper_bindto_lc[shipper_index-1][0].shippertime

    def setup_consignee_parameters(self, parameter_dict):
        consignee_bindto_lc = \
            self.loadconfirmation_queries.get_all_consignees_by_lcid(self.input_loadconfirmation_instance.lcid)
        for consignee_index in range(1, len(consignee_bindto_lc)+1):
            parameter_dict[f'consignee{str(consignee_index)}_name'] = \
                consignee_bindto_lc[consignee_index-1][1].consigneename
            parameter_dict[f'consignee{str(consignee_index)}_address'] = \
                consignee_bindto_lc[consignee_index-1][1].consigneeaddress
            parameter_dict[f'consignee{str(consignee_index)}_city'] = \
                consignee_bindto_lc[consignee_index-1][1].consigneecity
            parameter_dict[f'consignee{str(consignee_index)}_state'] = \
                consignee_bindto_lc[consignee_index-1][1].consigneestate
            parameter_dict[f'consignee{str(consignee_index)}_phone'] = \
                consignee_bindto_lc[consignee_index-1][1].consigneephone
            parameter_dict[f'consignee{str(consignee_index)}_fax'] = \
                consignee_bindto_lc[consignee_index-1][1].consigneefax
            parameter_dict[f'consignee{str(consignee_index)}_tollfree'] = \
                consignee_bindto_lc[consignee_index-1][1].consigneetollfree
            parameter_dict[f'consignee{str(consignee_index)}_contact'] = \
                consignee_bindto_lc[consignee_index-1][1].consigneecontact
            parameter_dict[f'drop{str(consignee_index)}_date'] = \
                qtc.QDateTime(
                    consignee_bindto_lc[consignee_index-1][0].consigneedate
                    ).toString('yyyy-MM-dd')
            parameter_dict[f'drop{str(consignee_index)}_time'] = \
                consignee_bindto_lc[consignee_index-1][0].consigneetime

    def setup_carrier_parameters(self, parameter_dict):
        parameter_dict['carrier_name'] = self.chosen_carrier.carriername
        parameter_dict['carrier_address'] = self.chosen_carrier.carrieraddress
        parameter_dict['carrier_city'] = self.chosen_carrier.carriercity
        parameter_dict['carrier_state'] = self.chosen_carrier.carrierstate
        parameter_dict['carrier_phone'] = self.chosen_carrier.carrierphone
        parameter_dict['carrier_fax'] = self.chosen_carrier.carrierfax
        parameter_dict['carrier_tollfree'] = self.chosen_carrier.carriertollfree
        parameter_dict['carrier_contact'] = self.chosen_carrier.carriercontact

    def setup_broker_parameters(self, parameter_dict):
        parameter_dict['broker_name'] = self.chosen_broker.custombrokername
        parameter_dict['broker_phone'] = self.chosen_broker.custombrokerphone
        parameter_dict['broker_fax'] = self.chosen_broker.custombrokerfax
        parameter_dict['broker_tollfree'] = self.chosen_broker.custombrokertollfree
        parameter_dict['broker_contact'] = self.chosen_broker.custombrokercontact

    def setup_additional_parameters(self, parameter_dict):
        parameter_dict['lcno'] = self.input_loadconfirmation_instance.lcno
        parameter_dict['agreed_rate'] = str(self.input_loadconfirmation_instance.lcagreedrate)
        parameter_dict['quantity'] = str(self.input_loadconfirmation_instance.lcquantity)
        parameter_dict['note'] = self.input_loadconfirmation_instance.lcnote
        currency_instance = self.loadconfirmation_queries.get_currency_by_lcid(
            self.input_loadconfirmation_instance.lcid
            )
        parameter_dict['currency'] =  currency_instance.currencyimagepath
        loadtype_instance = self.loadconfirmation_queries.get_loadtype_by_lcid(
            self.input_loadconfirmation_instance.lcid
            )
        parameter_dict['type'] = loadtype_instance.loadtypename


