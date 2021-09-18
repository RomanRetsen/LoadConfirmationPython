import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
from all_persistence_class import ConsigneeRefInstance
from all_persistence_class import ShipperRefInstance


class ConsigneeFrame(qtw.QFrame):

    deleteframe_signal = qtc.pyqtSignal(ConsigneeRefInstance)

    def __init__(
            self,
            sequence_number=0,
            delete_button_bool=False,
            input_consignee_instance=None,
            input_consigneeref_instance=None
            ):
        super().__init__()
        self.setup_supporting_vars(
            sequence_number,
            delete_button_bool,
            input_consignee_instance,
            input_consigneeref_instance
            )
        self.setup_gui()

    def setup_supporting_vars(self, 
                              sequence_number,
                              delete_button_bool,
                              input_consignee_instance,
                              input_consigneeref_instance
                              ):
        self.sequence_number = sequence_number
        self.input_consignee_instance = input_consignee_instance
        self.input_consigneeref_instance = input_consigneeref_instance
        self.delete_button_bool = delete_button_bool

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.main_box = qtw.QVBoxLayout()

        self.top_frame = qtw.QFrame()
        self.data_frame = qtw.QFrame()
        self.top_framebox = qtw.QHBoxLayout()
        self.data_framebox = qtw.QGridLayout()

        self.top_label = qtw.QLabel()
        if self.delete_button_bool:
            self.delete_button = qtw.QPushButton(' Delete Consignee ')

        self.consignee_name_editline = qtw.QLineEdit()
        self.consignee_address_editline = qtw.QLineEdit()
        self.consignee_city_editline = qtw.QLineEdit()
        self.consignee_state_editline = qtw.QLineEdit()
        self.consignee_country_editline = qtw.QLineEdit()
        self.consignee_postalcode_editline = qtw.QLineEdit()
        self.consignee_phone_editline = qtw.QLineEdit()
        self.consignee_fax_editline = qtw.QLineEdit()
        self.consignee_tollfree_editline = qtw.QLineEdit()
        self.consignee_contact_editline = qtw.QLineEdit()

        self.consignee_date_editline = qtw.QDateEdit(self)
        self.consignee_time_editline = qtw.QLineEdit()

    def setup_gui_object_style_names(self):
        self.setObjectName('dataFrame')
        self.top_frame.setObjectName('spacerFrame')
        self.data_frame.setObjectName('spacerFrame')

    def layout_gui_objects(self):
        self.setLayout(self.main_box)

        self.main_box.addWidget(self.top_frame)
        self.main_box.addWidget(self.data_frame, stretch=1)

        self.top_frame.setLayout(self.top_framebox)
        self.data_frame.setLayout(self.data_framebox)

        self.top_framebox.addWidget(self.top_label, 1, alignment=qtc.Qt.AlignLeft)
        if self.delete_button_bool:
            self.top_framebox.addWidget(self.delete_button, 1, alignment=qtc.Qt.AlignRight)

        self.data_framebox.setRowStretch(0, 1)
        self.data_framebox.setRowStretch(1, 1)
        self.data_framebox.setRowStretch(2, 1)
        self.data_framebox.setRowStretch(3, 1)
        self.data_framebox.setColumnStretch(0, 1)
        self.data_framebox.setColumnStretch(1, 1)
        self.data_framebox.setColumnStretch(2, 1)
        self.data_framebox.setColumnStretch(3, 1)
        self.data_framebox.setColumnStretch(4, 1)
        self.data_framebox.setColumnStretch(5, 1)
        self.data_framebox.setColumnStretch(6, 1)
        self.data_framebox.setColumnStretch(7, 1)
        self.data_framebox.setColumnStretch(8, 1)
        self.data_framebox.setColumnStretch(9, 1)
        self.data_framebox.setColumnStretch(10, 1)
        self.data_framebox.setColumnStretch(11, 1)
        self.data_framebox.addWidget(self.consignee_name_editline, 0, 0, 1, 4)
        self.data_framebox.addWidget(self.consignee_address_editline, 1, 0, 1, 4)
        self.data_framebox.addWidget(self.consignee_city_editline, 2, 0, 1, 1)
        self.data_framebox.addWidget(self.consignee_state_editline, 2, 1, 1, 1)
        self.data_framebox.addWidget(self.consignee_country_editline, 2, 2, 1, 1)
        self.data_framebox.addWidget(self.consignee_postalcode_editline, 2, 3, 1, 1)
        self.data_framebox.addWidget(self.consignee_phone_editline, 0, 4, 1, 4)
        self.data_framebox.addWidget(self.consignee_fax_editline, 1, 4, 1, 4)
        self.data_framebox.addWidget(self.consignee_tollfree_editline, 2, 4, 1, 4)
        self.data_framebox.addWidget(self.consignee_contact_editline, 0, 8, 1, 4)
        self.data_framebox.addWidget(self.consignee_date_editline, 1, 8, 1, 4)
        self.data_framebox.addWidget(self.consignee_time_editline, 2, 8, 1, 4)

    def feature_gui_objects(self):
        self.consignee_date_editline.setCalendarPopup(True)
        self.load_top_label()
        self.load_consignee_data()
        self.disable_editing()

    def load_top_label(self):
        if self.sequence_number > 0:
            self.top_label.setText("CONSIGNEE #" + str(self.sequence_number))

    def setup_gui_object_events(self):
        self.consignee_date_editline.dateChanged.connect(self.consignee_date_changed)
        if self.delete_button_bool:
            self.delete_button.clicked.connect(self.delete_button_action)

    def disable_editing(self):
        self.consignee_name_editline.setEnabled(False)
        self.consignee_address_editline.setEnabled(False)
        self.consignee_city_editline.setEnabled(False)
        self.consignee_state_editline.setEnabled(False)
        self.consignee_country_editline.setEnabled(False)
        self.consignee_postalcode_editline.setEnabled(False)
        self.consignee_phone_editline.setEnabled(False)
        self.consignee_fax_editline.setEnabled(False)
        self.consignee_tollfree_editline.setEnabled(False)
        self.consignee_contact_editline.setEnabled(False)

    def load_consignee_data(self):
        if self.input_consignee_instance:
            self.consignee_name_editline.setText(self.input_consignee_instance.consigneename)
            self.consignee_address_editline.setText(self.input_consignee_instance.consigneeaddress)
            self.consignee_city_editline.setText(self.input_consignee_instance.consigneecity)
            self.consignee_state_editline.setText(self.input_consignee_instance.consigneestate)
            self.consignee_country_editline.setText(self.input_consignee_instance.consigneecountry)
            self.consignee_postalcode_editline.setText(self.input_consignee_instance.consigneepostalcode)
            self.consignee_phone_editline.setText(self.input_consignee_instance.consigneephone)
            self.consignee_fax_editline.setText(self.input_consignee_instance.consigneefax)
            self.consignee_tollfree_editline.setText(self.input_consignee_instance.consigneetollfree)
            self.consignee_contact_editline.setText(self.input_consignee_instance.consigneecontact)

            #loading date and time data
        if self.input_consigneeref_instance:
            self.consignee_date_editline.setDate(
                qtc.QDate(
                    self.input_consigneeref_instance.consigneedate
                ))
            self.consignee_time_editline.setText(
                self.input_consigneeref_instance.consigneetime
            )
        else:
            self.consignee_date_editline.setDate(qtc.QDate().currentDate())


    def reload_consignee_data(self, input_consignee_instance):
        self.input_consignee_instance = input_consignee_instance
        self.load_consignee_data()

    def delete_button_action(self):
        self.deleteLater()
        self.deleteframe_signal.emit(self.input_consigneeref_instance)

    def change_sequence_number(self, sequence_number):
        self.sequence_number = sequence_number
        self.load_top_label()

    def consignee_date_changed(self):
        # event is triggered on loaded data
        # and ignored on adding new shipper to load confirmatio
        if self.input_consigneeref_instance:
            self.input_consigneeref_instance.consigneedate = self.consignee_date_editline.date().toPyDate()

