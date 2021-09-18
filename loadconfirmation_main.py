import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import loadconfirmation_settings as LCSettings
import login_window as lgnw
from core.workers.allworkers import LoadConfirmationConnectToDatabase
from core.workers.allqueries import UsersQueries
from core.widgets.allwidgets import (LoadTypeWidget, ShipperWidget, CarrierWidget,
                                     ConsigneeWidget, LoadConfirmationWidget, BrokerWidget,
                                     UsersWidget, CurrencyWidget)
from core.newdialog.alldialogs import NewPasswordDialog
from resources.icons import loadconfirmation_resources

class LoadConfirmationMain(qtw.QMainWindow):


    def __init__(self, app_settings):
        super().__init__()
        self.setup_supporting_vars(app_settings)
        self.assemble_conn_in_thread()
        self.setup_gui()


    def setup_supporting_vars(self, app_settings):
        """Misc variables"""
        self.app_settings = app_settings
        self.is_connection_valid = False


    def assemble_conn_in_thread(self):
        """Function creates separate thread to establish connection to database

        Connection class has custom signals in it:
            1) connection_signal
            2) windowmessage_signal
        These signals are connected to slots/functions: update_connection and update_status_bar respectively.

        """
        self.app_connection = None
        self.connection_worker_ctd = LoadConfirmationConnectToDatabase(self.app_settings)
        self.connection_worker_ctd.connection_signal.connect(self.update_connection)
        self.connection_worker_ctd.windowmessage_signal.connect(self.update_status_bar)
        self.connection_worker_ctd.start()


    def restart_assemble_conn_in_thread(self):
        """Function re-starts the thread, responsible for establishing database connection"""
        self.connection_worker_ctd.start()


    def update_connection(self, app_connection):
        """Function is used to recover connection variable seamlessly, after lost and re-established connection"""
        self.app_connection = app_connection


    def update_status_bar(self, code, message):
        """Function posts updated messages to the statusbar

        In order to change the color of the message, style has to be updated as well
        """
        self.connectivity_change(code=code)
        if code > 0:
            self.statusBar().setProperty('Error', False)
            self.statusBar().setStyle(self.statusBar().style())
            self.statusBar().showMessage(message)
        else:
            self.statusBar().setProperty('Error', True)
            self.statusBar().setStyle(self.statusBar().style())
            self.statusBar().showMessage(message)
            qtc.QTimer.singleShot(5000, lambda: self.assemble_conn_in_thread())

    def setup_gui(self):
        """Function that runs sequence of functions to create GUI"""
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        """Create MDI containers and menu bar"""
        self.mdi = qtw.QMdiArea()
        self.create_menus()

    def setup_gui_object_style_names(self):
        self.statusBar().setProperty('Error', False)

    def feature_gui_objects(self):
        """Setting up initial features of the GUI components"""
        self.setWindowTitle('Load Confirmation Generator')
        self.setGeometry(0, 0, app_settings.mainwindow_width, app_settings.mainwindow_height)
        self.setMinimumSize(600, 250)
        self.statusBar().showMessage('Establishing connection...')

    def layout_gui_objects(self):
        """Setup layouts"""
        self.setCentralWidget(self.mdi)

    def setup_gui_object_events(self):
        self.create_menu_actions()

    def create_menus(self):
        """Function creates menu """
        menu = self.menuBar()
        self.toolbar = self.addToolBar("mainToolBar")
        self.toolbar.setAllowedAreas(qtc.Qt.TopToolBarArea)
        self.toolbar.setFixedHeight(55)
        self.toolbar.setIconSize(qtc.QSize(50, 50))
        self.file_menu = menu.addMenu('File')
        self.library_menu = menu.addMenu('Library')
        self.administration_menu = menu.addMenu('Administration')

    def create_menu_actions(self):
        """Function creates menu actions

        Icon resources are referenced to to objects file loadconfirmation_resources.py
        that was generated based on resources.qrc file and pyrcc5 utility
        """
        self.exit_action = qtw.QAction((qtg.QIcon(':/icon_exit')), 'Exit', self)
        self.carrier_action = qtw.QAction((qtg.QIcon(':/icon_carrier')), 'Carrier', self)
        self.shipper_action = qtw.QAction((qtg.QIcon(':/icon_shipper')), 'Shipper', self)
        self.consignee_action = qtw.QAction((qtg.QIcon(':/icon_consignee')), 'Consignee', self)
        self.broker_action = qtw.QAction((qtg.QIcon(':/icon_broker')), 'Custom Broker', self)
        self.loadtype_action = qtw.QAction((qtg.QIcon(':/icon_loadtype')), 'Load Type', self)
        self.currency_action = qtw.QAction((qtg.QIcon(':/icon_currency')), 'Currency', self)
        self.loadconfirmation_action = qtw.QAction((qtg.QIcon(':/icon_loadconfirmation')), 'Load Confirmation', self)
        self.users_action = qtw.QAction((qtg.QIcon(':/icon_users')), 'Users', self)
        self.mypassword_action = qtw.QAction((qtg.QIcon(':/icon_my_password')), 'Change my password', self)
        #file menu
        self.file_menu.addAction(self.exit_action)
        # library menu
        self.library_menu.addAction(self.carrier_action)
        self.library_menu.addAction(self.shipper_action)
        self.library_menu.addAction(self.consignee_action)
        self.library_menu.addAction(self.broker_action)
        self.library_menu.addAction(self.loadtype_action)
        self.library_menu.addAction(self.loadconfirmation_action)
        self.library_menu.addAction(self.currency_action)
        #administration menu
        self.administration_menu.addAction(self.users_action)
        self.administration_menu.addAction(self.mypassword_action)
        self.toolbar.addAction(self.exit_action)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.carrier_action)
        self.toolbar.addAction(self.shipper_action)
        self.toolbar.addAction(self.consignee_action)
        self.toolbar.addAction(self.broker_action)
        self.toolbar.addAction(self.loadtype_action)
        self.toolbar.addAction(self.currency_action)
        self.toolbar.addAction(self.loadconfirmation_action)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.users_action)
        self.toolbar.addAction(self.mypassword_action)

        self.file_menu.triggered[qtw.QAction].connect(self.action_file_triggered)
        self.library_menu.triggered[qtw.QAction].connect(self.action_library_triggered)
        self.administration_menu.triggered[qtw.QAction].connect(self.action_administration_triggered)


    def action_file_triggered(self, source):
        if source.text() == 'Exit':
            sys.exit()

    def action_library_triggered(self, source):
        """Function process menu and toolbar actions"""
        if source.text() == 'Carrier':
            carrier_sub_window = qtw.QMdiSubWindow()
            carrier_sub_window.setWidget(CarrierWidget(self.app_settings, self.app_connection))
            carrier_sub_window.setAttribute(qtc.Qt.WA_DeleteOnClose)
            carrier_sub_window.setWindowTitle('Carriers')
            self.mdi.addSubWindow(carrier_sub_window)
            carrier_sub_window.setGeometry(0, 0, self.app_settings.subwindow_width, self.app_settings.subwindow_height)
            carrier_sub_window.show()
        elif source.text() == 'Shipper':
            shipper_sub_window = qtw.QMdiSubWindow()
            shipper_sub_window.setWidget(ShipperWidget(self.app_settings, self.app_connection))
            shipper_sub_window.setAttribute(qtc.Qt.WA_DeleteOnClose)
            shipper_sub_window.setWindowTitle('Shippers')
            self.mdi.addSubWindow(shipper_sub_window)
            shipper_sub_window.setGeometry(0, 0, self.app_settings.subwindow_width, self.app_settings.subwindow_height)
            shipper_sub_window.show()
        elif source.text() == 'Consignee':
            consignee_sub_window = qtw.QMdiSubWindow()
            consignee_sub_window.setWidget(ConsigneeWidget(self.app_settings, self.app_connection))
            consignee_sub_window.setAttribute(qtc.Qt.WA_DeleteOnClose)
            consignee_sub_window.setWindowTitle('Consignees')
            self.mdi.addSubWindow(consignee_sub_window)
            consignee_sub_window.setGeometry(0, 0, self.app_settings.subwindow_width, self.app_settings.subwindow_height)
            consignee_sub_window.show()
        elif source.text() == 'Custom Broker':
            broker_sub_window = qtw.QMdiSubWindow()
            broker_sub_window.setWidget(BrokerWidget(self.app_settings, self.app_connection))
            broker_sub_window.setAttribute(qtc.Qt.WA_DeleteOnClose)
            broker_sub_window.setWindowTitle('Brokers')
            self.mdi.addSubWindow(broker_sub_window)
            broker_sub_window.setGeometry(0, 0, self.app_settings.smallsubwindow_width, self.app_settings.smallsubwindow_height)
            broker_sub_window.show()
        elif source.text() == 'Load Type':
            loadtype_sub_window = qtw.QMdiSubWindow()
            loadtype_sub_window.setWidget(LoadTypeWidget(self.app_settings, self.app_connection))
            loadtype_sub_window.setWindowTitle('Type of Loads')
            self.mdi.addSubWindow(loadtype_sub_window)
            loadtype_sub_window.setGeometry(0, 0, self.app_settings.smallsubwindow_width, self.app_settings.smallsubwindow_height)
            loadtype_sub_window.show()
        elif source.text() == 'Load Confirmation':
            load_confirmation_sub_window = qtw.QMdiSubWindow()
            load_confirmation_sub_window.setWidget(LoadConfirmationWidget(self.app_settings, self.app_connection))
            load_confirmation_sub_window.setWindowTitle('Load Confirmation')
            self.mdi.addSubWindow(load_confirmation_sub_window)
            load_confirmation_sub_window.setGeometry(0, 0, self.app_settings.subwindow_width, self.app_settings.subwindow_height)
            load_confirmation_sub_window.show()
        elif source.text() == 'Currency':
            currency_sub_window = qtw.QMdiSubWindow()
            currency_sub_window.setWidget(CurrencyWidget(self.app_settings, self.app_connection))
            currency_sub_window.setWindowTitle('Currencies')
            self.mdi.addSubWindow(currency_sub_window)
            currency_sub_window.setGeometry(0, 0, self.app_settings.subwindow_width, self.app_settings.subwindow_height)
            currency_sub_window.show()

    def action_administration_triggered(self, source):
        """Function processes administration task

        Two functionalities related to administration are:
        1) Change logged in user password
        2) View all users and their passwords. For administrator's eyes only
        """
        if source.text() == 'Users':
            users_sub_window = qtw.QMdiSubWindow()
            users_sub_window.setWidget(UsersWidget(self.app_settings, self.app_connection))
            users_sub_window.setWindowTitle('Users')
            self.mdi.addSubWindow(users_sub_window)
            users_sub_window.setGeometry(0, 0, self.app_settings.smallsubwindow_width, self.app_settings.smallsubwindow_height)
            users_sub_window.show()
        elif source.text() == 'Change my password':
            users_queries = UsersQueries(self.app_connection)
            change_password_window = NewPasswordDialog(
                    self.app_settings,
                    forcepassword_flag=False,
                    users_queries=users_queries
                )
            change_password_window.exec_()

    def check_loginuser_privileges(self):
        """if login user is not Administrator, disable menu 'Administration' """
        if not self.app_settings.is_privilege_user:
            # self.administration_menu.setEnabled(False)
            self.users_action.setVisible(False)

    def connectivity_change(self, code):
        """Activate/Deactivate menu and toolbar"""
        if (code > 0 and not self.is_connection_valid):
            self.carrier_action.setEnabled(True)
            self.shipper_action.setEnabled(True)
            self.consignee_action.setEnabled(True)
            self.broker_action.setEnabled(True)
            self.loadtype_action.setEnabled(True)
            self.currency_action.setEnabled(True)
            self.loadconfirmation_action.setEnabled(True)
            self.users_action.setEnabled(True)
            self.mypassword_action.setEnabled(True)
            self.activate_all_children()
            self.is_connection_valid = True
        elif (code < 0 and self.is_connection_valid):
            self.carrier_action.setEnabled(False)
            self.shipper_action.setEnabled(False)
            self.consignee_action.setEnabled(False)
            self.broker_action.setEnabled(False)
            self.loadtype_action.setEnabled(False)
            self.currency_action.setEnabled(False)
            self.loadconfirmation_action.setEnabled(False)
            self.users_action.setEnabled(False)
            self.mypassword_action.setEnabled(False)
            self.deactivate_all_children()
            self.is_connection_valid = False

    def activate_all_children(self):
        """Loop runs functions in all MDI children to activate menu and toolbar"""
        for sub_window_child in self.mdi.subWindowList():
            sub_window_child.widget().activate_controls()

    def deactivate_all_children(self):
        """Loop runs functions in all MDI children to deactivate menu and toolbar"""
        for sub_window_child in self.mdi.subWindowList():
            sub_window_child.widget().deactivate_controls()

    def show_login_window(self, splash_window):
        """This function is displaying login windows

        Splash window is kept alive until database connection is established in separate thread.
        Checking is performed every 4 seconds with a help of Qtimer
        After successful authentication, main MDI window is displayed.
        """
        if self.app_connection:
            splash_window.close()
            login_window = lgnw.LoginWindow(self.app_settings, self.app_connection)
            if login_window.exec_() == qtw.QDialog.Accepted:
                self.check_loginuser_privileges()
                self.show()
            else:
                self.close()
        else:
            qtc.QTimer.singleShot(4000, lambda: main_window.show_login_window(splash_window))


def setup_splash_window():
    """Function creates and launches Splash Window

    Splash window is displayed until proper connection to database is established
    """
    splash_pixmap = qtg.QPixmap("resources/icons/volvo-truck.jpg")
    splash_window = qtw.QSplashScreen(splash_pixmap)
    splash_window.show()
    return splash_window


if __name__ == '__main__':
    """Entry point
    
    1. Run splash window
    2. Create instance of setting class based on screen dimensions
    3. Create main MDI window and run function in 2 seconds that displays Login Window.
    (even if database connection is established sonner, 2 sec. delay is honered) 
    """
    app = qtw.QApplication([])
    splash_window = setup_splash_window()
    app_settings = LCSettings.Settings(app.primaryScreen())
    app.setStyleSheet(LCSettings.Settings.style_sheet)
    main_window = LoadConfirmationMain(app_settings)
    qtc.QTimer.singleShot(2000, lambda: main_window.show_login_window(splash_window))
    sys.exit(app.exec_())










