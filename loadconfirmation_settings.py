"""Class with dimension's settings and style sheet information"""
import os

class Settings:

    ### Constrants ###

    # Flags of type of operations
    DELETE = 1
    INSERT = 2
    MODIFY = 3
    VIEW = 4

    style_sheet = """
        QFrame{
        background-color: grey;
        border-style: outset;
        border-width: 2px;
        border-color: black;
        }
        
        QMenu::item:selected{
            background: white;
            color: black;
            border-color: #83A563;
            border-style: outset;
            border-width: 2px;
        }
        
        QMenu::item:disabled{
            background: white;
            color: black;
            border-color: red;
            border-style: outset;
            border-width: 2px;
        }

        QHeaderView{
            background-color: grey;
            border: none;
            outline: none;
        }

       QHeaderView:section {
            background-color: #646464;
            color: white;
            border: none;
            outline: none;
        }

        QFrame#spacerFrame{
            background-color: grey;
            border-style: outset;
            border: none;
            outline: none;
        }

        QFrame#dataFrame{
            background-color: grey;
            border-style: outset;
            border-width: 2px;
            border-color: #83A563;
        }
        
        QLabel{
            background-color: grey;
            color: black;
            border: none;
            outline: none;
        } 

        QLabel#title{
            font-size: 16px;
            background-color: grey;
            color: black;
            border: none;
            outline: none;
        } 
        
        QPushButton{
            background-color: grey;
            font-size: 16px;
            border-style: outset;
            border-width: 2px;
            border-color: black;
            color: black;
        }

        QPushButton:disabled{
            background-color: grey;
            font-size: 16px;
            border-style: outset;
            border-width: 2px;
            border-color: white;
            color: black;
        }
        
        QPushButton:pressed{
            background-color: #646464;
            font-size: 16px;
            border-style: outset;
            border-width: 2px;
            border-color: white;
            color: black;
        }
        
        QComboBox{
            background-color: grey;
            color: black;
            outline: none;
        }
        
        QTextEdit{
            background-color: white;
            color: black;
            outline: none;
        }
                
        QLineEdit{
            background-color: grey;
            color: black;
            outline: none;
        }
        
        QLineEdit:focus{
            background-color: #83A563;
            color: black;
            border: none;
            outline: none;
        }

        QLineEdit:disabled{
            background-color: grey;
            color: black;
            border-width: 1px;
            border-style: outset;
            border-color: white;
        }

        QProgressBar{
            background-color: #C0C6CA;
            color: #FFFFFF;
            border: 1px solid grey;
            padding: 3px;
            height: 15px;
            text-align: center;
        }

        QProgressBar::chunk{
            background: #538DB8;
            width: 5px;
            margin: 0.5px;
        }

        QStatusBar[Error=true]{
            color: red;
        }

        QStatusBar[Error=false]{
            color: green;
        }
        """

    def __init__(self, screen):

        self.application_folderpath = os.path.abspath(os.path.dirname(__file__))
        self.images_relativepath = 'resources/report_templates/images'

        #connection settings for oracle server that uses SID
        # self.user = 'loadconfirmation'
        # self.password = 'loadconfirmation$6ddh'
        # self.sid = 'ORCL'
        # self.server = '25.60.170.16'
        # self.service_name = None
        # self.port = 1521

        #connection settings for server that uses SERVICE NAME
        self.service_name = 'pdborcl2'
        self.user = 'loadconfirmation'
        self.password = 'loadconfirmation'
        self.port = 1521
        # self.server = '192.168.100.189'
        self.server = '25.12.254.109'

        self.connection_worker = None
        # default user has basic privilege
        self.is_privilege_user = False

        #filename of the main report template
        self.report_template_name = 'shipper1consignee1_2020.jrxml'


        self.screen_width = screen.size().width()
        self.screen_height = screen.size().height()

        #windows dimension settings
        self.mainwindow_width = screen.size().width()
        self.mainwindow_height = int((screen.size().height() / 4) * 3)

        self.loginwindow_width = int(screen.size().width() / 2)
        self.loginwindow_height = int(screen.size().height() / 3)

        self.subwindow_width = screen.size().width()
        self.subwindow_height = int(screen.size().height() / 2)

        self.smallsubwindow_width = int(screen.size().width() / 2)
        self.smallsubwindow_height = int(screen.size().height() / 2)

        self.loadconfirmationwindow_width = int((screen.size().width() / 3) * 2)
        self.loadconfirmationwindow_height = int(screen.size().height() / 3)

        self.newwindow_width = int(screen.size().width() / 3)
        self.newwindow_height = int(screen.size().height() / 2)

        self.smallnewwindow_width = int(screen.size().width() / 3)
        self.smallnewwindow_height = int(screen.size().height() / 3)