class ShipperFrame(qtw.QFrame):
    deleteframe_signal = qtc.pyqtSignal(ShipperRefInstance)

    def __init__(
            self,
            sequence_number=0,
            delete_button_bool=False,
            input_shipper_instance=None,
            input_shipperref_instance=None
    ):
        super().__init__()
        self.setup_supporting_vars(
            sequence_number,
            delete_button_bool,
            input_shipper_instance,
            input_shipperref_instance
        )
        self.setup_gui()

    def setup_supporting_vars(self,
                              sequence_number,
                              delete_button_bool,
                              input_shipper_instance,
                              input_shipperref_instance
                              ):
        self.sequence_number = sequence_number
        self.input_shipper_instance = input_shipper_instance
        self.input_shipperref_instance = input_shipperref_instance
        self.delete_button_bool = delete_button_bool

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.main_box = qtw.QVBoxLayout()

        self.top_frame = qtw.QFrame()
        self.data_frame = qtw.QFrame()
        self.top_framebox = qtw.QHBoxLayout()
        self.data_framebox = qtw.QGridLayout()

        self.top_label = qtw.QLabel()
        if self.delete_button_bool:
            self.delete_button = qtw.QPushButton(' Delete Shipper ')

        self.shipper_name_editline = qtw.QLineEdit()
        self.shipper_address_editline = qtw.QLineEdit()
        self.shipper_city_editline = qtw.QLineEdit()
        self.shipper_state_editline = qtw.QLineEdit()
        self.shipper_country_editline = qtw.QLineEdit()
        self.shipper_postalcode_editline = qtw.QLineEdit()
        self.shipper_phone_editline = qtw.QLineEdit()
        self.shipper_fax_editline = qtw.QLineEdit()
        self.shipper_tollfree_editline = qtw.QLineEdit()
        self.shipper_contact_editline = qtw.QLineEdit()

        self.shipper_date_editline = qtw.QDateEdit(self)
        self.shipper_time_editline = qtw.QLineEdit()

    def setup_gui_object_style_names(self):
        self.setObjectName('dataFrame')
        self.top_frame.setObjectName('spacerFrame')
        self.data_frame.setObjectName('spacerFrame')

    def layout_gui_objects(self):
        self.setLayout(self.main_box)

        self.main_box.addWidget(self.top_frame)
        self.main_box.addWidget(self.data_frame, stretch=1)

        self.top_frame.setLayout(self.top_framebox)
        self.data_frame.setLayout(self.data_framebox)

        self.top_framebox.addWidget(self.top_label, 1, alignment=qtc.Qt.AlignLeft)
        if self.delete_button_bool:
            self.top_framebox.addWidget(self.delete_button, 1, alignment=qtc.Qt.AlignRight)

        self.data_framebox.setRowStretch(0, 1)
        self.data_framebox.setRowStretch(1, 1)
        self.data_framebox.setRowStretch(2, 1)
        self.data_framebox.setRowStretch(3, 1)
        self.data_framebox.setColumnStretch(0, 1)
        self.data_framebox.setColumnStretch(1, 1)
        self.data_framebox.setColumnStretch(2, 1)
        self.data_framebox.setColumnStretch(3, 1)
        self.data_framebox.setColumnStretch(4, 1)
        self.data_framebox.setColumnStretch(5, 1)
        self.data_framebox.setColumnStretch(6, 1)
        self.data_framebox.setColumnStretch(7, 1)
        self.data_framebox.setColumnStretch(8, 1)
        self.data_framebox.setColumnStretch(9, 1)
        self.data_framebox.setColumnStretch(10, 1)
        self.data_framebox.setColumnStretch(11, 1)
        self.data_framebox.addWidget(self.shipper_name_editline, 0, 0, 1, 4)
        self.data_framebox.addWidget(self.shipper_address_editline, 1, 0, 1, 4)
        self.data_framebox.addWidget(self.shipper_city_editline, 2, 0, 1, 1)
        self.data_framebox.addWidget(self.shipper_state_editline, 2, 1, 1, 1)
        self.data_framebox.addWidget(self.shipper_country_editline, 2, 2, 1, 1)
        self.data_framebox.addWidget(self.shipper_postalcode_editline, 2, 3, 1, 1)
        self.data_framebox.addWidget(self.shipper_phone_editline, 0, 4, 1, 4)
        self.data_framebox.addWidget(self.shipper_fax_editline, 1, 4, 1, 4)
        self.data_framebox.addWidget(self.shipper_tollfree_editline, 2, 4, 1, 4)
        self.data_framebox.addWidget(self.shipper_contact_editline, 0, 8, 1, 4)
        self.data_framebox.addWidget(self.shipper_date_editline, 1, 8, 1, 4)
        self.data_framebox.addWidget(self.shipper_time_editline, 2, 8, 1, 4)

    def feature_gui_objects(self):
        self.shipper_date_editline.setCalendarPopup(True)
        self.load_top_label()
        self.load_shipper_data()
        self.disable_editing()

    def load_top_label(self):
        if self.sequence_number > 0:
            self.top_label.setText("SHIPPER #" + str(self.sequence_number))

    def setup_gui_object_events(self):
        self.shipper_date_editline.dateChanged.connect(self.shipper_date_changed)
        if self.delete_button_bool:
            self.delete_button.clicked.connect(self.delete_button_action)

    def disable_editing(self):
        self.shipper_name_editline.setEnabled(False)
        self.shipper_address_editline.setEnabled(False)
        self.shipper_city_editline.setEnabled(False)
        self.shipper_state_editline.setEnabled(False)
        self.shipper_country_editline.setEnabled(False)
        self.shipper_postalcode_editline.setEnabled(False)
        self.shipper_phone_editline.setEnabled(False)
        self.shipper_fax_editline.setEnabled(False)
        self.shipper_tollfree_editline.setEnabled(False)
        self.shipper_contact_editline.setEnabled(False)

    def load_shipper_data(self):
        if self.input_shipper_instance:
            self.shipper_name_editline.setText(self.input_shipper_instance.shippername)
            self.shipper_address_editline.setText(self.input_shipper_instance.shipperaddress)
            self.shipper_city_editline.setText(self.input_shipper_instance.shippercity)
            self.shipper_state_editline.setText(self.input_shipper_instance.shipperstate)
            self.shipper_country_editline.setText(self.input_shipper_instance.shippercountry)
            self.shipper_postalcode_editline.setText(self.input_shipper_instance.shipperpostalcode)
            self.shipper_phone_editline.setText(self.input_shipper_instance.shipperphone)
            self.shipper_fax_editline.setText(self.input_shipper_instance.shipperfax)
            self.shipper_tollfree_editline.setText(self.input_shipper_instance.shippertollfree)
            self.shipper_contact_editline.setText(self.input_shipper_instance.shippercontact)

        if self.input_shipperref_instance:
            self.shipper_date_editline.setDate(
                qtc.QDate(
                    self.input_shipperref_instance.shipperdate
                    ))
            self.shipper_time_editline.setText(
                self.input_shipperref_instance.shippertime
                )
        else:
            self.shipper_date_editline.setDate(qtc.QDate().currentDate())

    def reload_shipper_data(self, input_shipper_instance):
        self.input_shipper_instance = input_shipper_instance
        self.load_shipper_data()

    def delete_button_action(self):
        self.deleteLater()
        self.deleteframe_signal.emit(self.input_shipperref_instance)

    def change_sequence_number(self, sequence_number):
        self.sequence_number = sequence_number
        self.load_top_label()

    def shipper_date_changed(self):
        # event is triggered on loaded data
        # and ignored on adding new shipper to load confirmation
        if self.input_shipperref_instance:
            self.input_shipperref_instance.shipperdate = self.shipper_date_editline.date().toPyDate()


