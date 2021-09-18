"""This module contains all QWidget classes that are used as MDIChildWindows for the main MDIWindow

These are: BrokerWidget, CarrierWidget, ConsigneeWeidget, CurrencyWidget,
            LoadConfirmationWidget, LoadTypeWidget, ShipperWidget
"""
import loadconfirmation_settings as LCSettings
from core.workers.allworkers import (BrokerWorker, CarrierWorker, ConsigneeWorker,
                                     CurrencyWorker, LoadConfirmationsWorker, LoadTypeWorker,
                                     ShipperWorker, UsersWorker)
from core.workers.allqueries import (BrokerQueries, CarrierQueries, ConsigneeQueries,
                                     CurrencyQueries, LoadConfirmationsQueries, LoadTypeQueries,
                                     ShipperQueries, UsersQueries)
from core.newdialog.alldialogs import (NewBrokerDialog, NewCarrierDialog, NewConsigneeDialog,
                                       NewCurrencyDialog, NewLoadConfirmationDialog, NewLoadTypeDialog,
                                       NewShipperDialog, NewUserDialog, NewPasswordDialog)
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
from all_persistence_class import (BrokerInstance, CarrierInstance, ConsigneeInstance,
                                   CurrencyInstance, LoadConfirmationInstance, LoadTypeInstance,
                                   ShipperInstance, UserInstance)

