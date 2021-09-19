"""This module solely responsible for  building login window"""
import hashlib
import cx_Oracle
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

class LoginWindow(qtw.QDialog):

    def __init__(self, app_settings, app_connection):
        super().__init__()
        self.setup_supporting_vars(app_settings, app_connection)
        self.setup_gui()

    def setup_supporting_vars(self, app_settings, app_connection):
        """Misc variables"""
        self.users_id_list = []
        self.app_settings = app_settings
        self.app_connection = app_connection
        self.is_privilege = False

    def setup_gui(self):
        """Function that runs sequence of functions to create GUI"""
        self.create_gui_objects()
        self.setup_gui_object_style_names()
        self.layout_gui_objects()
        self.feature_gui_objects()
        self.setup_gui_object_events()

    def create_gui_objects(self):
        self.main_box = qtw.QHBoxLayout()
        self.left_frame = qtw.QFrame()
        self.animation_label = qtw.QLabel()
        self.left_frame_box = qtw.QVBoxLayout()
        self.loginandpass_frame = qtw.QFrame()
        self.users_table_frame = qtw.QFrame()
        self.buttons_frame = qtw.QFrame()
        self.loginandpass_frame_box = qtw.QGridLayout()
        self.users_table_frame_box = qtw.QVBoxLayout()
        self.button_frame_box = qtw.QHBoxLayout()

        self.password_label = qtw.QLabel('Password')
        self.password_editline = qtw.QLineEdit()
        self.users_table = qtw.QTableWidget()
        self.cncl_button = qtw.QPushButton('   Cancel   ')
        self.ok_button = qtw.QPushButton('     OK     ')

    def setup_gui_object_style_names(self):
        self.main_box.setObjectName('frame')
        self.left_frame.setObjectName('frame')
        self.animation_label.setObjectName('frame')

    def layout_gui_objects(self):
        """Setup layouts"""
        self.setLayout(self.main_box)
        # self.main_box.addWidget(self.left_frame, 0, 0, 1, 1)
        # self.main_box.addWidget(self.animation_label, 0, 1, 1, 1)

        self.main_box.addWidget(self.left_frame, 1)
        self.main_box.addWidget(self.animation_label, 1)

        self.left_frame.setLayout(self.left_frame_box)
        self.left_frame_box.addWidget(self.loginandpass_frame)
        self.left_frame_box.addWidget(self.users_table_frame)
        self.left_frame_box.addWidget(self.buttons_frame)

        self.loginandpass_frame.setLayout(self.loginandpass_frame_box)
        self.users_table_frame.setLayout(self.users_table_frame_box)
        self.buttons_frame.setLayout(self.button_frame_box)

        self.loginandpass_frame_box.addWidget(self.password_label, 0, 0, 1, 1)
        self.loginandpass_frame_box.addWidget(self.password_editline, 0, 1, 1, 1)

        self.users_table_frame_box.addWidget(self.users_table)

        self.button_frame_box.addStretch()
        self.button_frame_box.addWidget(self.cncl_button)
        self.button_frame_box.addWidget(self.ok_button)
        self.button_frame_box.addStretch()

    def feature_gui_objects(self):
        """Function runs more break-down functions for adding features to the widgets"""
        self.setup_window_geometry()
        self.setup_left_panel_animation()
        self.setup_users_table()
        self.password_editline.setEchoMode(qtw.QLineEdit.Password)

    def setup_window_geometry(self):
        window_x_coord = int(self.app_settings.screen_width / 2 - self.app_settings.loginwindow_width / 2)
        window_y_coord = int(self.app_settings.screen_height / 2 - self.app_settings.loginwindow_height / 2)
        self.setGeometry(window_x_coord, window_y_coord,
                         self.app_settings.loginwindow_width, self.app_settings.loginwindow_height)

    def setup_left_panel_animation(self):
        anim_gif = qtg.QMovie('resources/icons/animated_truck.gif')
        anim_gif.setScaledSize(qtc.QSize(int(self.size().width() / 2), self.size().height()))
        self.animation_label.setMovie(anim_gif)
        self.animation_label.setAlignment(qtc.Qt.AlignCenter)
        anim_gif.start()

    def setup_users_table(self):
        """Fill the table with available users to be used to login

        Because user's list is not large in small companies, this SQL query is not executed is separate thread
        """
        self.users_table.setColumnCount(1)
        self.users_table.setSelectionMode(qtw.QAbstractItemView.SingleSelection)
        self.users_table.setHorizontalHeaderLabels(["Users"])
        my_curr = self.app_connection.cursor()
        my_curr.execute("SELECT id, fname ||'   '|| sname AS pib FROM users ORDER BY 1")
        while True:
            one_row = my_curr.fetchone()
            if one_row is None:
                break
            self.users_id_list.append(one_row[0])
            row_position = self.users_table.rowCount()
            self.users_table.insertRow(row_position)
            self.users_table.setItem(row_position, 0, qtw.QTableWidgetItem(one_row[1]))
        self.users_table.setCurrentCell(0, 0)
        header = self.users_table.horizontalHeader()
        header.setSectionResizeMode(0, qtw.QHeaderView.Stretch)
        # self.usersTable.setColumnWidth(0, 200)

    def setup_gui_object_events(self):
        self.cncl_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.login_application)

    def close_application(self, e):
        self.reject()

    def keyPressEvent(self, event):
        """slot for processing Enter key. Linked to the same function as OK button"""
        if event.key() == qtc.Qt.Key_Return:
            self.login_application()

    def login_application(self):
        """Function attemps to authenticate user based on id of chosen user and typed password
        
        Authentication check is performed by database internal function
        Database function returns success/fail and privilege of the user flags
        In case if fail attempt, application allows countless re-tries.
        """
        selected_user_id = self.users_id_list[self.users_table.currentRow()]
        selected_user_password = self.hash_entered_password()
        try:
            my_curr = self.app_connection.cursor()
            return_value = my_curr.var(cx_Oracle.NUMBER)
            out_value_is_privilege = my_curr.var(cx_Oracle.NUMBER)
            out_value_is_privilege.setvalue(0, -1)

            my_curr.callfunc('SUPPORT_PACKAGE.parol_func', return_value,
                             [
                                 selected_user_id,
                                 selected_user_password,
                                 out_value_is_privilege
                            ])

            # VERY IMPORTANT!!!
            # oracle function return 0 in case of  fail
            if return_value.getvalue() == 1:
                if out_value_is_privilege.getvalue() == 1:
                    self.app_settings.is_privilege_user = True
                else:
                    self.app_settings.is_privilege_user = False
                self.accept()
                return 0
            else:
                retry = qtw.QMessageBox.question(self, 'Wrong Password', 'You have entered wrong password. Retry?',
                                         qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)
                if retry == qtw.QMessageBox.Yes:
                    self.password_editline.setText('')
                else:
                    self.reject()
        except cx_Oracle.Error as exception:
            error, = exception.args
            print(error.code)
            print(error.message)
            # log
            return -1
        finally:
            my_curr.close()

    def hash_entered_password(self):
        """This is simple function that converts string into sha256 digest"""
        return hashlib.sha256(self.password_editline.text().encode()).hexdigest()