class CarrierFrame(qtw.QFrame):

    def __init__(self,delete_button_bool=False, input_carrier_instance=None):
        super().__init__()
        self.setup_supporting_vars(delete_button_bool, input_carrier_instance)
        self.setup_gui()

    def setup_supporting_vars(self,delete_button_bool, input_carrier_instance):
        self.input_carrier_instance = input_carrier_instance
        self.delete_button_bool = delete_button_bool

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.main_box = qtw.QVBoxLayout()

        self.top_frame = qtw.QFrame()
        self.data_frame = qtw.QFrame()
        self.top_framebox = qtw.QHBoxLayout()
        self.data_framebox = qtw.QGridLayout()

        self.top_label = qtw.QLabel("CARRIER")
        if self.delete_button_bool:
            self.delete_button = qtw.QPushButton(' Delete Carrier ')

        self.carrier_name_editline = qtw.QLineEdit()
        self.carrier_address_editline = qtw.QLineEdit()
        self.carrier_city_editline = qtw.QLineEdit()
        self.carrier_state_editline = qtw.QLineEdit()
        self.carrier_country_editline = qtw.QLineEdit()
        self.carrier_postalcode_editline = qtw.QLineEdit()
        self.carrier_phone_editline = qtw.QLineEdit()
        self.carrier_fax_editline = qtw.QLineEdit()
        self.carrier_tollfree_editline = qtw.QLineEdit()
        self.carrier_contact_editline = qtw.QLineEdit()

    def setup_gui_object_style_names(self):
        self.setObjectName('dataFrame')
        self.top_frame.setObjectName('spacerFrame')
        self.data_frame.setObjectName('spacerFrame')

    def layout_gui_objects(self):
        self.setLayout(self.main_box)

        self.main_box.addWidget(self.top_frame)
        self.main_box.addWidget(self.data_frame, stretch=1)

        self.top_frame.setLayout(self.top_framebox)
        self.data_frame.setLayout(self.data_framebox)

        self.top_framebox.addWidget(self.top_label, 1, alignment=qtc.Qt.AlignLeft)
        if self.delete_button_bool:
            self.top_framebox.addWidget(self.delete_button, 1, alignment=qtc.Qt.AlignRight)

        self.data_framebox.setRowStretch(0, 1)
        self.data_framebox.setRowStretch(1, 1)
        self.data_framebox.setRowStretch(2, 1)
        self.data_framebox.setRowStretch(3, 1)
        self.data_framebox.setColumnStretch(0, 1)
        self.data_framebox.setColumnStretch(1, 1)
        self.data_framebox.setColumnStretch(2, 1)
        self.data_framebox.setColumnStretch(3, 1)
        self.data_framebox.setColumnStretch(4, 1)
        self.data_framebox.setColumnStretch(5, 1)
        self.data_framebox.setColumnStretch(6, 1)
        self.data_framebox.setColumnStretch(7, 1)
        self.data_framebox.setColumnStretch(8, 1)
        self.data_framebox.setColumnStretch(9, 1)
        self.data_framebox.setColumnStretch(10, 1)
        self.data_framebox.setColumnStretch(11, 1)
        self.data_framebox.addWidget(self.carrier_name_editline, 0, 0, 1, 4)
        self.data_framebox.addWidget(self.carrier_address_editline, 1, 0, 1, 4)
        self.data_framebox.addWidget(self.carrier_city_editline, 2, 0, 1, 1)
        self.data_framebox.addWidget(self.carrier_state_editline, 2, 1, 1, 1)
        self.data_framebox.addWidget(self.carrier_country_editline, 2, 2, 1, 1)
        self.data_framebox.addWidget(self.carrier_postalcode_editline, 2, 3, 1, 1)
        self.data_framebox.addWidget(self.carrier_phone_editline, 0, 4, 1, 4)
        self.data_framebox.addWidget(self.carrier_fax_editline, 1, 4, 1, 4)
        self.data_framebox.addWidget(self.carrier_tollfree_editline, 2, 4, 1, 4)
        self.data_framebox.addWidget(self.carrier_contact_editline, 0, 8, 1, 4)

    def feature_gui_objects(self):
        self.load_carrier_data()
        self.disable_editing()

    def setup_gui_object_events(self):
        if self.delete_button_bool:
            self.delete_button.clicked.connect(self.delete_button_action)

    def disable_editing(self):
        self.carrier_name_editline.setEnabled(False)
        self.carrier_address_editline.setEnabled(False)
        self.carrier_city_editline.setEnabled(False)
        self.carrier_state_editline.setEnabled(False)
        self.carrier_country_editline.setEnabled(False)
        self.carrier_postalcode_editline.setEnabled(False)
        self.carrier_phone_editline.setEnabled(False)
        self.carrier_fax_editline.setEnabled(False)
        self.carrier_tollfree_editline.setEnabled(False)
        self.carrier_contact_editline.setEnabled(False)

    def load_carrier_data(self):
        if self.input_carrier_instance is not None:
            self.carrier_name_editline.setText(self.input_carrier_instance.carriername)
            self.carrier_address_editline.setText(self.input_carrier_instance.carrieraddress)
            self.carrier_city_editline.setText(self.input_carrier_instance.carriercity)
            self.carrier_state_editline.setText(self.input_carrier_instance.carrierstate)
            self.carrier_country_editline.setText(self.input_carrier_instance.carriercountry)
            self.carrier_postalcode_editline.setText(self.input_carrier_instance.carrierpostalcode)
            self.carrier_phone_editline.setText(self.input_carrier_instance.carrierphone)
            self.carrier_fax_editline.setText(self.input_carrier_instance.carrierfax)
            self.carrier_tollfree_editline.setText(self.input_carrier_instance.carriertollfree)
            self.carrier_contact_editline.setText(self.input_carrier_instance.carriercontact)

    def reload_carrier_data(self, input_carrier_instance):
        self.input_carrier_instance = input_carrier_instance
        self.load_carrier_data()

    def delete_button_action(self):
        self.deleteLater()