class BrokerWidget(qtw.QWidget):

    def __init__(self, app_settings, app_connection):
        super().__init__()
        # create "load from json" function for Settings class
        # self.app_connection = self.assembleConnection(self.app_settings)
        self.setup_supporting_vars(app_settings, app_connection)
        self.setup_gui()
        self.show()
        self.activate_worker()

    def setup_supporting_vars(self, app_settings, app_connection):
        self.app_settings = app_settings
        self.app_connection = app_connection
        self.broker_worker = BrokerWorker(self.app_connection)
        self.broker_queries = BrokerQueries(self.app_connection)

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.vertical_lo = qtw.QVBoxLayout()
        self.broker_table = qtw.QTableWidget()
        self.progress_bar = qtw.QProgressBar()
        self.statusbar = qtw.QStatusBar()
        self.create_menus()

    def setup_gui_object_style_names(self):
        self.statusbar.setProperty('Error', False)
        self.statusbar.setStyle(self.statusbar.style())

    def layout_gui_objects(self):
        self.vertical_lo.addWidget(self.toolbar)
        self.vertical_lo.addWidget(self.broker_table)
        self.vertical_lo.addWidget(self.progress_bar)
        self.vertical_lo.addWidget(self.statusbar)
        self.setLayout(self.vertical_lo)

    def feature_gui_objects(self):
        self.setGeometry(0, 0, self.app_settings.subwindow_width, self.app_settings.subwindow_height)
        self.setMinimumSize(600, 250)
        #dressing up table
        self.broker_table.setColumnCount(6)
        self.broker_table.setColumnHidden(0, True)
        self.broker_table.setEditTriggers(qtw.QTableWidget.NoEditTriggers)
        self.broker_table.setSelectionMode(qtw.QAbstractItemView.SingleSelection)
        self.broker_table.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)
        # self.broker_table.selectRow(0)
        self.broker_table.setHorizontalHeaderLabels(["Brokers Id", "Brokers Name", "Phone",
                                                    "Fax", "Brokers Name", "Contact"
                                                    ])
        header = self.broker_table.horizontalHeader()
        header.setSectionResizeMode(0, qtw.QHeaderView.Fixed)
        header.setSectionResizeMode(1, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(2, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(3, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(4, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(5, qtw.QHeaderView.Stretch)
        #  settings up progress bar
        self.progress_bar.setValue(0)
        brokers_count = self.broker_queries.brokers_count()
        if brokers_count != 0:
            self.progress_bar.setRange(0, brokers_count)
        else:
            self.progress_bar.setRange(0, 1)
        self.statusbar.showMessage('...')


    def setup_gui_object_events(self):
        self.create_menu_actions()
        self.broker_table.cellDoubleClicked.connect(self.view_broker_window)

    def activate_controls(self):
        self.delete_action.setEnabled(True)
        self.insert_action.setEnabled(True)
        self.modify_action.setEnabled(True)
        self.view_action.setEnabled(True)
        self.refresh_action.setEnabled(True)

    def deactivate_controls(self):
        self.delete_action.setEnabled(False)
        self.insert_action.setEnabled(False)
        self.modify_action.setEnabled(False)
        self.view_action.setEnabled(False)
        self.refresh_action.setEnabled(False)

    def activate_worker(self):
        self.broker_worker.update_windowmessage_signal.connect(self.update_status_bar)
        self.broker_queries.update_windowmessage_signal.connect(self.update_status_bar)
        self.broker_worker.update_progressbar_signal.connect(self.update_progress_bar)
        self.broker_worker.update_nextrow_signal.connect(self.add_row_to_table)
        self.broker_worker.start()

    def update_status_bar(self, code, message):
        if code == 100000:
            self.statusbar.setProperty('Error', False)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(message)
            self.broker_table.setCurrentCell(0, 0)
            self.refresh_action.setEnabled(True)
        elif code == 100001 or code == 100002:
            self.statusbar.setProperty('Error', False)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(message)
        else:
            self.statusbar.setProperty('Error', True)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(f'Error code: {code}. Error message: {message}')

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def add_row_to_table(self, broker_instance):
        row_number = self.broker_table.rowCount()
        self.broker_table.insertRow(row_number)
        self.fill_row_with_data(row_number, broker_instance)

    def add_row_topof_table(self, broker_instance):
        self.broker_table.insertRow(0)
        self.fill_row_with_data(0, broker_instance)
        self.broker_table.setCurrentCell(0, 0)

    def fill_row_with_data(self, row_number, broker_instance):
        inserteditemid = qtw.QTableWidgetItem()
        inserteditemid.setData(qtc.Qt.DisplayRole, broker_instance.custombrokerid)
        inserteditemid.setTextAlignment(qtc.Qt.AlignCenter)
        self.broker_table.setItem(row_number, 0, inserteditemid)

        inserteditemname = qtw.QTableWidgetItem()
        inserteditemname.setData(qtc.Qt.DisplayRole, broker_instance.custombrokername)
        inserteditemname.setTextAlignment(qtc.Qt.AlignCenter)
        self.broker_table.setItem(row_number, 1, inserteditemname)

        inserteditemphone = qtw.QTableWidgetItem()
        inserteditemphone.setData(qtc.Qt.DisplayRole, broker_instance.custombrokerphone)
        inserteditemphone.setTextAlignment(qtc.Qt.AlignCenter)
        self.broker_table.setItem(row_number, 2, inserteditemphone)

        inserteditemfax = qtw.QTableWidgetItem()
        inserteditemfax.setData(qtc.Qt.DisplayRole, broker_instance.custombrokerfax)
        inserteditemfax.setTextAlignment(qtc.Qt.AlignCenter)
        self.broker_table.setItem(row_number, 3, inserteditemfax)

        inserteditemtollfree = qtw.QTableWidgetItem()
        inserteditemtollfree.setData(qtc.Qt.DisplayRole, broker_instance.custombrokertollfree)
        inserteditemtollfree.setTextAlignment(qtc.Qt.AlignCenter)
        self.broker_table.setItem(row_number, 4, inserteditemtollfree)

        inserteditemcontact = qtw.QTableWidgetItem()
        inserteditemcontact.setData(qtc.Qt.DisplayRole, broker_instance.custombrokercontact)
        inserteditemcontact.setTextAlignment(qtc.Qt.AlignCenter)
        self.broker_table.setItem(row_number, 5, inserteditemcontact)


    def create_menus(self):
        menubar = qtw.QMenuBar()
        self.toolbar = qtw.QToolBar()
        self.toolbar.setFixedHeight(55)
        self.toolbar.setIconSize(qtc.QSize(50, 50))
        self.file_menu = menubar.addMenu('File')
        self.operation_menu = menubar.addMenu('Operation')
        self.vertical_lo.setMenuBar(menubar)

    def create_menu_actions(self):
        self.exit_action = qtw.QAction(
            (qtg.QIcon(':/icon_exit.png')),
            'Exit', self
        )
        self.delete_action = qtw.QAction(
            (qtg.QIcon(':/icon_delete.png')),
            'Delete Load Confirmation', self
        )
        self.insert_action = qtw.QAction(
            (qtg.QIcon(':/icon_insert.png')),
            'Insert Load Confirmation', self
        )
        self.modify_action = qtw.QAction(
            (qtg.QIcon(':/icon_modify.png')),
            'Modify Load Confirmation', self
        )
        self.view_action = qtw.QAction(
            (qtg.QIcon(':/icon_view.png')),
            'View Load Confirmation', self
        )
        self.refresh_action = qtw.QAction(
            (qtg.QIcon(':/icon_refresh.png')),
            'Refresh Table', self
        )
        self.refresh_action.setEnabled(False)
        self.exit_action.triggered.connect(self.close_window)
        self.delete_action.triggered.connect(self.delete_broker_window)
        self.insert_action.triggered.connect(self.insert_broker_window)
        self.modify_action.triggered.connect(self.modify_broker_window)
        self.view_action.triggered.connect(self.view_broker_window)
        self.refresh_action.triggered.connect(self.refresh_broker_window)
        self.file_menu.addAction(self.exit_action)
        self.operation_menu.addAction(self.delete_action)
        self.operation_menu.addAction(self.insert_action)
        self.operation_menu.addAction(self.modify_action)
        self.operation_menu.addAction(self.view_action)
        self.toolbar.addAction(self.exit_action)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.delete_action)
        self.toolbar.addAction(self.insert_action)
        self.toolbar.addAction(self.modify_action)
        self.toolbar.addAction(self.view_action)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.refresh_action)

    def close_window(self):
        self.parentWidget().close()

    def delete_broker_window(self):
        selected_row = self.broker_table.currentRow()
        if selectedIDItem := self.broker_table.item(selected_row, 0):
            requested_broker= self.broker_queries.get_broker_by_id(selectedIDItem.text())
            if isinstance(requested_broker, BrokerInstance):
                delete_broker_window = NewBrokerDialog(
                    self.app_settings, LCSettings.Settings.DELETE, requested_broker
                )
                if delete_broker_window.exec_() == qtw.QDialog.Accepted:
                    operation_returm_code = self.broker_queries.delete_broker(requested_broker)
                    if operation_returm_code == 0:
                        qtw.QMessageBox(
                            qtw.QMessageBox.Information,
                            "Success", "Broker was deleted",
                            qtw.QMessageBox.Yes
                        ).exec_()
                        self.broker_table.removeRow(selected_row)
                        self.select_nearby_row(selected_row)
                else:
                    print('cancel')
            else:
                self.broker_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                # self.statusbar.showMessage('Error code: -1. Error message: None selected row')
                #logging this error event

    def insert_broker_window(self):
        insert_broker_window = NewBrokerDialog(
            self.app_settings, LCSettings.Settings.INSERT, broker_queries=self.broker_queries
        )
        if insert_broker_window.exec_() == qtw.QDialog.Accepted:
            self.add_row_topof_table(insert_broker_window.new_broker_instance)
        else:
            print('cancel')


    def modify_broker_window(self):
        selected_row = self.broker_table.currentRow()
        if selectedIDItem := self.broker_table.item(selected_row, 0):
            requested_broker = self.broker_queries.get_broker_by_id(selectedIDItem.text())
            if isinstance(requested_broker, BrokerInstance):
                modify_broker_window = NewBrokerDialog(
                    self.app_settings, LCSettings.Settings.MODIFY, requested_broker, self.broker_queries
                )
                if modify_broker_window.exec_() == qtw.QDialog.Accepted:
                    self.fill_row_with_data(selected_row, modify_broker_window.modify_broker_instance)
                else:
                    print('cancel')
            else:
                self.broker_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                #logging this error eve

    def view_broker_window(self):
        selected_row = self.broker_table.currentRow()
        if selectedIDItem := self.broker_table.item(selected_row, 0):
            requested_broker = self.broker_queries.get_broker_by_id(selectedIDItem.text())
            if isinstance(requested_broker, BrokerInstance):
                view_broker_window = NewBrokerDialog(
                    self.app_settings, LCSettings.Settings.VIEW, requested_broker
                )
                if view_broker_window.exec_() == qtw.QDialog.Accepted:
                    pass
                else:
                    pass
            else:
                self.broker_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                #logging this error event

    def refresh_broker_window(self):
        if self.broker_worker.isRunning():
            self.broker_worker.quit()
            self.broker_table.setRowCount(0)
            self.broker_worker.start()
        else:
            self.broker_table.setRowCount(0)
            self.broker_worker.start()

    def select_nearby_row(self, delete_row):
        row_count = self.broker_table.rowCount()
        if row_count != 0:
            if delete_row == row_count:
                self.broker_table.setCurrentCell(delete_row - 1, 0)
            else:
                self.broker_table.setCurrentCell(delete_row, 0)


class CarrierWidget(qtw.QWidget):

    def __init__(self, app_settings, app_connection):
        super().__init__()
        # create "load from json" function for Settings class
        # self.app_connection = self.assembleConnection(self.app_settings)
        self.setup_supporting_vars(app_settings, app_connection)
        self.setup_gui()
        self.show()
        self.activate_worker()

    def setup_supporting_vars(self, app_settings, app_connection):
        self.app_settings = app_settings
        self.app_connection = app_connection
        self.carrier_worker = CarrierWorker(self.app_connection)
        self.carrier_queries = CarrierQueries(self.app_connection)

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.vertical_lo = qtw.QVBoxLayout()
        self.carrier_table = qtw.QTableWidget()
        self.progress_bar = qtw.QProgressBar()
        self.statusbar = qtw.QStatusBar()
        self.create_menus()

    def setup_gui_object_style_names(self):
        self.statusbar.setProperty('Error', False)
        self.statusbar.setStyle(self.statusbar.style())

    def layout_gui_objects(self):
        self.vertical_lo.addWidget(self.toolbar)
        self.vertical_lo.addWidget(self.carrier_table)
        self.vertical_lo.addWidget(self.progress_bar)
        self.vertical_lo.addWidget(self.statusbar)
        self.setLayout(self.vertical_lo)

    def feature_gui_objects(self):
        self.setGeometry(0, 0, self.app_settings.subwindow_width, self.app_settings.subwindow_height)
        self.setMinimumSize(600, 250)
        #dressing up table
        self.carrier_table.setColumnCount(11)
        self.carrier_table.setColumnHidden(0, True)
        self.carrier_table.setEditTriggers(qtw.QTableWidget.NoEditTriggers)
        self.carrier_table.setSelectionMode(qtw.QAbstractItemView.SingleSelection)
        self.carrier_table.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)
        self.carrier_table.selectRow(0)
        # self.usersTable.setCurrentItem(self.loadsTable.item(0, 0))
        self.carrier_table.setHorizontalHeaderLabels([
            "Carrier ID","Carrier Name", "Address", "City",
            "State", "Country", "Postal Code",
            "Phone", "Fax", "Toll Free Phone",
            "Carrier Contact"
        ])
        header = self.carrier_table.horizontalHeader()
        header.setSectionResizeMode(0, qtw.QHeaderView.Fixed)
        header.setSectionResizeMode(1, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(2, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(3, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(4, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(5, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(6, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(7, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(8, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(9, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(10, qtw.QHeaderView.Stretch)
        #  settings up progress bar
        self.progress_bar.setValue(0)
        carrier_count = self.carrier_queries.carriers_count()
        if carrier_count != 0:
            self.progress_bar.setRange(0, carrier_count)
        else:
            self.progress_bar.setRange(0, 1)
        self.statusbar.showMessage('...')

    def setup_gui_object_events(self):
        self.create_menu_actions()
        self.carrier_table.cellDoubleClicked.connect(self.view_carrier_window)

    def activate_controls(self):
        self.delete_action.setEnabled(True)
        self.insert_action.setEnabled(True)
        self.modify_action.setEnabled(True)
        self.view_action.setEnabled(True)
        self.refresh_action.setEnabled(True)

    def deactivate_controls(self):
        self.delete_action.setEnabled(False)
        self.insert_action.setEnabled(False)
        self.modify_action.setEnabled(False)
        self.view_action.setEnabled(False)
        self.refresh_action.setEnabled(False)

    def activate_worker(self):
        self.carrier_queries.update_windowmessage_signal.connect(self.update_status_bar)
        self.carrier_worker.update_windowmessage_signal.connect(self.update_status_bar)
        self.carrier_worker.update_progressbar_signal.connect(self.update_progress_bar)
        self.carrier_worker.update_nextrow_signal.connect(self.add_row_to_table)
        self.carrier_worker.start()

    def update_status_bar(self, code, message):
        #code 100000 called when table was completely fetched
        if code == 100000:
            self.statusbar.setProperty('Error', False)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(message)
            self.carrier_table.setCurrentCell(0, 0)
            self.refresh_action.setEnabled(True)
        elif code == 100001 or code == 100002:
            self.statusbar.setProperty('Error', False)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(message)
        else:
            self.statusbar.setProperty('Error', True)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(f'Error code: {code}. Error message: {message}')

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def add_row_to_table(self, carrier_instance):
        row_number = self.carrier_table.rowCount()
        self.carrier_table.insertRow(row_number)
        self.fill_row_with_data(row_number, carrier_instance)

    def add_row_topof_table(self, carrier_instance):
        self.carrier_table.insertRow(0)
        self.fill_row_with_data(0, carrier_instance)
        self.carrier_table.setCurrentCell(0, 0)

    def fill_row_with_data(self, row_number, carrier_instance):
        inserteditemid = qtw.QTableWidgetItem()
        inserteditemid.setData(qtc.Qt.DisplayRole, carrier_instance.carrierid)
        inserteditemid.setTextAlignment(qtc.Qt.AlignCenter)
        self.carrier_table.setItem(row_number, 0, inserteditemid)

        inserteditemname = qtw.QTableWidgetItem()
        inserteditemname.setData(qtc.Qt.DisplayRole, carrier_instance.carriername)
        inserteditemname.setTextAlignment(qtc.Qt.AlignCenter)
        self.carrier_table.setItem(row_number, 1, inserteditemname)

        inserteditemaddress = qtw.QTableWidgetItem()
        inserteditemaddress.setData(qtc.Qt.DisplayRole, carrier_instance.carrieraddress)
        inserteditemaddress.setTextAlignment(qtc.Qt.AlignCenter)
        self.carrier_table.setItem(row_number, 2, inserteditemaddress)

        inserteditemcity = qtw.QTableWidgetItem()
        inserteditemcity.setData(qtc.Qt.DisplayRole, carrier_instance.carriercity)
        inserteditemcity.setTextAlignment(qtc.Qt.AlignCenter)
        self.carrier_table.setItem(row_number, 3, inserteditemcity)

        inserteditemstate = qtw.QTableWidgetItem()
        inserteditemstate.setData(qtc.Qt.DisplayRole, carrier_instance.carrierstate)
        inserteditemstate.setTextAlignment(qtc.Qt.AlignCenter)
        self.carrier_table.setItem(row_number, 4, inserteditemstate)

        inserteditemcountry = qtw.QTableWidgetItem()
        inserteditemcountry.setData(qtc.Qt.DisplayRole, carrier_instance.carriercountry)
        inserteditemcountry.setTextAlignment(qtc.Qt.AlignCenter)
        self.carrier_table.setItem(row_number, 5, inserteditemcountry)

        inserteditempostalcode = qtw.QTableWidgetItem()
        inserteditempostalcode.setData(qtc.Qt.DisplayRole, carrier_instance.carrierpostalcode)
        inserteditempostalcode.setTextAlignment(qtc.Qt.AlignCenter)
        self.carrier_table.setItem(row_number, 6, inserteditempostalcode)

        inserteditemphone = qtw.QTableWidgetItem()
        inserteditemphone.setData(qtc.Qt.DisplayRole, carrier_instance.carrierphone)
        inserteditemphone.setTextAlignment(qtc.Qt.AlignCenter)
        self.carrier_table.setItem(row_number, 7, inserteditemphone)

        inserteditemfax = qtw.QTableWidgetItem()
        inserteditemfax.setData(qtc.Qt.DisplayRole, carrier_instance.carrierfax)
        inserteditemfax.setTextAlignment(qtc.Qt.AlignCenter)
        self.carrier_table.setItem(row_number, 8, inserteditemfax)

        inserteditemtollfree = qtw.QTableWidgetItem()
        inserteditemtollfree.setData(qtc.Qt.DisplayRole, carrier_instance.carriertollfree)
        inserteditemtollfree.setTextAlignment(qtc.Qt.AlignCenter)
        self.carrier_table.setItem(row_number, 9, inserteditemtollfree)

        inserteditemcontact = qtw.QTableWidgetItem()
        inserteditemcontact.setData(qtc.Qt.DisplayRole, carrier_instance.carriercontact)
        inserteditemcontact.setTextAlignment(qtc.Qt.AlignCenter)
        self.carrier_table.setItem(row_number, 10, inserteditemcontact)

    def create_menus(self):
        menubar = qtw.QMenuBar()
        self.toolbar = qtw.QToolBar()
        self.toolbar.setFixedHeight(55)
        self.toolbar.setIconSize(qtc.QSize(50, 50))
        self.file_menu = menubar.addMenu('File')
        self.operation_menu = menubar.addMenu('Operation')
        self.vertical_lo.setMenuBar(menubar)

    def create_menu_actions(self):
        self.exit_action = qtw.QAction(
            (qtg.QIcon(':/icon_exit')),
            'Exit', self
        )
        self.delete_action = qtw.QAction(
            (qtg.QIcon(':/icon_delete.png')),
            'Delete Load Confirmation', self
        )
        self.insert_action = qtw.QAction(
            (qtg.QIcon(':/icon_insert.png')),
            'Insert Load Confirmation', self
        )
        self.modify_action = qtw.QAction(
            (qtg.QIcon(':/icon_modify.png')),
            'Modify Load Confirmation', self
        )
        self.view_action = qtw.QAction(
            (qtg.QIcon(':/icon_view.png')),
            'View Load Confirmation', self
        )
        self.refresh_action = qtw.QAction(
            (qtg.QIcon(':/icon_refresh.png')),
            'Refresh Table', self
        )
        self.refresh_action.setEnabled(False)
        self.exit_action.triggered.connect(self.close_window)
        self.delete_action.triggered.connect(self.delete_carrier_window)
        self.insert_action.triggered.connect(self.insert_carrier_window)
        self.modify_action.triggered.connect(self.modify_carrier_window)
        self.view_action.triggered.connect(self.view_carrier_window)
        self.refresh_action.triggered.connect(self.refresh_carrier_window)
        self.file_menu.addAction(self.exit_action)
        self.operation_menu.addAction(self.delete_action)
        self.operation_menu.addAction(self.insert_action)
        self.operation_menu.addAction(self.modify_action)
        self.operation_menu.addAction(self.view_action)
        self.toolbar.addAction(self.exit_action)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.delete_action)
        self.toolbar.addAction(self.insert_action)
        self.toolbar.addAction(self.modify_action)
        self.toolbar.addAction(self.view_action)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.refresh_action)

    def close_window(self):
        self.parentWidget().close()

    def delete_carrier_window(self):
        selected_row = self.carrier_table.currentRow()
        if selectedIDItem := self.carrier_table.item(selected_row, 0):
            requested_carrier= self.carrier_queries.get_carrier_byid(selectedIDItem.text())
            if isinstance(requested_carrier, CarrierInstance):
                delete_carrier_window = NewCarrierDialog(
                    self.app_settings, LCSettings.Settings.DELETE, requested_carrier
                )
                if delete_carrier_window.exec_() == qtw.QDialog.Accepted:
                    operation_returm_code = self.carrier_queries.delete_carrier(requested_carrier)
                    if operation_returm_code == 0:
                        qtw.QMessageBox(
                            qtw.QMessageBox.Information,
                            "Success", "Carrier was deleted",
                            qtw.QMessageBox.Yes
                        ).exec_()
                        self.carrier_table.removeRow(selected_row)
                        self.select_nearby_row(selected_row)
                else:
                    print('cancel')
            else:
                self.carrier_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                # self.statusbar.showMessage('Error code: -1. Error message: None selected row')
                #logging this error event

    def insert_carrier_window(self):
        insert_carrier_window = NewCarrierDialog(
            self.app_settings, LCSettings.Settings.INSERT, carrier_queries=self.carrier_queries
        )
        if insert_carrier_window.exec_() == qtw.QDialog.Accepted:
            self.add_row_topof_table(insert_carrier_window.new_carrier_instance)
        else:
            print('cancel')


    def modify_carrier_window(self):
        selected_row = self.carrier_table.currentRow()
        if selectedIDItem := self.carrier_table.item(selected_row, 0):
            requested_carrier = self.carrier_queries.get_carrier_byid(selectedIDItem.text())
            if isinstance(requested_carrier, CarrierInstance):
                modify_carrier_window = NewCarrierDialog(
                    self.app_settings, LCSettings.Settings.MODIFY, requested_carrier, self.carrier_queries
                )
                if modify_carrier_window.exec_() == qtw.QDialog.Accepted:
                    self.fill_row_with_data(selected_row, modify_carrier_window.modify_carrier_instance)
                else:
                    print('cancel')
            else:
                self.carrier_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                #logging this error eve

    def view_carrier_window(self):
        selected_row = self.carrier_table.currentRow()
        if selectedIDItem := self.carrier_table.item(selected_row, 0):
            requested_carrier = self.carrier_queries.get_carrier_byid(selectedIDItem.text())
            if isinstance(requested_carrier, CarrierInstance):
                view_carrier_window = NewCarrierDialog(
                    self.app_settings, LCSettings.Settings.VIEW, requested_carrier
                )
                if view_carrier_window.exec_() == qtw.QDialog.Accepted:
                    pass
                else:
                    pass
            else:
                self.carrier_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                #logging this error event

    def refresh_carrier_window(self):
        if self.carrier_worker.isRunning():
            self.carrier_worker.quit()
            self.carrier_table.setRowCount(0)
            self.carrier_worker.start()
        else:
            self.carrier_table.setRowCount(0)
            self.carrier_worker.start()

    def select_nearby_row(self, delete_row):
        row_count = self.carrier_table.rowCount()
        if row_count != 0:
            if delete_row == row_count:
                self.carrier_table.setCurrentCell(delete_row - 1, 0)
            else:
                self.carrier_table.setCurrentCell(delete_row, 0)


class ConsigneeWidget(qtw.QWidget):

    def __init__(self, app_settings, app_connection):
        super().__init__()
        # create "load from json" function for Settings class
        # self.app_connection = self.assembleConnection(self.app_settings)
        self.setup_supporting_vars(app_settings, app_connection)
        self.setup_gui()
        self.show()
        self.activate_worker()

    def setup_supporting_vars(self, app_settings, app_connection):
        self.app_settings = app_settings
        self.app_connection = app_connection
        self.consignee_worker = ConsigneeWorker(self.app_connection)
        self.consignee_queries = ConsigneeQueries(self.app_connection)

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.vertical_lo = qtw.QVBoxLayout()
        self.consignee_table = qtw.QTableWidget()
        self.progress_bar = qtw.QProgressBar()
        self.statusbar = qtw.QStatusBar()
        self.create_menus()

    def setup_gui_object_style_names(self):
        self.statusbar.setProperty('Error', False)
        self.statusbar.setStyle(self.statusbar.style())

    def layout_gui_objects(self):
        self.vertical_lo.addWidget(self.toolbar)
        self.vertical_lo.addWidget(self.consignee_table)
        self.vertical_lo.addWidget(self.progress_bar)
        self.vertical_lo.addWidget(self.statusbar)
        self.setLayout(self.vertical_lo)

    def feature_gui_objects(self):
        self.setGeometry(0, 0, self.app_settings.subwindow_width, self.app_settings.subwindow_height)
        self.setMinimumSize(600, 250)
        #dressing up table
        self.consignee_table.setColumnCount(11)
        self.consignee_table.setColumnHidden(0, True)
        self.consignee_table.setEditTriggers(qtw.QTableWidget.NoEditTriggers)
        self.consignee_table.setSelectionMode(qtw.QAbstractItemView.SingleSelection)
        self.consignee_table.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)
        self.consignee_table.selectRow(0)
        # self.usersTable.setCurrentItem(self.loadsTable.item(0, 0))
        self.consignee_table.setHorizontalHeaderLabels([
            "Consignee ID", "Consignee Name", "Address", "City",
            "State", "Country", "Postal Code",
            "Phone", "Fax", "Toll Free Phone",
            "Consignee Contact"
        ])
        header = self.consignee_table.horizontalHeader()
        header.setSectionResizeMode(0, qtw.QHeaderView.Fixed)
        header.setSectionResizeMode(1, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(2, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(3, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(4, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(5, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(6, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(7, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(8, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(9, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(10, qtw.QHeaderView.Stretch)
        #  settings up progress bar
        self.progress_bar.setValue(0)
        consignee_count = self.consignee_queries.consignees_count()
        if consignee_count != 0:
            self.progress_bar.setRange(0, consignee_count)
        else:
            self.progress_bar.setRange(0, 1)
        self.statusbar.showMessage('...')

    def setup_gui_object_events(self):
        self.create_menu_actions()
        self.consignee_table.cellDoubleClicked.connect(self.view_consignee_window)

    def activate_controls(self):
        self.delete_action.setEnabled(True)
        self.insert_action.setEnabled(True)
        self.modify_action.setEnabled(True)
        self.view_action.setEnabled(True)
        self.refresh_action.setEnabled(True)

    def deactivate_controls(self):
        self.delete_action.setEnabled(False)
        self.insert_action.setEnabled(False)
        self.modify_action.setEnabled(False)
        self.view_action.setEnabled(False)
        self.refresh_action.setEnabled(False)


    def activate_worker(self):
        self.consignee_queries.update_windowmessage_signal.connect(self.update_status_bar)
        self.consignee_worker.update_windowmessage_signal.connect(self.update_status_bar)
        self.consignee_worker.update_progressbar_signal.connect(self.update_progress_bar)
        self.consignee_worker.update_nextrow_signal.connect(self.add_row_to_table)
        self.consignee_worker.start()

    def update_status_bar(self, code, message):
        if code == 100000:
            self.statusbar.setProperty('Error', False)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(message)
            self.consignee_table.setCurrentCell(0, 0)
        elif code == 100001 or code == 100002:
            self.statusbar.setProperty('Error', False)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(message)
        else:
            self.statusbar.setProperty('Error', True)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(f'Error code: {code}. Error message: {message}')

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def add_row_to_table(self, consignee_instance):
        row_number = self.consignee_table.rowCount()
        self.consignee_table.insertRow(row_number)
        self.fill_row_with_data(row_number, consignee_instance)

    def add_row_topof_table(self, consignee_instance):
        self.consignee_table.insertRow(0)
        self.fill_row_with_data(0, consignee_instance)
        self.consignee_table.setCurrentCell(0, 0)

    def fill_row_with_data(self, row_number, consignee_instance):
        inserteditemid = qtw.QTableWidgetItem()
        inserteditemid.setData(qtc.Qt.DisplayRole, consignee_instance.consigneeid)
        inserteditemid.setTextAlignment(qtc.Qt.AlignCenter)
        self.consignee_table.setItem(row_number, 0, inserteditemid)

        inserteditemname = qtw.QTableWidgetItem()
        inserteditemname.setData(qtc.Qt.DisplayRole, consignee_instance.consigneename)
        inserteditemname.setTextAlignment(qtc.Qt.AlignCenter)
        self.consignee_table.setItem(row_number, 1, inserteditemname)

        inserteditemaddress = qtw.QTableWidgetItem()
        inserteditemaddress.setData(qtc.Qt.DisplayRole, consignee_instance.consigneeaddress)
        inserteditemaddress.setTextAlignment(qtc.Qt.AlignCenter)
        self.consignee_table.setItem(row_number, 2, inserteditemaddress)

        inserteditemcity = qtw.QTableWidgetItem()
        inserteditemcity.setData(qtc.Qt.DisplayRole, consignee_instance.consigneecity)
        inserteditemcity.setTextAlignment(qtc.Qt.AlignCenter)
        self.consignee_table.setItem(row_number, 3, inserteditemcity)

        inserteditemstate = qtw.QTableWidgetItem()
        inserteditemstate.setData(qtc.Qt.DisplayRole, consignee_instance.consigneestate)
        inserteditemstate.setTextAlignment(qtc.Qt.AlignCenter)
        self.consignee_table.setItem(row_number, 4, inserteditemstate)

        inserteditemcountry = qtw.QTableWidgetItem()
        inserteditemcountry.setData(qtc.Qt.DisplayRole, consignee_instance.consigneecountry)
        inserteditemcountry.setTextAlignment(qtc.Qt.AlignCenter)
        self.consignee_table.setItem(row_number, 5, inserteditemcountry)

        inserteditempostalcode = qtw.QTableWidgetItem()
        inserteditempostalcode.setData(qtc.Qt.DisplayRole, consignee_instance.consigneepostalcode)
        inserteditempostalcode.setTextAlignment(qtc.Qt.AlignCenter)
        self.consignee_table.setItem(row_number, 6, inserteditempostalcode)

        inserteditemphone = qtw.QTableWidgetItem()
        inserteditemphone.setData(qtc.Qt.DisplayRole, consignee_instance.consigneephone)
        inserteditemphone.setTextAlignment(qtc.Qt.AlignCenter)
        self.consignee_table.setItem(row_number, 7, inserteditemphone)

        inserteditemfax = qtw.QTableWidgetItem()
        inserteditemfax.setData(qtc.Qt.DisplayRole, consignee_instance.consigneefax)
        inserteditemfax.setTextAlignment(qtc.Qt.AlignCenter)
        self.consignee_table.setItem(row_number, 8, inserteditemfax)

        inserteditemtollfree = qtw.QTableWidgetItem()
        inserteditemtollfree.setData(qtc.Qt.DisplayRole, consignee_instance.consigneetollfree)
        inserteditemtollfree.setTextAlignment(qtc.Qt.AlignCenter)
        self.consignee_table.setItem(row_number, 9, inserteditemtollfree)

        inserteditemcontact = qtw.QTableWidgetItem()
        inserteditemcontact.setData(qtc.Qt.DisplayRole, consignee_instance.consigneecontact)
        inserteditemcontact.setTextAlignment(qtc.Qt.AlignCenter)
        self.consignee_table.setItem(row_number, 10, inserteditemcontact)

    def create_menus(self):
        menubar = qtw.QMenuBar()
        self.toolbar = qtw.QToolBar()
        self.toolbar.setFixedHeight(55)
        self.toolbar.setIconSize(qtc.QSize(50, 50))
        self.file_menu = menubar.addMenu('File')
        self.operation_menu = menubar.addMenu('Operation')
        self.vertical_lo.setMenuBar(menubar)

    def create_menu_actions(self):
        self.exit_action = qtw.QAction(
            (qtg.QIcon(':/icon_exit.png')),
            'Exit', self
        )
        self.delete_action = qtw.QAction(
            (qtg.QIcon(':/icon_delete.png')),
            'Delete Load Confirmation', self
        )
        self.insert_action = qtw.QAction(
            (qtg.QIcon(':/icon_insert.png')),
            'Insert Load Confirmation', self
        )
        self.modify_action = qtw.QAction(
            (qtg.QIcon(':/icon_modify.png')),
            'Modify Load Confirmation', self
        )
        self.view_action = qtw.QAction(
            (qtg.QIcon(':/icon_view.png')),
            'View Load Confirmation', self
        )
        self.refresh_action = qtw.QAction(
            (qtg.QIcon(':/icon_refresh.png')),
            'Refresh Table', self
        )
        self.exit_action.triggered.connect(self.close_window)
        self.delete_action.triggered.connect(self.delete_consignee_window)
        self.insert_action.triggered.connect(self.insert_consignee_window)
        self.modify_action.triggered.connect(self.modify_consignee_window)
        self.view_action.triggered.connect(self.view_consignee_window)
        self.refresh_action.triggered.connect(self.refresh_consignee_window)
        self.file_menu.addAction(self.exit_action)
        self.operation_menu.addAction(self.delete_action)
        self.operation_menu.addAction(self.insert_action)
        self.operation_menu.addAction(self.modify_action)
        self.operation_menu.addAction(self.view_action)
        self.toolbar.addAction(self.exit_action)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.delete_action)
        self.toolbar.addAction(self.insert_action)
        self.toolbar.addAction(self.modify_action)
        self.toolbar.addAction(self.view_action)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.refresh_action)

    def close_window(self):
        self.parentWidget().close()

    def delete_consignee_window(self):
        selected_row = self.consignee_table.currentRow()
        if selectedIDItem := self.consignee_table.item(selected_row, 0):
            requested_consignee= self.consignee_queries.get_consignee_byid(selectedIDItem.text())
            if isinstance(requested_consignee, ConsigneeInstance):
                delete_consignee_window = NewConsigneeDialog(
                    app_settings=self.app_settings,
                    dialog_flag=LCSettings.Settings.DELETE,
                    input_consignee_instance=requested_consignee,
                    consignee_queries=self.consignee_queries
                )
                if delete_consignee_window.exec_() == qtw.QDialog.Accepted:
                    operation_returm_code = self.consignee_queries.delete_consignee(requested_consignee)
                    if operation_returm_code == 0:
                        qtw.QMessageBox(
                            qtw.QMessageBox.Information,
                            "Success", "Consignee was deleted",
                            qtw.QMessageBox.Yes
                        ).exec_()
                        self.consignee_table.removeRow(selected_row)
                        self.select_nearby_row(selected_row)
                else:
                    print('cancel')
            else:
                self.consignee_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                # self.statusbar.showMessage('Error code: -1. Error message: None selected row')
                #logging this error event

    def insert_consignee_window(self):
        insert_consignee_window = NewConsigneeDialog(
            self.app_settings, LCSettings.Settings.INSERT, consignee_queries=self.consignee_queries
        )
        if insert_consignee_window.exec_() == qtw.QDialog.Accepted:
            self.add_row_topof_table(insert_consignee_window.new_consignee_instance)
        else:
            print('cancel')


    def modify_consignee_window(self):
        selected_row = self.consignee_table.currentRow()
        if selectedIDItem := self.consignee_table.item(selected_row, 0):
            requested_consignee = self.consignee_queries.get_consignee_byid(selectedIDItem.text())
            if isinstance(requested_consignee, ConsigneeInstance):
                modify_consignee_window = NewConsigneeDialog(
                    self.app_settings, LCSettings.Settings.MODIFY, requested_consignee, self.consignee_queries
                )
                if modify_consignee_window.exec_() == qtw.QDialog.Accepted:
                    self.fill_row_with_data(selected_row, modify_consignee_window.modify_consignee_instance)
                else:
                    print('cancel')
            else:
                self.consignee_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                #logging this error eve

    def view_consignee_window(self):
        selected_row = self.consignee_table.currentRow()
        if selectedIDItem := self.consignee_table.item(selected_row, 0):
            requested_consignee = self.consignee_queries.get_consignee_byid(selectedIDItem.text())
            if isinstance(requested_consignee, ConsigneeInstance):
                view_consignee_window = NewConsigneeDialog(
                    self.app_settings, LCSettings.Settings.VIEW, requested_consignee
                )
                if view_consignee_window.exec_() == qtw.QDialog.Accepted:
                    pass
                else:
                    pass
            else:
                self.consignee_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                #logging this error event

    def refresh_consignee_window(self):
        if self.consignee_worker.isRunning():
            self.consignee_worker.terminate()
            self.consignee_table.setRowCount(0)
            self.consignee_worker.start()
        else:
            self.consignee_table.setRowCount(0)
            self.consignee_worker.start()

    def select_nearby_row(self, delete_row):
        row_count = self.consignee_table.rowCount()
        if row_count != 0:
            if delete_row == row_count:
                self.consignee_table.setCurrentCell(delete_row - 1, 0)
            else:
                self.consignee_table.setCurrentCell(delete_row, 0)


class CurrencyWidget(qtw.QWidget):

    def __init__(self, app_settings, app_connection):
        super().__init__()
        # create "load from json" function for Settings class
        # self.app_connection = self.assembleConnection(self.app_settings)
        self.setup_supporting_vars(app_settings, app_connection)
        self.setup_gui()
        self.show()
        self.activate_worker()

    def setup_supporting_vars(self, app_settings, app_connection):
        self.app_settings = app_settings
        self.app_connection = app_connection
        self.currency_worker = CurrencyWorker(self.app_connection)
        self.currency_queries = CurrencyQueries(self.app_connection)

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.vertical_lo = qtw.QVBoxLayout()
        self.currency_table = qtw.QTableWidget()
        self.progress_bar = qtw.QProgressBar()
        self.statusbar = qtw.QStatusBar()
        self.create_menus()

    def setup_gui_object_style_names(self):
        self.statusbar.setProperty('Error', False)
        self.statusbar.setStyle(self.statusbar.style())

    def layout_gui_objects(self):
        self.vertical_lo.addWidget(self.toolbar)
        self.vertical_lo.addWidget(self.currency_table)
        self.vertical_lo.addWidget(self.progress_bar)
        self.vertical_lo.addWidget(self.statusbar)
        self.setLayout(self.vertical_lo)

    def feature_gui_objects(self):
        self.setGeometry(0, 0, self.app_settings.smallsubwindow_width, self.app_settings.smallsubwindow_height)
        self.setMinimumSize(600, 250)
        #dressing up table
        self.currency_table.setColumnCount(4)
        self.currency_table.setColumnHidden(0, True)
        self.currency_table.setEditTriggers(qtw.QTableWidget.NoEditTriggers)
        self.currency_table.setSelectionMode(qtw.QAbstractItemView.SingleSelection)
        self.currency_table.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)
        self.currency_table.selectRow(0)
        self.currency_table.setHorizontalHeaderLabels([
            "CurrencyId",
            "Currency Short Name",
            "Currency Name",
            "Currency Image"
            ])
        self.currency_table.setColumnWidth(1, 200)
        self.currency_table.setColumnWidth(2, 200)
        self.currency_table.setColumnWidth(3, 65)
        # settings up progress bar
        self.progress_bar.setValue(0)
        currencys_count = self.currency_queries.currencies_count()
        if currencys_count != 0:
            self.progress_bar.setRange(0, currencys_count)
        else:
            self.progress_bar.setRange(0, 1)
        self.statusbar.showMessage('...')

    def setup_gui_object_events(self):
        self.create_menu_actions()
        self.currency_table.cellDoubleClicked.connect(self.view_currency_window)

    def activate_controls(self):
        self.delete_action.setEnabled(True)
        self.insert_action.setEnabled(True)
        self.modify_action.setEnabled(True)
        self.view_action.setEnabled(True)
        self.refresh_action.setEnabled(True)

    def deactivate_controls(self):
        self.delete_action.setEnabled(False)
        self.insert_action.setEnabled(False)
        self.modify_action.setEnabled(False)
        self.view_action.setEnabled(False)
        self.refresh_action.setEnabled(False)

    def activate_worker(self):
        self.currency_queries.update_windowmessage_signal.connect(self.update_status_bar)
        self.currency_worker.update_windowmessage_signal.connect(self.update_status_bar)
        self.currency_worker.update_progressbar_signal.connect(self.update_progress_bar)
        self.currency_worker.update_nextrow_signal.connect(self.add_row_to_table)
        self.currency_worker.start()

    def update_status_bar(self, code, message):
        if code == 100000:
            self.statusbar.setProperty('Error', False)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(message)
            self.currency_table.setCurrentCell(0, 0)
            self.refresh_action.setEnabled(True)
        elif code == 100001 or code == 100002:
            self.statusbar.setProperty('Error', False)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(message)
        else:
            self.statusbar.setProperty('Error', True)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(f'Error code: {code}. Error message: {message}')

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def add_row_to_table(self, new_currency_instance):
        current_row_count = self.currency_table.rowCount()
        self.currency_table.insertRow(current_row_count)
        self.fill_row_with_data(current_row_count, new_currency_instance)

    def add_row_topof_table(self, currency_instance):
        self.currency_table.insertRow(0)
        self.fill_row_with_data(0, currency_instance)
        self.currency_table.setCurrentCell(0, 0)

    def fill_row_with_data(self, row_number, currency_instance):
        inserteditemid = qtw.QTableWidgetItem()
        inserteditemid.setData(qtc.Qt.DisplayRole, currency_instance.currencyid)
        inserteditemid.setTextAlignment(qtc.Qt.AlignCenter)
        self.currency_table.setItem(row_number, 0, inserteditemid)

        inserteditemshortname = qtw.QTableWidgetItem()
        inserteditemshortname.setData(qtc.Qt.DisplayRole, currency_instance.currencyshortname)
        inserteditemshortname.setTextAlignment(qtc.Qt.AlignCenter)
        self.currency_table.setItem(row_number, 1, inserteditemshortname)

        inserteditemname = qtw.QTableWidgetItem()
        inserteditemname.setData(qtc.Qt.DisplayRole, currency_instance.currencyname)
        inserteditemname.setTextAlignment(qtc.Qt.AlignCenter)
        self.currency_table.setItem(row_number, 2, inserteditemname)

        inserteditemimage = qtw.QTableWidgetItem()
        inserteditemimage.setData(qtc.Qt.DecorationRole, qtg.QPixmap(currency_instance.currencyimagepath))
        inserteditemimage.setTextAlignment(qtc.Qt.AlignCenter)
        self.currency_table.setItem(row_number, 3, inserteditemimage)

    def create_menus(self):
        menubar = qtw.QMenuBar()
        self.toolbar = qtw.QToolBar()
        self.toolbar.setFixedHeight(55)
        self.toolbar.setIconSize(qtc.QSize(50, 50))
        self.file_menu = menubar.addMenu('File')
        self.operation_menu = menubar.addMenu('Operation')
        self.vertical_lo.setMenuBar(menubar)

    def create_menu_actions(self):
        self.exit_action = qtw.QAction(
            (qtg.QIcon(':/icon_exit.png')),
            'Exit', self
        )
        self.delete_action = qtw.QAction(
            (qtg.QIcon(':/icon_delete.png')),
            'Delete Currency', self
        )
        self.insert_action = qtw.QAction(
            (qtg.QIcon(':/icon_insert.png')),
            'Insert Currency', self
        )
        self.modify_action = qtw.QAction(
            (qtg.QIcon(':/icon_modify.png')),
            'Modify Currency', self
        )
        self.view_action = qtw.QAction(
            (qtg.QIcon(':/icon_view.png')),
            'View Currency', self
        )
        self.refresh_action = qtw.QAction(
            (qtg.QIcon(':/icon_refresh.png')),
            'Refresh Table', self
        )
        self.refresh_action.setEnabled(False)
        self.exit_action.triggered.connect(self.close_window)
        self.delete_action.triggered.connect(self.delete_currency_window)
        self.insert_action.triggered.connect(self.insert_currency_window)
        self.modify_action.triggered.connect(self.modify_currency_window)
        self.view_action.triggered.connect(self.view_currency_window)
        self.refresh_action.triggered.connect(self.refresh_currency_window)
        self.file_menu.addAction(self.exit_action)
        self.operation_menu.addAction(self.delete_action)
        self.operation_menu.addAction(self.insert_action)
        self.operation_menu.addAction(self.modify_action)
        self.operation_menu.addAction(self.view_action)
        self.toolbar.addAction(self.exit_action)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.delete_action)
        self.toolbar.addAction(self.insert_action)
        self.toolbar.addAction(self.modify_action)
        self.toolbar.addAction(self.view_action)
        self.toolbar.addAction(self.refresh_action)

    def close_window(self):
        self.parentWidget().close()

    def delete_currency_window(self):
        selected_row = self.currency_table.currentRow()
        if selectedIDItem := self.currency_table.item(selected_row, 0):
            requested_currency = self.currency_queries.get_currency_byid(selectedIDItem.text())
            if isinstance(requested_currency, CurrencyInstance):
                delete_currency_window = NewCurrencyDialog(
                    self.app_settings, LCSettings.Settings.DELETE, requested_currency
                )
                if delete_currency_window.exec_() == qtw.QDialog.Accepted:
                    operation_returm_code = self.currency_queries.delete_currency(requested_currency)
                    if operation_returm_code == 0:
                        qtw.QMessageBox(
                            qtw.QMessageBox.Information,
                            "Success", "Currency was deleted",
                            qtw.QMessageBox.Yes
                        ).exec_()
                        self.currency_table.removeRow(selected_row)
                        self.select_nearby_row(selected_row)
                else:
                    print('cancel')
            else:
                self.currency_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                # self.statusbar.showMessage('Error code: -1. Error message: None selected row')
                #logging this error event

    def insert_currency_window(self):
        insert_currency_window = NewCurrencyDialog(
            self.app_settings, LCSettings.Settings.INSERT, currency_queries=self.currency_queries
        )
        if insert_currency_window.exec_() == qtw.QDialog.Accepted:
            self.add_row_topof_table(insert_currency_window.new_currency_instance)
        else:
            print('cancel')


    def modify_currency_window(self):
        selected_row = self.currency_table.currentRow()
        if selectedIDItem := self.currency_table.item(selected_row, 0):
            requested_currency = self.currency_queries.get_currency_byid(selectedIDItem.text())
            if isinstance(requested_currency, CurrencyInstance):
                modify_currency_window = NewCurrencyDialog(
                    self.app_settings, LCSettings.Settings.MODIFY, requested_currency, self.currency_queries
                )
                if modify_currency_window.exec_() == qtw.QDialog.Accepted:
                    self.fill_row_with_data(selected_row, modify_currency_window.modify_currency_instance)
                else:
                    print('cancel')
            else:
                self.currency_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                #logging this error eve

    def view_currency_window(self):
        selected_row = self.currency_table.currentRow()
        if selectedIDItem := self.currency_table.item(selected_row, 0):
            requested_currency = self.currency_queries.get_currency_byid(selectedIDItem.text())
            if isinstance(requested_currency, CurrencyInstance):
                view_currency_window = NewCurrencyDialog(
                    self.app_settings, LCSettings.Settings.VIEW, requested_currency
                )
                if view_currency_window.exec_() == qtw.QDialog.Accepted:
                    pass
                else:
                    pass
            else:
                self.currency_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                #logging this error event

    def refresh_currency_window(self):
        if self.currency_worker.isRunning():
            self.currency_worker.quit()
            self.currency_table.setRowCount(0)
            self.currency_worker.start()
        else:
            self.currency_table.setRowCount(0)
            self.currency_worker.start()

    def select_nearby_row(self, delete_row):
        row_count = self.currency_table.rowCount()
        if row_count != 0:
            if delete_row == row_count:
                self.currency_table.setCurrentCell(delete_row - 1, 0)
            else:
                self.currency_table.setCurrentCell(delete_row, 0)


class LoadConfirmationWidget(qtw.QWidget):

    def __init__(self, app_settings, app_connection):
        super().__init__()
        # create "load from json" function for Settings class
        # self.app_connection = self.assembleConnection(self.app_settings)
        self.setup_supporting_vars(app_settings, app_connection)
        self.setup_gui()
        self.show()
        self.activate_worker()

    def setup_supporting_vars(self, app_settings, app_connection):
        self.app_settings = app_settings
        self.app_connection = app_connection
        self.loadconfirmation_worker= LoadConfirmationsWorker(self.app_connection)
        self.loadconfirmation_queries = LoadConfirmationsQueries(self.app_connection)

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.vertical_lo = qtw.QVBoxLayout()
        self.dir_button = qtw.QPushButton('  FilterButton  ')
        self.loadconfirmation_table = qtw.QTableWidget()
        self.progress_bar = qtw.QProgressBar()
        self.statusbar = qtw.QStatusBar()
        self.create_menus()

    def setup_gui_object_style_names(self):
        self.statusbar.setProperty('Error', False)
        self.statusbar.setStyle(self.statusbar.style())

    def layout_gui_objects(self):
        self.vertical_lo.addWidget(self.toolbar)
        self.vertical_lo.addWidget(self.dir_button, alignment=qtc.Qt.AlignLeft)
        self.vertical_lo.addWidget(self.loadconfirmation_table)
        self.vertical_lo.addWidget(self.progress_bar)
        self.vertical_lo.addWidget(self.statusbar)
        self.setLayout(self.vertical_lo)

    def feature_gui_objects(self):
        self.setGeometry(0, 0, self.app_settings.subwindow_width, self.app_settings.subwindow_height)
        self.setMinimumSize(600, 250)
        #dressing up table
        self.loadconfirmation_table.setColumnCount(15)
        self.loadconfirmation_table.setColumnHidden(0, True)
        self.loadconfirmation_table.setColumnHidden(1, True)
        self.loadconfirmation_table.setColumnHidden(2, True)
        self.loadconfirmation_table.setColumnHidden(3, True)
        self.loadconfirmation_table.setColumnHidden(4, True)
        self.loadconfirmation_table.setColumnHidden(5, True)
        self.loadconfirmation_table.setEditTriggers(qtw.QTableWidget.NoEditTriggers)
        self.loadconfirmation_table.setSelectionMode(qtw.QAbstractItemView.SingleSelection)
        self.loadconfirmation_table.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)
        self.loadconfirmation_table.selectRow(0)
        self.loadconfirmation_table.setHorizontalHeaderLabels([
            "LCID", "CurrencyID", "LoadTypeID",
            "CarrierID", "CustombrokerID", "Note",
            "Confirmation #", "Created on", "Rate",
            "Currency", "Quantity", "Load Type",
            "Carrier", "Custom Broker", "User"
        ])
        header = self.loadconfirmation_table.horizontalHeader()
        header.setSectionResizeMode(0, qtw.QHeaderView.Fixed)
        header.setSectionResizeMode(1, qtw.QHeaderView.Fixed)
        header.setSectionResizeMode(2, qtw.QHeaderView.Fixed)
        header.setSectionResizeMode(3, qtw.QHeaderView.Fixed)
        header.setSectionResizeMode(4, qtw.QHeaderView.Fixed)
        header.setSectionResizeMode(5, qtw.QHeaderView.Fixed)
        header.setSectionResizeMode(6, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(7, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(8, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(9, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(10, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(11, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(12, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(13, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(14, qtw.QHeaderView.Stretch)

        # settings up progress bar
        self.progress_bar.setValue(0)
        loads_count = self.loadconfirmation_queries.loads_count()
        if loads_count != 0:
            self.progress_bar.setRange(0, loads_count)
        else:
            self.progress_bar.setRange(0, 1)
        self.statusbar.showMessage('...')


    def setup_gui_object_events(self):
        self.dir_button.clicked.connect(self.execute_filter)
        self.loadconfirmation_table.cellDoubleClicked.connect(self.view_loadconfirmation_window)
        self.create_menu_actions()

    def activate_controls(self):
        self.delete_action.setEnabled(True)
        self.insert_action.setEnabled(True)
        self.modify_action.setEnabled(True)
        self.view_action.setEnabled(True)
        self.refresh_action.setEnabled(True)

    def deactivate_controls(self):
        self.delete_action.setEnabled(False)
        self.insert_action.setEnabled(False)
        self.modify_action.setEnabled(False)
        self.view_action.setEnabled(False)
        self.refresh_action.setEnabled(False)

    def execute_filter(self):
        self.reset_progress_bar()

    def reset_progress_bar(self):
        pass

    def activate_worker(self):
        self.loadconfirmation_queries.update_windowmessage_signal.connect(self.update_status_bar)
        self.loadconfirmation_worker.update_windowmessage_signal.connect(self.update_status_bar)
        self.loadconfirmation_worker.update_value_signal.connect(self.update_progress_bar)
        self.loadconfirmation_worker.update_nextrow_signal.connect(self.add_row_to_table)
        self.loadconfirmation_worker.start()

    def update_status_bar(self, code, message):
        if code == 100000:
            self.statusbar.setProperty('Error', False)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(message)
            self.loadconfirmation_table.setCurrentCell(0, 0)
            self.refresh_action.setEnabled(True)
        elif code == 100001 or code == 100002:
            self.statusbar.setProperty('Error', False)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(message)
        else:
            self.statusbar.setProperty('Error', True)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(f'Error code: {code}. Error message: {message}')

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def add_row_to_table(self, new_load_confirmation_instance):
        current_row_count = self.loadconfirmation_table.rowCount()
        self.loadconfirmation_table.insertRow(current_row_count)
        self.fill_row_with_data(current_row_count, new_load_confirmation_instance)

    def add_row_topof_table(self, new_loadconfirmation_instance):
        self.loadconfirmation_table.insertRow(0)
        self.fill_row_with_data(0, new_loadconfirmation_instance)
        self.loadconfirmation_table.setCurrentCell(0, 0)

    def fill_row_with_data(self, current_row_count, new_loadconfirmation_instance):
        inserteditemid = qtw.QTableWidgetItem()
        inserteditemid.setData(qtc.Qt.DisplayRole, new_loadconfirmation_instance.lcid)
        inserteditemid.setTextAlignment(qtc.Qt.AlignCenter)
        self.loadconfirmation_table.setItem(current_row_count, 0, inserteditemid)

        inserteditemcurrencyid = qtw.QTableWidgetItem()
        inserteditemcurrencyid.setData(qtc.Qt.DisplayRole, new_loadconfirmation_instance.lccurrencyid)
        inserteditemcurrencyid.setTextAlignment(qtc.Qt.AlignCenter)
        self.loadconfirmation_table.setItem(current_row_count, 1, inserteditemcurrencyid)

        inserteditemloadtypeid = qtw.QTableWidgetItem()
        inserteditemloadtypeid.setData(qtc.Qt.DisplayRole, new_loadconfirmation_instance.lcloadtypeid)
        inserteditemloadtypeid.setTextAlignment(qtc.Qt.AlignCenter)
        self.loadconfirmation_table.setItem(current_row_count, 2, inserteditemloadtypeid)

        inserteditemcarrierid = qtw.QTableWidgetItem()
        inserteditemcarrierid.setData(qtc.Qt.DisplayRole, new_loadconfirmation_instance.lccarrierid)
        inserteditemcarrierid.setTextAlignment(qtc.Qt.AlignCenter)
        self.loadconfirmation_table.setItem(current_row_count, 3, inserteditemcarrierid)

        inserteditemcustombrokerid = qtw.QTableWidgetItem()
        inserteditemcustombrokerid.setData(qtc.Qt.DisplayRole, new_loadconfirmation_instance.lccustombrokerid)
        inserteditemcustombrokerid.setTextAlignment(qtc.Qt.AlignCenter)
        self.loadconfirmation_table.setItem(current_row_count, 4, inserteditemcustombrokerid)

        inserteditemnote = qtw.QTableWidgetItem()
        inserteditemnote.setData(qtc.Qt.DisplayRole, new_loadconfirmation_instance.lcnote)
        inserteditemnote.setTextAlignment(qtc.Qt.AlignCenter)
        self.loadconfirmation_table.setItem(current_row_count, 5, inserteditemnote)

        inserteditemno = qtw.QTableWidgetItem()
        inserteditemno.setData(qtc.Qt.DisplayRole, new_loadconfirmation_instance.lcno)
        inserteditemno.setTextAlignment(qtc.Qt.AlignCenter)
        self.loadconfirmation_table.setItem(current_row_count, 6, inserteditemno)

        # print(type(new_loadconfirmation_instance.lcdatecreated.data(qtc.Qt.EditRole)))
        inserteditemdatecreated = qtw.QTableWidgetItem()
        inserteditemdatecreated.setData(
            qtc.Qt.DisplayRole,
            qtc.QDateTime(new_loadconfirmation_instance.lcdatecreated).toString('yyyy-MM-dd')
        )
        inserteditemdatecreated.setTextAlignment(qtc.Qt.AlignCenter)
        self.loadconfirmation_table.setItem(current_row_count, 7, inserteditemdatecreated)

        inserteditemagreedrate = qtw.QTableWidgetItem()
        inserteditemagreedrate.setData(qtc.Qt.DisplayRole, str(new_loadconfirmation_instance.lcagreedrate))
        inserteditemagreedrate.setTextAlignment(qtc.Qt.AlignCenter)
        self.loadconfirmation_table.setItem(current_row_count, 8, inserteditemagreedrate)

        inserteditemcurrencyshortname = qtw.QTableWidgetItem()
        inserteditemcurrencyshortname.setData(qtc.Qt.DisplayRole, new_loadconfirmation_instance.lccurrencyshortname)
        inserteditemcurrencyshortname.setTextAlignment(qtc.Qt.AlignCenter)
        self.loadconfirmation_table.setItem(current_row_count, 9, inserteditemcurrencyshortname)

        inserteditemquantity = qtw.QTableWidgetItem()
        inserteditemquantity.setData(qtc.Qt.DisplayRole, new_loadconfirmation_instance.lcquantity)
        inserteditemquantity.setTextAlignment(qtc.Qt.AlignCenter)
        self.loadconfirmation_table.setItem(current_row_count, 10, inserteditemquantity)

        inserteditemtypename = qtw.QTableWidgetItem()
        inserteditemtypename.setData(qtc.Qt.DisplayRole, new_loadconfirmation_instance.lcloadtypename)
        inserteditemtypename.setTextAlignment(qtc.Qt.AlignCenter)
        self.loadconfirmation_table.setItem(current_row_count, 11, inserteditemtypename)

        inserteditemcarriername = qtw.QTableWidgetItem()
        inserteditemcarriername.setData(qtc.Qt.DisplayRole, new_loadconfirmation_instance.lccarriername)
        inserteditemcarriername.setTextAlignment(qtc.Qt.AlignCenter)
        self.loadconfirmation_table.setItem(current_row_count, 12, inserteditemcarriername)

        inserteditembrokername = qtw.QTableWidgetItem()
        inserteditembrokername.setData(qtc.Qt.DisplayRole, new_loadconfirmation_instance.lccustombrokername)
        inserteditembrokername.setTextAlignment(qtc.Qt.AlignCenter)
        self.loadconfirmation_table.setItem(current_row_count, 13, inserteditembrokername)

        inserteditemcreatedby = qtw.QTableWidgetItem()
        inserteditemcreatedby.setData(qtc.Qt.DisplayRole, new_loadconfirmation_instance.lccreatedby)
        inserteditemcreatedby.setTextAlignment(qtc.Qt.AlignCenter)
        self.loadconfirmation_table.setItem(current_row_count, 14, inserteditemcreatedby)

    def create_menus(self):
        menubar = qtw.QMenuBar()
        self.toolbar = qtw.QToolBar()
        self.toolbar.setFixedHeight(55)
        self.toolbar.setIconSize(qtc.QSize(50, 50))
        self.file_menu = menubar.addMenu('File')
        self.operation_menu = menubar.addMenu('Operation')
        self.vertical_lo.setMenuBar(menubar)

    def create_menu_actions(self):
        self.exit_action = qtw.QAction(
            (qtg.QIcon(':/icon_exit.png')),
            'Exit', self
        )
        self.delete_action = qtw.QAction(
            (qtg.QIcon(':/icon_delete.png')),
            'Delete Load Confirmation', self
        )
        self.insert_action = qtw.QAction(
            (qtg.QIcon(':/icon_insert.png')),
            'Insert Load Confirmation', self
        )
        self.modify_action = qtw.QAction(
            (qtg.QIcon(':/icon_modify.png')),
            'Modify Load Confirmation', self
        )
        self.view_action = qtw.QAction(
            (qtg.QIcon(':/icon_view.png')),
            'View Load Confirmation', self
        )
        self.refresh_action = qtw.QAction(
            (qtg.QIcon(':/icon_refresh.png')),
            'Refresh Table', self
        )
        self.refresh_action.setEnabled(False)
        self.exit_action.triggered.connect(self.close_window)
        self.delete_action.triggered.connect(self.delete_loadconfirmation_window)
        self.insert_action.triggered.connect(self.insert_loadconfirmation_window)
        self.modify_action.triggered.connect(self.modify_loadconfirmation_window)
        self.view_action.triggered.connect(self.view_loadconfirmation_window)
        self.refresh_action.triggered.connect(self.refresh_loadconfirmation_window)
        self.file_menu.addAction(self.exit_action)
        self.operation_menu.addAction(self.delete_action)
        self.operation_menu.addAction(self.insert_action)
        self.operation_menu.addAction(self.modify_action)
        self.operation_menu.addAction(self.view_action)
        self.toolbar.addAction(self.exit_action)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.delete_action)
        self.toolbar.addAction(self.insert_action)
        self.toolbar.addAction(self.modify_action)
        self.toolbar.addAction(self.view_action)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.refresh_action)

    def close_window(self):
        self.parentWidget().close()

    def delete_loadconfirmation_window(self):
        selected_row = self.loadconfirmation_table.currentRow()
        if selectedIDItem := self.loadconfirmation_table.item(selected_row, 0):
            requested_loadconfirmation = self.loadconfirmation_queries.get_loadconfirmation_byid(selectedIDItem.text())
            if isinstance(requested_loadconfirmation, LoadConfirmationInstance):
                delete_loadconfirmation_window = NewLoadConfirmationDialog(
                    self.app_settings,
                    LCSettings.Settings.DELETE,
                    requested_loadconfirmation,
                    loadconfirmation_queries=self.loadconfirmation_queries
                )
                if delete_loadconfirmation_window.exec_() == qtw.QDialog.Accepted:
                    self.loadconfirmation_table.removeRow(selected_row)
                    self.select_nearby_row(selected_row)
                else:
                    print('cancel')

    def insert_loadconfirmation_window(self):
        insert_loadconfirmation_window = NewLoadConfirmationDialog(
            self.app_settings,
            LCSettings.Settings.INSERT,
            loadconfirmation_queries=self.loadconfirmation_queries
        )
        if insert_loadconfirmation_window.exec_() == qtw.QDialog.Accepted:
            self.add_row_topof_table(insert_loadconfirmation_window.new_loadconfirmation_instance)
        else:
            print('cancel')

    def modify_loadconfirmation_window(self):
        selected_row = self.loadconfirmation_table.currentRow()
        if selectedIDItem := self.loadconfirmation_table.item(selected_row, 0):
            requested_load_confirmation = self.loadconfirmation_queries.get_loadconfirmation_byid(selectedIDItem.text())
            if isinstance(requested_load_confirmation, LoadConfirmationInstance):
                modify_load_confirmation_window = NewLoadConfirmationDialog(
                    self.app_settings,
                    LCSettings.Settings.MODIFY,
                    requested_load_confirmation,
                    loadconfirmation_queries=self.loadconfirmation_queries
                )
                if modify_load_confirmation_window.exec_() == qtw.QDialog.Accepted:
                    self.fill_row_with_data(selected_row, modify_load_confirmation_window.modify_loadconfirmation_instance)
                else:
                    pass
            else:
                self.loadconfirmation_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                #logging this error event

    def view_loadconfirmation_window(self):
        selected_row = self.loadconfirmation_table.currentRow()
        if selectedIDItem := self.loadconfirmation_table.item(selected_row, 0):
            requested_load_confirmation = self.loadconfirmation_queries.get_loadconfirmation_byid(selectedIDItem.text())
            print(requested_load_confirmation.lcno)
            if isinstance(requested_load_confirmation, LoadConfirmationInstance):
                view_load_confirmation_window = NewLoadConfirmationDialog(
                    app_settings=self.app_settings,
                    dialog_flag=LCSettings.Settings.VIEW,
                    input_loadconfirmation_instance=requested_load_confirmation,
                    loadconfirmation_queries=self.loadconfirmation_queries
                )
                if view_load_confirmation_window.exec_() == qtw.QDialog.Accepted:
                    pass
                else:
                    pass
            else:
                self.loadconfirmation_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                #logging this error event

    def refresh_loadconfirmation_window(self):
        if self.loadconfirmation_worker.isRunning():
            self.loadconfirmation_worker.quit()
            self.loadconfirmation_table.setRowCount(0)
            self.loadconfirmation_worker.start()
        else:
            self.loadconfirmation_table.setRowCount(0)
            self.loadconfirmation_worker.start()

    def select_nearby_row(self, delete_row):
        row_count = self.loadconfirmation_table.rowCount()
        if row_count != 0:
            if delete_row == row_count:
                self.loadconfirmation_table.setCurrentCell(delete_row - 1, 0)
            else:
                self.loadconfirmation_table.setCurrentCell(delete_row, 0)


class LoadTypeWidget(qtw.QWidget):

    def __init__(self, app_settings, app_connection):
        super().__init__()
        # create "load from json" function for Settings class
        # self.app_connection = self.assembleConnection(self.app_settings)
        self.setup_supporting_vars(app_settings, app_connection)
        self.setup_gui()
        self.show()
        self.activate_worker()

    def setup_supporting_vars(self, app_settings, app_connection):
        self.app_settings = app_settings
        self.app_connection = app_connection
        self.loadtype_worker = LoadTypeWorker(self.app_connection)
        self.loadtype_queries = LoadTypeQueries(self.app_connection)

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.vertical_lo = qtw.QVBoxLayout()
        self.loadtype_table = qtw.QTableWidget()
        self.progress_bar = qtw.QProgressBar()
        self.statusbar = qtw.QStatusBar()
        self.create_menus()

    def setup_gui_object_style_names(self):
        self.statusbar.setProperty('Error', False)
        self.statusbar.setStyle(self.statusbar.style())

    def layout_gui_objects(self):
        self.vertical_lo.addWidget(self.toolbar)
        self.vertical_lo.addWidget(self.loadtype_table)
        self.vertical_lo.addWidget(self.progress_bar)
        self.vertical_lo.addWidget(self.statusbar)
        self.setLayout(self.vertical_lo)

    def feature_gui_objects(self):
        self.setGeometry(0, 0, self.app_settings.subwindow_width, self.app_settings.subwindow_height)
        self.setMinimumSize(600, 250)
        #dressing up table
        self.loadtype_table.setColumnCount(2)
        self.loadtype_table.setColumnHidden(0, True)
        self.loadtype_table.setEditTriggers(qtw.QTableWidget.NoEditTriggers)
        self.loadtype_table.setSelectionMode(qtw.QAbstractItemView.SingleSelection)
        self.loadtype_table.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)
        self.loadtype_table.selectRow(0)
        # self.loadsTable.setCurrentItem(self.loadsTable.item(0, 0))
        self.loadtype_table.setHorizontalHeaderLabels(["TypeId", "Type Of Loads"])
        self.loadtype_table.setColumnWidth(1, 200)
        # settings up progress bar
        self.progress_bar.setValue(0)
        loadtypes_count = self.loadtype_queries.types_count()
        if loadtypes_count != 0:
            self.progress_bar.setRange(0, loadtypes_count)
        else:
            self.progress_bar.setRange(0, 1)
        self.statusbar.showMessage('...')

    def setup_gui_object_events(self):
        self.create_menu_actions()
        self.loadtype_table.cellDoubleClicked.connect(self.view_type_window)

    def activate_controls(self):
        self.delete_action.setEnabled(True)
        self.insert_action.setEnabled(True)
        self.modify_action.setEnabled(True)
        self.view_action.setEnabled(True)
        self.refresh_action.setEnabled(True)

    def deactivate_controls(self):
        self.delete_action.setEnabled(False)
        self.insert_action.setEnabled(False)
        self.modify_action.setEnabled(False)
        self.view_action.setEnabled(False)
        self.refresh_action.setEnabled(False)


    def activate_worker(self):
        self.loadtype_queries.update_windowmessage_signal.connect(self.update_status_bar)
        self.loadtype_worker.update_windowmessage_signal.connect(self.update_status_bar)
        self.loadtype_worker.update_progressbar_signal.connect(self.update_progress_bar)
        self.loadtype_worker.update_nextrow_signal.connect(self.add_row_to_table)
        self.loadtype_worker.start()

    def update_status_bar(self, code, message):
        if code == 100000:
            self.statusbar.setProperty('Error', False)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(message)
            self.loadtype_table.setCurrentCell(0, 0)
            self.refresh_action.setEnabled(True)
        elif code == 100001 or code == 100002:
            self.statusbar.setProperty('Error', False)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(message)
        else:
            self.statusbar.setProperty('Error', True)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(f'Error code: {code}. Error message: {message}')

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def add_row_to_table(self, new_type_instance):
        current_row_count = self.loadtype_table.rowCount()
        self.loadtype_table.insertRow(current_row_count)
        self.fill_row_with_data(current_row_count, new_type_instance)

    def add_row_topof_table(self, loadtype_instance):
        self.loadtype_table.insertRow(0)
        self.fill_row_with_data(0, loadtype_instance)
        self.loadtype_table.setCurrentCell(0, 0)

    def fill_row_with_data(self, row_number, loadtype_instance):
        inserteditemid = qtw.QTableWidgetItem()
        inserteditemid.setData(qtc.Qt.DisplayRole, loadtype_instance.loadtypeid)
        inserteditemid.setTextAlignment(qtc.Qt.AlignCenter)
        self.loadtype_table.setItem(row_number, 0, inserteditemid)

        inserteditemname = qtw.QTableWidgetItem()
        inserteditemname.setData(qtc.Qt.DisplayRole, loadtype_instance.loadtypename)
        inserteditemname.setTextAlignment(qtc.Qt.AlignCenter)
        self.loadtype_table.setItem(row_number, 1, inserteditemname)

    def create_menus(self):
        menubar = qtw.QMenuBar()
        self.toolbar = qtw.QToolBar()
        self.toolbar.setFixedHeight(55)
        self.toolbar.setIconSize(qtc.QSize(50, 50))
        self.file_menu = menubar.addMenu('File')
        self.operation_menu = menubar.addMenu('Operation')
        self.vertical_lo.setMenuBar(menubar)

    def create_menu_actions(self):
        self.exit_action = qtw.QAction(
            (qtg.QIcon(':/icon_exit.png')),
            'Exit', self
        )
        self.delete_action = qtw.QAction(
            (qtg.QIcon(':/icon_delete.png')),
            'Delete Load Confirmation', self
        )
        self.insert_action = qtw.QAction(
            (qtg.QIcon(':/icon_insert.png')),
            'Insert Load Confirmation', self
        )
        self.modify_action = qtw.QAction(
            (qtg.QIcon(':/icon_modify.png')),
            'Modify Load Confirmation', self
        )
        self.view_action = qtw.QAction(
            (qtg.QIcon(':/icon_view.png')),
            'View Load Confirmation', self
        )
        self.refresh_action = qtw.QAction(
            (qtg.QIcon(':/icon_refresh.png')),
            'Refresh Table', self
        )
        self.refresh_action.setEnabled(False)
        self.exit_action.triggered.connect(self.close_window)
        self.delete_action.triggered.connect(self.delete_type_window)
        self.insert_action.triggered.connect(self.insert_type_window)
        self.modify_action.triggered.connect(self.modify_type_window)
        self.view_action.triggered.connect(self.view_type_window)
        self.refresh_action.triggered.connect(self.refresh_type_window)
        self.file_menu.addAction(self.exit_action)
        self.operation_menu.addAction(self.delete_action)
        self.operation_menu.addAction(self.insert_action)
        self.operation_menu.addAction(self.modify_action)
        self.operation_menu.addAction(self.view_action)
        self.toolbar.addAction(self.exit_action)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.delete_action)
        self.toolbar.addAction(self.insert_action)
        self.toolbar.addAction(self.modify_action)
        self.toolbar.addAction(self.view_action)
        self.toolbar.addAction(self.refresh_action)

    def close_window(self):
        self.parentWidget().close()


    def delete_type_window(self):
        selected_row = self.loadtype_table.currentRow()
        if selectedIDItem := self.loadtype_table.item(selected_row, 0):
            requested_type= self.loadtype_queries.get_loadtype_byid(selectedIDItem.text())
            if isinstance(requested_type, LoadTypeInstance):
                delete_type_window = NewLoadTypeDialog(
                    self.app_settings, LCSettings.Settings.DELETE, requested_type
                )
                if delete_type_window.exec_() == qtw.QDialog.Accepted:
                    operation_returm_code = self.loadtype_queries.delete_loadtype(requested_type)
                    if operation_returm_code == 0:
                        qtw.QMessageBox(
                            qtw.QMessageBox.Information,
                            "Success", "Type was deleted",
                            qtw.QMessageBox.Yes
                        ).exec_()
                        self.loadtype_table.removeRow(selected_row)
                        self.select_nearby_row(selected_row)
                else:
                    print('cancel')
            else:
                self.loadtype_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                # self.statusbar.showMessage('Error code: -1. Error message: None selected row')
                #logging this error event

    def insert_type_window(self):
        insert_type_window = NewLoadTypeDialog(
            self.app_settings, LCSettings.Settings.INSERT, loadtype_queries=self.loadtype_queries
        )
        if insert_type_window.exec_() == qtw.QDialog.Accepted:
            self.add_row_topof_table(insert_type_window.new_loadtype_instance)
        else:
            print('cancel')


    def modify_type_window(self):
        selected_row = self.loadtype_table.currentRow()
        if selectedIDItem := self.loadtype_table.item(selected_row, 0):
            requested_type = self.loadtype_queries.get_loadtype_byid(selectedIDItem.text())
            if isinstance(requested_type, LoadTypeInstance):
                modify_type_window = NewLoadTypeDialog(
                    self.app_settings, LCSettings.Settings.MODIFY, requested_type, self.loadtype_queries
                )
                if modify_type_window.exec_() == qtw.QDialog.Accepted:
                    self.fill_row_with_data(selected_row, modify_type_window.modify_loadtype_instance)
                else:
                    print('cancel')
            else:
                self.loadtype_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                #logging this error eve

    def view_type_window(self):
        selected_row = self.loadtype_table.currentRow()
        if selectedIDItem := self.loadtype_table.item(selected_row, 0):
            requested_type = self.loadtype_queries.get_loadtype_byid(selectedIDItem.text())
            if isinstance(requested_type, LoadTypeInstance):
                view_type_window = NewLoadTypeDialog(
                    self.app_settings, LCSettings.Settings.VIEW, requested_type
                )
                if view_type_window.exec_() == qtw.QDialog.Accepted:
                    pass
                else:
                    pass
            else:
                self.loadtype_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                #logging this error event

    def refresh_type_window(self):
        if self.loadtype_worker.isRunning():
            self.loadtype_worker.quit()
            self.loadtype_table.setRowCount(0)
            self.loadtype_worker.start()
        else:
            self.loadtype_table.setRowCount(0)
            self.loadtype_worker.start()

    def select_nearby_row(self, delete_row):
        row_count = self.loadtype_table.rowCount()
        if row_count != 0:
            if delete_row == row_count:
                self.loadtype_table.setCurrentCell(delete_row - 1, 0)
            else:
                self.loadtype_table.setCurrentCell(delete_row, 0)


class ShipperWidget(qtw.QWidget):

    def __init__(self, app_settings, app_connection):
        super().__init__()
        # create "load from json" function for Settings class
        # self.app_connection = self.assembleConnection(self.app_settings)
        self.setup_supporting_vars(app_settings, app_connection)
        self.setup_gui()
        self.show()
        self.activate_worker()

    def setup_supporting_vars(self, app_settings, app_connection):
        self.app_settings = app_settings
        self.app_connection = app_connection
        self.shipper_worker = ShipperWorker(self.app_connection)
        self.shipper_queries = ShipperQueries(self.app_connection)

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.vertical_lo = qtw.QVBoxLayout()
        self.shipper_table = qtw.QTableWidget()
        self.progress_bar = qtw.QProgressBar()
        self.statusbar = qtw.QStatusBar()
        self.create_menus()

    def setup_gui_object_style_names(self):
        self.statusbar.setProperty('Error', False)
        self.statusbar.setStyle(self.statusbar.style())

    def layout_gui_objects(self):
        self.vertical_lo.addWidget(self.toolbar)
        self.vertical_lo.addWidget(self.shipper_table)
        self.vertical_lo.addWidget(self.progress_bar)
        self.vertical_lo.addWidget(self.statusbar)
        self.setLayout(self.vertical_lo)

    def feature_gui_objects(self):
        self.setGeometry(0, 0, self.app_settings.subwindow_width, self.app_settings.subwindow_height)
        self.setMinimumSize(600, 250)
        #dressing up table
        self.shipper_table.setColumnCount(11)
        self.shipper_table.setColumnHidden(0, True)
        self.shipper_table.setEditTriggers(qtw.QTableWidget.NoEditTriggers)
        self.shipper_table.setSelectionMode(qtw.QAbstractItemView.SingleSelection)
        self.shipper_table.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)
        self.shipper_table.selectRow(0)
        # self.usersTable.setCurrentItem(self.loadsTable.item(0, 0))
        self.shipper_table.setHorizontalHeaderLabels([
            "Shipper ID", "Shipper Name", "Address", "City",
            "State", "Country", "Postal Code",
            "Phone", "Fax", "Toll Free Phone",
            "Shipper Contact"
        ])
        header = self.shipper_table.horizontalHeader()
        header.setSectionResizeMode(0, qtw.QHeaderView.Fixed)
        header.setSectionResizeMode(1, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(2, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(3, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(4, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(5, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(6, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(7, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(8, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(9, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(10, qtw.QHeaderView.Stretch)
        #  settings up progress bar
        self.progress_bar.setValue(0)
        shippers_count = self.shipper_queries.shippers_count()
        if shippers_count != 0:
            self.progress_bar.setRange(0, shippers_count)
        else:
            self.progress_bar.setRange(0, 1)
        self.statusbar.showMessage('...')

    def setup_gui_object_events(self):
        self.create_menu_actions()
        self.shipper_table.cellDoubleClicked.connect(self.view_shipper_window)

    def activate_controls(self):
        self.delete_action.setEnabled(True)
        self.insert_action.setEnabled(True)
        self.modify_action.setEnabled(True)
        self.view_action.setEnabled(True)
        self.refresh_action.setEnabled(True)

    def deactivate_controls(self):
        self.delete_action.setEnabled(False)
        self.insert_action.setEnabled(False)
        self.modify_action.setEnabled(False)
        self.view_action.setEnabled(False)
        self.refresh_action.setEnabled(False)

    def activate_worker(self):
        self.shipper_queries.update_windowmessage_signal.connect(self.update_status_bar)
        self.shipper_worker.update_windowmessage_signal.connect(self.update_status_bar)
        self.shipper_worker.update_progressbar_signal.connect(self.update_progress_bar)
        self.shipper_worker.update_nextrow_signal.connect(self.add_row_to_table)
        self.shipper_worker.start()

    def update_status_bar(self, code, message):
        if code == 100000:
            self.statusbar.setProperty('Error', False)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(message)
            self.shipper_table.setCurrentCell(0, 0)
            self.refresh_action.setEnabled(True)
        elif code == 100001 or code == 100002:
            self.statusbar.setProperty('Error', False)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(message)
        else:
            self.statusbar.setProperty('Error', True)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(f'Error code: {code}. Error message: {message}')

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def add_row_to_table(self, shipper_instance):
        row_number = self.shipper_table.rowCount()
        self.shipper_table.insertRow(row_number)
        self.fill_row_with_data(row_number, shipper_instance)

    def add_row_topof_table(self, shipper_instance):
        self.shipper_table.insertRow(0)
        self.fill_row_with_data(0, shipper_instance)
        self.shipper_table.setCurrentCell(0, 0)

    def fill_row_with_data(self, row_number, shipper_instance):
        inserteditemid = qtw.QTableWidgetItem()
        inserteditemid.setData(qtc.Qt.DisplayRole, shipper_instance.shipperid)
        inserteditemid.setTextAlignment(qtc.Qt.AlignCenter)
        self.shipper_table.setItem(row_number, 0, inserteditemid)

        inserteditemname = qtw.QTableWidgetItem()
        inserteditemname.setData(qtc.Qt.DisplayRole, shipper_instance.shippername)
        inserteditemname.setTextAlignment(qtc.Qt.AlignCenter)
        self.shipper_table.setItem(row_number, 1, inserteditemname)

        inserteditemaddress = qtw.QTableWidgetItem()
        inserteditemaddress.setData(qtc.Qt.DisplayRole, shipper_instance.shipperaddress)
        inserteditemaddress.setTextAlignment(qtc.Qt.AlignCenter)
        self.shipper_table.setItem(row_number, 2, inserteditemaddress)

        inserteditemcity = qtw.QTableWidgetItem()
        inserteditemcity.setData(qtc.Qt.DisplayRole, shipper_instance.shippercity)
        inserteditemcity.setTextAlignment(qtc.Qt.AlignCenter)
        self.shipper_table.setItem(row_number, 3, inserteditemcity)

        inserteditemstate = qtw.QTableWidgetItem()
        inserteditemstate.setData(qtc.Qt.DisplayRole, shipper_instance.shipperstate)
        inserteditemstate.setTextAlignment(qtc.Qt.AlignCenter)
        self.shipper_table.setItem(row_number, 4, inserteditemstate)

        inserteditemcountry = qtw.QTableWidgetItem()
        inserteditemcountry.setData(qtc.Qt.DisplayRole, shipper_instance.shippercountry)
        inserteditemcountry.setTextAlignment(qtc.Qt.AlignCenter)
        self.shipper_table.setItem(row_number, 5, inserteditemcountry)

        inserteditempostalcode = qtw.QTableWidgetItem()
        inserteditempostalcode.setData(qtc.Qt.DisplayRole, shipper_instance.shipperpostalcode)
        inserteditempostalcode.setTextAlignment(qtc.Qt.AlignCenter)
        self.shipper_table.setItem(row_number, 6, inserteditempostalcode)

        inserteditemphone = qtw.QTableWidgetItem()
        inserteditemphone.setData(qtc.Qt.DisplayRole, shipper_instance.shipperphone)
        inserteditemphone.setTextAlignment(qtc.Qt.AlignCenter)
        self.shipper_table.setItem(row_number, 7, inserteditemphone)

        inserteditemfax = qtw.QTableWidgetItem()
        inserteditemfax.setData(qtc.Qt.DisplayRole, shipper_instance.shipperfax)
        inserteditemfax.setTextAlignment(qtc.Qt.AlignCenter)
        self.shipper_table.setItem(row_number, 8, inserteditemfax)

        inserteditemtollfree = qtw.QTableWidgetItem()
        inserteditemtollfree.setData(qtc.Qt.DisplayRole, shipper_instance.shippertollfree)
        inserteditemtollfree.setTextAlignment(qtc.Qt.AlignCenter)
        self.shipper_table.setItem(row_number, 9, inserteditemtollfree)

        inserteditemcontact = qtw.QTableWidgetItem()
        inserteditemcontact.setData(qtc.Qt.DisplayRole, shipper_instance.shippercontact)
        inserteditemcontact.setTextAlignment(qtc.Qt.AlignCenter)
        self.shipper_table.setItem(row_number, 10, inserteditemcontact)

    def create_menus(self):
        menubar = qtw.QMenuBar()
        self.toolbar = qtw.QToolBar()
        self.toolbar.setFixedHeight(55)
        self.toolbar.setIconSize(qtc.QSize(50, 50))
        self.file_menu = menubar.addMenu('File')
        self.operation_menu = menubar.addMenu('Operation')
        self.vertical_lo.setMenuBar(menubar)

    def create_menu_actions(self):
        self.exit_action = qtw.QAction(
            (qtg.QIcon(':/icon_exit.png')),
            'Exit', self
        )
        self.delete_action = qtw.QAction(
            (qtg.QIcon(':/icon_delete.png')),
            'Delete Load Confirmation', self
        )
        self.insert_action = qtw.QAction(
            (qtg.QIcon(':/icon_insert.png')),
            'Insert Load Confirmation', self
        )
        self.modify_action = qtw.QAction(
            (qtg.QIcon(':/icon_modify.png')),
            'Modify Load Confirmation', self
        )
        self.view_action = qtw.QAction(
            (qtg.QIcon(':/icon_view.png')),
            'View Load Confirmation', self
        )
        self.refresh_action = qtw.QAction(
            (qtg.QIcon(':/icon_refresh.png')),
            'Refresh Table', self
        )
        self.refresh_action.setEnabled(False)
        self.exit_action.triggered.connect(self.close_window)
        self.delete_action.triggered.connect(self.delete_shipper_window)
        self.insert_action.triggered.connect(self.insert_shipper_window)
        self.modify_action.triggered.connect(self.modify_shipper_window)
        self.view_action.triggered.connect(self.view_shipper_window)
        self.refresh_action.triggered.connect(self.refresh_shipper_window)
        self.file_menu.addAction(self.exit_action)
        self.operation_menu.addAction(self.delete_action)
        self.operation_menu.addAction(self.insert_action)
        self.operation_menu.addAction(self.modify_action)
        self.operation_menu.addAction(self.view_action)
        self.toolbar.addAction(self.exit_action)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.delete_action)
        self.toolbar.addAction(self.insert_action)
        self.toolbar.addAction(self.modify_action)
        self.toolbar.addAction(self.view_action)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.refresh_action)

    def close_window(self):
        self.parentWidget().close()

    def delete_shipper_window(self):
        selected_row = self.shipper_table.currentRow()
        if selectedIDItem := self.shipper_table.item(selected_row, 0):
            requested_shipper= self.shipper_queries.get_shipper_by_id(selectedIDItem.text())
            if isinstance(requested_shipper, ShipperInstance):
                delete_shipper_window = NewShipperDialog(
                    self.app_settings, LCSettings.Settings.DELETE, requested_shipper
                )
                if delete_shipper_window.exec_() == qtw.QDialog.Accepted:
                    operation_returm_code = self.shipper_queries.delete_shipper(requested_shipper)
                    if operation_returm_code == 0:
                        qtw.QMessageBox(
                            qtw.QMessageBox.Information,
                            "Success", "Shipper was deleted",
                            qtw.QMessageBox.Yes
                        ).exec_()
                        self.shipper_table.removeRow(selected_row)
                        self.select_nearby_row(selected_row)
                else:
                    print('cancel')
            else:
                self.shipper_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                # self.statusbar.showMessage('Error code: -1. Error message: None selected row')
                #logging this error event

    def insert_shipper_window(self):
        insert_shipper_window = NewShipperDialog(
            self.app_settings, LCSettings.Settings.INSERT, shipper_queries=self.shipper_queries
        )
        if insert_shipper_window.exec_() == qtw.QDialog.Accepted:
            self.add_row_topof_table(insert_shipper_window.new_shipper_instance)
        else:
            print('cancel')

    def modify_shipper_window(self):
        selected_row = self.shipper_table.currentRow()
        if selectedIDItem := self.shipper_table.item(selected_row, 0):
            requested_shipper = self.shipper_queries.get_shipper_by_id(selectedIDItem.text())
            if isinstance(requested_shipper, ShipperInstance):
                modify_shipper_window = NewShipperDialog(
                    self.app_settings, LCSettings.Settings.MODIFY, requested_shipper, self.shipper_queries
                )
                if modify_shipper_window.exec_() == qtw.QDialog.Accepted:
                    self.fill_row_with_data(selected_row, modify_shipper_window.modify_shipper_instance)
                else:
                    print('cancel')
            else:
                self.shipper_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                #logging this error eve

    def view_shipper_window(self):
        selected_row = self.shipper_table.currentRow()
        if selectedIDItem := self.shipper_table.item(selected_row, 0):
            requested_shipper = self.shipper_queries.get_shipper_by_id(selectedIDItem.text())
            if isinstance(requested_shipper, ShipperInstance):
                view_shipper_window = NewShipperDialog(
                    self.app_settings, LCSettings.Settings.VIEW, requested_shipper
                )
                if view_shipper_window.exec_() == qtw.QDialog.Accepted:
                    pass
                else:
                    pass
            else:
                self.shipper_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                #logging this error event

    def refresh_shipper_window(self):
        if self.shipper_worker.isRunning():
            self.shipper_worker.quit()
            self.shipper_table.setRowCount(0)
            self.shipper_worker.start()
        else:
            self.shipper_table.setRowCount(0)
            self.shipper_worker.start()

    def select_nearby_row(self, delete_row):
        row_count = self.shipper_table.rowCount()
        if row_count != 0:
            if delete_row == row_count:
                self.shipper_table.setCurrentCell(delete_row - 1, 0)
            else:
                self.shipper_table.setCurrentCell(delete_row, 0)


class UsersWidget(qtw.QWidget):

    def __init__(self, app_settings, app_connection):
        super().__init__()
        # create "load from json" function for Settings class
        # self.app_connection = self.assembleConnection(self.app_settings)
        self.setup_supporting_vars(app_settings, app_connection)
        self.setup_gui()
        self.show()
        self.activate_worker()

    def setup_supporting_vars(self, app_settings, app_connection):
        self.app_settings = app_settings
        self.app_connection = app_connection
        self.users_worker= UsersWorker(self.app_connection)
        self.users_queries = UsersQueries(self.app_connection)

    def setup_gui(self):
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.vertical_lo = qtw.QVBoxLayout()
        self.users_table = qtw.QTableWidget()
        self.progress_bar = qtw.QProgressBar()
        self.statusbar = qtw.QStatusBar()
        self.create_menus()

    def setup_gui_object_style_names(self):
        self.statusbar.setProperty('Error', False)
        self.statusbar.setStyle(self.statusbar.style())

    def layout_gui_objects(self):
        self.vertical_lo.addWidget(self.toolbar)
        self.vertical_lo.addWidget(self.users_table)
        self.vertical_lo.addWidget(self.progress_bar)
        self.vertical_lo.addWidget(self.statusbar)
        self.setLayout(self.vertical_lo)

    def feature_gui_objects(self):
        self.setGeometry(0, 0, self.app_settings.subwindow_width, self.app_settings.subwindow_height)
        self.setMinimumSize(600, 250)
        #dressing up table
        self.users_table.setColumnCount(4)
        self.users_table.setColumnHidden(0, True)
        self.users_table.setEditTriggers(qtw.QTableWidget.NoEditTriggers)
        self.users_table.setSelectionMode(qtw.QAbstractItemView.SingleSelection)
        self.users_table.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)
        self.users_table.selectRow(0)
        self.users_table.setHorizontalHeaderLabels([
            "User Id", "First Name", "Last Name", "Password/Hashcode"
        ])
        header = self.users_table.horizontalHeader()
        # header.setSectionResizeMode(0, qtw.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(1, qtw.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(2, qtw.QHeaderView.ResizeToContents)
        #  settings up progress bar
        self.progress_bar.setValue(0)
        users_count = self.users_queries.users_count()
        if users_count != 0:
            self.progress_bar.setRange(0, users_count)
        else:
            self.progress_bar.setRange(0, 1)
        self.statusbar.showMessage('...')

    def setup_gui_object_events(self):
        self.create_menu_actions()
        self.users_table.cellDoubleClicked.connect(self.view_user_window)

    def activate_controls(self):
        self.delete_action.setEnabled(True)
        self.insert_action.setEnabled(True)
        self.modify_action.setEnabled(True)
        self.view_action.setEnabled(True)
        self.refresh_action.setEnabled(True)
        self.userpassword_action.setEnabled(True)

    def deactivate_controls(self):
        self.delete_action.setEnabled(False)
        self.insert_action.setEnabled(False)
        self.modify_action.setEnabled(False)
        self.view_action.setEnabled(False)
        self.refresh_action.setEnabled(False)
        self.userpassword_action.setEnabled(False)

    # Adjusting column's width with resizing window
    def resizeEvent(self, event):
        self.adjust_columns_width()

    def adjust_columns_width(self):
        self.users_table.setColumnWidth(0, 0)
        self.users_table.setColumnWidth(1, int(self.width() * 0.15))
        self.users_table.setColumnWidth(2, int(self.width() * 0.25))
        self.users_table.setColumnWidth(3, int(self.width() * 0.25))

    def activate_worker(self):
        self.users_queries.update_windowmessage_signal .connect(self.update_progress_bar)
        self.users_worker.update_progressbar_signal.connect(self.update_progress_bar)
        self.users_worker.update_nextrow_signal.connect(self.add_row_to_table)
        self.users_worker.update_windowmessage_signal.connect(self.update_status_bar)
        self.users_worker.start()

    def update_status_bar(self, code, message):
        if code == 100000:
            self.statusbar.setProperty('Error', False)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(message)
            self.users_table.setCurrentCell(0, 0)
            self.refresh_action.setEnabled(True)
        elif code == 100001 or code == 100002:
            self.statusbar.setProperty('Error', False)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(message)
        else:
            self.statusbar.setProperty('Error', True)
            self.statusbar.setStyle(self.statusbar.style())
            self.statusbar.showMessage(f'Error code: {code}. Error message: {message}')

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def add_row_to_table(self, new_user_instance):
        current_row_count = self.users_table.rowCount()
        self.users_table.insertRow(current_row_count)
        self.fill_row_with_data(current_row_count, new_user_instance)

    def add_row_topof_table(self, new_user_instance):
        self.users_table.insertRow(0)
        self.fill_row_with_data(0, new_user_instance)
        self.users_table.setCurrentCell(0, 0)

    def fill_row_with_data(self, row_number, user_instance):
        inserteditemid = qtw.QTableWidgetItem()
        inserteditemid.setData(qtc.Qt.DisplayRole, user_instance.userid)
        inserteditemid.setTextAlignment(qtc.Qt.AlignCenter)
        self.users_table.setItem(row_number, 0, inserteditemid)

        inserteditemfname = qtw.QTableWidgetItem()
        inserteditemfname.setData(qtc.Qt.DisplayRole, user_instance.userfname)
        inserteditemfname.setTextAlignment(qtc.Qt.AlignCenter)
        self.users_table.setItem(row_number, 1, inserteditemfname)

        inserteditemsname = qtw.QTableWidgetItem()
        inserteditemsname.setData(qtc.Qt.DisplayRole, user_instance.usersname)
        inserteditemsname.setTextAlignment(qtc.Qt.AlignCenter)
        self.users_table.setItem(row_number, 2, inserteditemsname)

        inserteditempassword = qtw.QTableWidgetItem()
        inserteditempassword.setData(qtc.Qt.DisplayRole, user_instance.password)
        inserteditempassword.setTextAlignment(qtc.Qt.AlignCenter)
        self.users_table.setItem(row_number, 3, inserteditempassword)

    def create_menus(self):
        menubar = qtw.QMenuBar()
        self.toolbar = qtw.QToolBar()
        self.toolbar.setFixedHeight(55)
        self.toolbar.setIconSize(qtc.QSize(50, 50))
        self.file_menu = menubar.addMenu('File')
        self.operation_menu = menubar.addMenu('Operation')
        self.vertical_lo.setMenuBar(menubar)

    def create_menu_actions(self):
        self.exit_action = qtw.QAction(
            (qtg.QIcon(':/icon_exit.png')),
            'Exit', self
        )
        self.delete_action = qtw.QAction(
            (qtg.QIcon(':/icon_delete.png')),
            'Delete Load Confirmation', self
        )
        self.insert_action = qtw.QAction(
            (qtg.QIcon(':/icon_insert.png')),
            'Insert Load Confirmation', self
        )
        self.modify_action = qtw.QAction(
            (qtg.QIcon(':/icon_modify.png')),
            'Modify Load Confirmation', self
        )
        self.view_action = qtw.QAction(
            (qtg.QIcon(':/icon_view.png')),
            'View Load Confirmation', self
        )
        self.refresh_action = qtw.QAction(
            (qtg.QIcon(':/icon_refresh.png')),
            'Refresh Table', self
        )
        self.userpassword_action = qtw.QAction(
            (qtg.QIcon(':/icon_user_password.png')),
            'Change Users Password', self
        )
        self.refresh_action.setEnabled(False)
        self.exit_action.triggered.connect(self.close_window)
        self.delete_action.triggered.connect(self.delete_user_window)
        self.insert_action.triggered.connect(self.insert_user_window)
        self.modify_action.triggered.connect(self.modify_user_window)
        self.view_action.triggered.connect(self.view_user_window)
        self.userpassword_action.triggered.connect(self.change_user_password)
        self.refresh_action.triggered.connect(self.refresh_user_window)
        self.file_menu.addAction(self.exit_action)
        self.operation_menu.addAction(self.delete_action)
        self.operation_menu.addAction(self.insert_action)
        self.operation_menu.addAction(self.modify_action)
        self.operation_menu.addAction(self.view_action)
        self.operation_menu.addAction(self.userpassword_action)
        self.toolbar.addAction(self.exit_action)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.delete_action)
        self.toolbar.addAction(self.insert_action)
        self.toolbar.addAction(self.modify_action)
        self.toolbar.addAction(self.view_action)
        self.toolbar.addAction(self.userpassword_action)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.refresh_action)

    def close_window(self):
        self.parentWidget().close()

    def delete_user_window(self):
        selected_row = self.users_table.currentRow()
        if selectedIDItem := self.users_table.item(selected_row, 0):
            requested_user = self.users_queries.get_user_byid(selectedIDItem.text())
            if isinstance(requested_user, UserInstance):
                delete_user_window = NewUserDialog(
                    self.app_settings, LCSettings.Settings.DELETE, requested_user
                )
                if delete_user_window.exec_() == qtw.QDialog.Accepted:
                    operation_returm_code = self.users_queries.delete_user(requested_user)
                    if operation_returm_code == 0:
                        qtw.QMessageBox(
                            qtw.QMessageBox.Information,
                            "Success", "User was deleted",
                            qtw.QMessageBox.Yes
                        ).exec_()
                        self.users_table.removeRow(selected_row)
                        self.select_nearby_row(selected_row)
                else:
                    print('cancel')
            else:
                self.users_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                # self.statusbar.showMessage('Error code: -1. Error message: None selected row')
                #logging this error event

    def insert_user_window(self):
        insert_user_window = NewUserDialog(
            self.app_settings, LCSettings.Settings.INSERT, users_queries=self.users_queries
        )
        if insert_user_window.exec_() == qtw.QDialog.Accepted:
            self.add_row_topof_table(insert_user_window.new_user_instance)
        else:
            print('cancel')


    def modify_user_window(self):
        selected_row = self.users_table.currentRow()
        if selectedIDItem := self.users_table.item(selected_row, 0):
            requested_user = self.users_queries.get_user_byid(selectedIDItem.text())
            if isinstance(requested_user, UserInstance):
                modify_user_window = NewUserDialog(
                    self.app_settings, LCSettings.Settings.MODIFY, requested_user, self.users_queries
                )
                if modify_user_window.exec_() == qtw.QDialog.Accepted:
                    self.fill_row_with_data(selected_row, modify_user_window.modify_user_instance)
                else:
                    print('cancel')
            else:
                self.users_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                #logging this error eve

    def view_user_window(self):
        selected_row = self.users_table.currentRow()
        selected_id_item = self.users_table.item(selected_row, 0)
        if selected_id_item is not None:
            requested_user = self.users_queries.get_user_byid(selected_id_item.text())
            if isinstance(requested_user, UserInstance):
                view_user_window = NewUserDialog(
                    self.app_settings, LCSettings.Settings.VIEW, requested_user
                )
                if view_user_window.exec_() == qtw.QDialog.Accepted:
                    pass
                else:
                    pass
            else:
                self.users_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                #logging this error event

    def refresh_user_window(self):
        if self.users_worker.isRunning():
            self.users_worker.quit()
            self.users_table.setRowCount(0)
            self.users_worker.start()
        else:
            self.users_table.setRowCount(0)
            self.users_worker.start()

    def select_nearby_row(self, delete_row):
        row_count = self.users_table.rowCount()
        if row_count >= 1 and delete_row != row_count :
            self.users_table.setCurrentCell(delete_row, 0)
        elif row_count >= 1 and delete_row == row_count :
            self.users_table.setCurrentCell(delete_row - 1, 0)


    def change_user_password(self):
        selected_row = self.users_table.currentRow()
        selected_id_item = self.users_table.item(selected_row, 0)
        if selected_id_item is not None:
            requested_user = self.users_queries.get_user_byid(selected_id_item.text())
            if isinstance(requested_user, UserInstance):
                change_password_window = NewPasswordDialog(
                    self.app_settings,
                    forcepassword_flag=True,
                    new_user_instance=requested_user,
                    users_queries=self.users_queries
                )
                if change_password_window.exec_() == qtw.QDialog.Accepted:
                    #retrieve new hash. for now simply printing "new password assigned"
                    requested_user.password = "New hash generated. Refresh page to see it."
                    self.fill_row_with_data(selected_row, requested_user)
                else:
                    print('cancel')
                # change_password_window.exec_()

            else:
                self.users_queries.update_windowmessage_signal.emit(
                    -100000,
                    'Record with such ID does not exist\n'
                    'Try refreshing the data.'
                )
                #logging this error event


