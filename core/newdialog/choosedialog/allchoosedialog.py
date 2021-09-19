"""Module allchoosedialog contains dialog classes

All classes in this modules are subclasses from QDialog.
These dialogs responsible for choosing  shipper, consignee, broker and carrier information
during steps of building one load confirmation.
Each dialog contains combo-box with the list of all entities (for instance carriers)
and central data_frame that displays break-down information of currently chosen entity in the combo-box.
These are: ChooseBrokerDialog, ChooseCarrierDialog, ChooseConsigneeDialog, ChooseShipperDialog.
"""
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
from core.newdialog.choosedialog.alldataframes import (BrokerFrame, CarrierFrame,
                                                       ShipperFrame, ConsigneeFrame)


class ChooseBrokerDialog(qtw.QDialog):

    def __init__(self, app_settings, input_all_brokers):
        super().__init__()
        self.setup_supporting_vars(app_settings, input_all_brokers)
        self.setup_gui()

    def setup_supporting_vars(self, app_settings, input_all_brokers):
        self.app_settings = app_settings
        self.input_all_brokers = input_all_brokers
        self.selected_broker = input_all_brokers[0]

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.main_box = qtw.QVBoxLayout()

        self.title_frame = qtw.QFrame()
        self.data_frame = BrokerFrame()
        self.buttons_frame = qtw.QFrame()
        self.title_framebox = qtw.QHBoxLayout()
        # layout for dataFrame is setup in its custom class BrokerFrame
        self.buttons_framebox = qtw.QHBoxLayout()

        self.title_label = qtw.QLabel('Choose Broker')
        self.choose_broker_combobox = qtw.QComboBox()
        self.cncl_button = qtw.QPushButton('   Cancel    ')
        self.ok_button = qtw.QPushButton('   Choose    ')

    def setup_gui_object_style_names(self):
        self.title_label.setObjectName('title')

    def layout_gui_objects(self):
        self.setLayout(self.main_box)

        self.main_box.addWidget(self.title_frame)
        self.main_box.addWidget(self.data_frame, stretch=1)
        self.main_box.addWidget(self.buttons_frame)

        self.title_frame.setLayout(self.title_framebox)
        self.buttons_frame.setLayout(self.buttons_framebox)

        self.title_framebox.addWidget(self.title_label, qtc.Qt.AlignLeft)
        self.title_framebox.addWidget(self.choose_broker_combobox, qtc.Qt.AlignLeft)

        self.buttons_framebox.addStretch()
        self.buttons_framebox.addWidget(self.cncl_button, alignment=qtc.Qt.AlignRight)
        self.buttons_framebox.addWidget(self.ok_button, alignment=qtc.Qt.AlignRight)

    def feature_gui_objects(self):
        self.setWindowTitle('Choose Broker Window')
        self.setup_window_geometry()
        self.load_broker_combo()
        self.data_frame.reload_broker_data(self.input_all_brokers[0])

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
                         window_y_coord,
                         self.app_settings.loadconfirmationwindow_width,
                         self.app_settings.loadconfirmationwindow_height
                         )
        self.setMinimumSize(
            self.app_settings.loadconfirmationwindow_width,
            self.app_settings.loadconfirmationwindow_height
        )

    def load_broker_combo(self):
        self.choose_broker_combobox.addItems([
            broker.custombrokername for broker
            in self.input_all_brokers
            ])
        self.choose_broker_combobox.setCurrentIndex(0)

    def setup_gui_object_events(self):
        self.cncl_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.accept)
        self.choose_broker_combobox.currentIndexChanged.connect(self.broker_combobox_action)

    def broker_combobox_action(self, currentIndex):
        self.selected_broker = self.input_all_brokers[currentIndex]
        self.data_frame.reload_broker_data(self.selected_broker)