class BrokerFrame(qtw.QFrame):

    def __init__(self,delete_button_bool=False, input_broker_instance=None):
        super().__init__()
        self.setup_supporting_vars(delete_button_bool, input_broker_instance)
        self.setup_gui()

    def setup_supporting_vars(self, delete_button_bool, input_broker_instance):
        self.input_broker_instance = input_broker_instance
        self.delete_button_bool = delete_button_bool

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.main_box = qtw.QVBoxLayout()

        self.top_frame = qtw.QFrame()
        self.data_frame = qtw.QFrame()
        self.top_framebox = qtw.QHBoxLayout()
        self.data_framebox = qtw.QGridLayout()

        self.top_label = qtw.QLabel("CUSTOM BROKER")
        if self.delete_button_bool:
            self.delete_button = qtw.QPushButton(' Delete Broker ')

        self.broker_name_editline = qtw.QLineEdit()
        self.broker_contact_editline = qtw.QLineEdit()
        self.broker_phone_editline = qtw.QLineEdit()
        self.broker_fax_editline = qtw.QLineEdit()
        self.broker_tollfree_editline = qtw.QLineEdit()

    def setup_gui_object_style_names(self):
        self.setObjectName('dataFrame')
        self.top_frame.setObjectName('spacerFrame')
        self.data_frame.setObjectName('spacerFrame')

    def layout_gui_objects(self):
        self.setLayout(self.main_box)

        self.main_box.addWidget(self.top_frame)
        self.main_box.addWidget(self.data_frame, stretch=1)

        self.top_frame.setLayout(self.top_framebox)
        self.data_frame.setLayout(self.data_framebox)

        self.top_framebox.addWidget(self.top_label, 1, alignment=qtc.Qt.AlignLeft)
        if self.delete_button_bool:
            self.top_framebox.addWidget(self.delete_button, 1, alignment=qtc.Qt.AlignRight)

        self.data_framebox.setRowStretch(0, 1)
        self.data_framebox.setRowStretch(1, 1)
        self.data_framebox.setRowStretch(2, 1)
        self.data_framebox.setColumnStretch(0, 1)
        self.data_framebox.setColumnStretch(1, 1)
        self.data_framebox.setColumnStretch(2, 1)
        self.data_framebox.addWidget(self.broker_name_editline, 0, 0, 1, 1)
        self.data_framebox.addWidget(self.broker_contact_editline, 1, 0, 1, 1)
        self.data_framebox.addWidget(self.broker_phone_editline, 0, 1, 1, 1)
        self.data_framebox.addWidget(self.broker_fax_editline, 1, 1, 1, 1)
        self.data_framebox.addWidget(self.broker_tollfree_editline, 0, 2, 1, 1)

    def feature_gui_objects(self):
        self.load_broker_data()
        self.disable_editing()

    def setup_gui_object_events(self):
        if self.delete_button_bool:
            self.delete_button.clicked.connect(self.delete_button_action)

    def disable_editing(self):
        self.broker_name_editline.setEnabled(False)
        self.broker_phone_editline.setEnabled(False)
        self.broker_fax_editline.setEnabled(False)
        self.broker_tollfree_editline.setEnabled(False)
        self.broker_contact_editline.setEnabled(False)

    def load_broker_data(self):
        if self.input_broker_instance is not None:
            self.broker_name_editline.setText(self.input_broker_instance.custombrokername)
            self.broker_phone_editline.setText(self.input_broker_instance.custombrokerphone)
            self.broker_fax_editline.setText(self.input_broker_instance.custombrokerfax)
            self.broker_tollfree_editline.setText(self.input_broker_instance.custombrokertollfree)
            self.broker_contact_editline.setText(self.input_broker_instance.custombrokercontact)

    def reload_broker_data(self, input_broker_instance):
        self.input_broker_instance = input_broker_instance
        self.load_broker_data()

    def delete_button_action(self):
        self.deleteLater()