class ChooseCarrierDialog(qtw.QDialog):

    def __init__(self, app_settings, input_all_carriers):
        super().__init__()
        self.setup_supporting_vars(app_settings, input_all_carriers)
        self.setup_gui()

    def setup_supporting_vars(self, app_settings, input_all_carriers):
        self.app_settings = app_settings
        self.input_all_carriers = input_all_carriers
        self.selected_carrier = input_all_carriers[0]

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.main_box = qtw.QVBoxLayout()

        self.title_frame = qtw.QFrame()
        self.data_frame = CarrierFrame()
        self.buttons_frame = qtw.QFrame()
        self.title_framebox = qtw.QHBoxLayout()
        # layout for dataFrame is setup in its custom class CarrierFrame
        self.buttons_framebox = qtw.QHBoxLayout()

        self.title_label = qtw.QLabel('Choose Carrier')
        self.choose_carrier_combobox = qtw.QComboBox()
        self.cncl_button = qtw.QPushButton('   Cancel    ')
        self.ok_button = qtw.QPushButton('   Choose    ')

    def setup_gui_object_style_names(self):
        self.title_label.setObjectName('title')

    def layout_gui_objects(self):
        self.setLayout(self.main_box)

        self.main_box.addWidget(self.title_frame)
        self.main_box.addWidget(self.data_frame, stretch=1)
        self.main_box.addWidget(self.buttons_frame)

        self.title_frame.setLayout(self.title_framebox)
        self.buttons_frame.setLayout(self.buttons_framebox)

        self.title_framebox.addWidget(self.title_label, qtc.Qt.AlignLeft)
        self.title_framebox.addWidget(self.choose_carrier_combobox, qtc.Qt.AlignLeft)

        self.buttons_framebox.addStretch()
        self.buttons_framebox.addWidget(self.cncl_button, alignment=qtc.Qt.AlignRight)
        self.buttons_framebox.addWidget(self.ok_button, alignment=qtc.Qt.AlignRight)

    def feature_gui_objects(self):
        self.setWindowTitle('Choose Carrier Window')
        self.setup_window_geometry()
        self.load_carrier_combo()
        self.data_frame.reload_carrier_data(self.input_all_carriers[0])

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
                         window_y_coord,
                         self.app_settings.loadconfirmationwindow_width,
                         self.app_settings.loadconfirmationwindow_height
                         )
        self.setMinimumSize(
            self.app_settings.loadconfirmationwindow_width,
            self.app_settings.loadconfirmationwindow_height
        )

    def load_carrier_combo(self):
        self.choose_carrier_combobox.addItems([
            carrier.carriername for carrier
            in self.input_all_carriers
        ])
        self.choose_carrier_combobox.setCurrentIndex(0)

    def setup_gui_object_events(self):
        self.cncl_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.accept)
        self.choose_carrier_combobox.currentIndexChanged.connect(self.carrier_combobox_action)

    def carrier_combobox_action(self, currentIndex):
        self.selected_carrier = self.input_all_carriers[currentIndex]
        self.data_frame.reload_carrier_data(self.selected_carrier)


class ChooseConsigneeDialog(qtw.QDialog):

    def __init__(self, app_settings, input_all_consignees):
        super().__init__()
        self.setup_supporting_vars(app_settings, input_all_consignees)
        self.setup_gui()

    def setup_supporting_vars(self, app_settings, input_all_consignees):
        self.app_settings = app_settings
        self.input_all_consignees = input_all_consignees
        self.selected_consignee = input_all_consignees[0]

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.main_box = qtw.QVBoxLayout()

        self.title_frame = qtw.QFrame()
        # layout for dataFrame is setup in its custom class ConsigneeFrame
        self.data_frame = ConsigneeFrame()
        self.buttons_frame = qtw.QFrame()
        self.title_framebox = qtw.QHBoxLayout()
        self.buttons_framebox = qtw.QHBoxLayout()

        self.title_label = qtw.QLabel('Choose Consignee')
        self.choose_consignee_combobox = qtw.QComboBox()
        self.cncl_button = qtw.QPushButton('   Cancel    ')
        self.ok_button = qtw.QPushButton('   Choose    ')

    def setup_gui_object_style_names(self):
        self.title_label.setObjectName('title')

    def layout_gui_objects(self):
        self.setLayout(self.main_box)

        self.main_box.addWidget(self.title_frame)
        self.main_box.addWidget(self.data_frame, stretch=1)
        self.main_box.addWidget(self.buttons_frame)

        self.title_frame.setLayout(self.title_framebox)
        self.buttons_frame.setLayout(self.buttons_framebox)

        self.title_framebox.addWidget(self.title_label, qtc.Qt.AlignLeft)
        self.title_framebox.addWidget(self.choose_consignee_combobox, qtc.Qt.AlignLeft)

        self.buttons_framebox.addStretch()
        self.buttons_framebox.addWidget(self.cncl_button, alignment=qtc.Qt.AlignRight)
        self.buttons_framebox.addWidget(self.ok_button, alignment=qtc.Qt.AlignRight)

    def feature_gui_objects(self):
        self.setWindowTitle('Choose Consignee Window')
        self.setup_window_geometry()
        self.load_consignee_combo()
        self.data_frame.reload_consignee_data(self.input_all_consignees[0])

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
                         window_y_coord,
                         self.app_settings.loadconfirmationwindow_width,
                         self.app_settings.loadconfirmationwindow_height
                         )
        self.setMinimumSize(
            self.app_settings.loadconfirmationwindow_width,
            self.app_settings.loadconfirmationwindow_height
        )

    def load_consignee_combo(self):
        self.choose_consignee_combobox.addItems([
            consignee.consigneename for consignee
            in self.input_all_consignees
        ])
        self.choose_consignee_combobox.setCurrentIndex(0)

    def setup_gui_object_events(self):
        self.cncl_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.accept)
        self.choose_consignee_combobox.currentIndexChanged.connect(self.consignee_combobox_action)

    def consignee_combobox_action(self, currentIndex):
        self.selected_consignee = self.input_all_consignees[currentIndex]
        self.data_frame.reload_consignee_data(self.selected_consignee)


class ChooseShipperDialog(qtw.QDialog):

    def __init__(self, app_settings, input_all_shippers):
        super().__init__()
        self.setup_supporting_vars(app_settings, input_all_shippers)
        self.setup_gui()

    def setup_supporting_vars(self, app_settings, input_all_shippers):
        self.app_settings = app_settings
        self.input_all_shippers = input_all_shippers
        self.selected_shipper = input_all_shippers[0]

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.main_box = qtw.QVBoxLayout()

        self.title_frame = qtw.QFrame()
        # layout for dataFrame is setup in its custom class ShipperFrame
        self.data_frame = ShipperFrame()
        self.buttons_frame = qtw.QFrame()
        self.title_framebox = qtw.QHBoxLayout()
        self.buttons_framebox = qtw.QHBoxLayout()

        self.title_label = qtw.QLabel('Choose Shipper')
        self.choose_shipper_combobox = qtw.QComboBox()
        self.cncl_button = qtw.QPushButton('   Cancel    ')
        self.ok_button = qtw.QPushButton('   Choose    ')

    def setup_gui_object_style_names(self):
        self.title_label.setObjectName('title')

    def layout_gui_objects(self):
        self.setLayout(self.main_box)

        self.main_box.addWidget(self.title_frame)
        self.main_box.addWidget(self.data_frame, stretch=1)
        self.main_box.addWidget(self.buttons_frame)

        self.title_frame.setLayout(self.title_framebox)
        self.buttons_frame.setLayout(self.buttons_framebox)

        self.title_framebox.addWidget(self.title_label, qtc.Qt.AlignLeft)
        self.title_framebox.addWidget(self.choose_shipper_combobox, qtc.Qt.AlignLeft)

        self.buttons_framebox.addStretch()
        self.buttons_framebox.addWidget(self.cncl_button, alignment=qtc.Qt.AlignRight)
        self.buttons_framebox.addWidget(self.ok_button, alignment=qtc.Qt.AlignRight)

    def feature_gui_objects(self):
        self.setWindowTitle('Choose Shipper Window')
        self.setup_window_geometry()
        self.load_shipper_combo()
        self.data_frame.reload_shipper_data(self.input_all_shippers[0])

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
                         window_y_coord,
                         self.app_settings.loadconfirmationwindow_width,
                         self.app_settings.loadconfirmationwindow_height
                         )
        self.setMinimumSize(
            self.app_settings.loadconfirmationwindow_width,
            self.app_settings.loadconfirmationwindow_height
        )

    def load_shipper_combo(self):
        self.choose_shipper_combobox.addItems([
            shipper.shippername for shipper
            in self.input_all_shippers
        ])
        self.choose_shipper_combobox.setCurrentIndex(0)

    def setup_gui_object_events(self):
        self.cncl_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.accept)
        self.choose_shipper_combobox.currentIndexChanged.connect(self.shipper_combobox_action)

    def shipper_combobox_action(self, currentIndex):
        self.selected_shipper = self.input_all_shippers[currentIndex]
        self.data_frame.reload_shipper_data(self.selected_shipper)






