"""allworkers module contains all worker classes, which are all subclassing Thread

These are: LoadConfirmationWorker, BrokerWorker, CarrierWroker, ConsgineeWorker,
            CurrencyWorker, LoadTypeWroker, ShipperWorker, UsersWorker,
            LoadCofirmationConnectToDatabase, GenerateReportWorker

This approach allows to execute heavy SQL queries to the database without having GUI frontend become frozen
Most of these are responsible for loading large tables for every MDIsubwindows
"""

import os
import pyreportjasper
import time
import socket
import decimal
import cx_Oracle
from PyQt5.QtCore import QThread, pyqtSignal
from all_persistence_class import (LoadConfirmationInstance, BrokerInstance, CarrierInstance,
                                   ConsigneeInstance, CurrencyInstance, LoadTypeInstance,
                                   ShipperInstance, UserInstance)

class LoadConfirmationsWorker(QThread):
    """This Thread queries all load confirmation records"""

    update_value_signal = pyqtSignal(int)
    update_nextrow_signal = pyqtSignal(LoadConfirmationInstance)
    update_windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_connection):
        super().__init__()
        self.app_connection = app_connection
        self.row_num = 0

    def NumberToDecimal(self, cursor, name, defaultType, size, precision, scale):
        if defaultType == cx_Oracle.DB_TYPE_NUMBER and name == 'LCAGREEDRATE':
            return cursor.var(decimal.Decimal, arraysize=cursor.arraysize)

    def run(self):
        try:
            self.update_windowmessage_signal.emit(100001, 'Fetching data...')
            my_curr = self.app_connection.cursor()
            my_curr.outputtypehandler = self.NumberToDecimal
            my_curr.execute(
                "SELECT l.lcid, l.lccurrencyid, l.lcloadtypeid, "
                "l.lccarrierid, l.lccustombrokerid, l.lcnote, "
                " l.lcno, l.lccreated, l.lcagreedrate, "
                "c.currencyshortname, l.lcquantity, t.loadtypename, "
                "r.carriername, b.custombrokername, u.fname || '  ' ||u.sname "
                "FROM loadconfirmation l,users u, currency c, "
                "loadtype t, carrier r, custombroker b "
                "WHERE l.lccurrencyid = c.currencyid "
                "AND l.lcloadtypeid = t.loadtypeid "
                "AND l.lccarrierid = r.carrierid "
                "AND l.lccustombrokerid = b.custombrokerid "
                "AND l.lccreatedby = u.id " 
                "ORDER BY 1 DESC"
                )
            while True:
                one_row = my_curr.fetchone()
                if one_row is None:
                    break
                self.update_value_signal.emit(self.row_num)
                self.update_nextrow_signal.emit(LoadConfirmationInstance(
                    lcid=one_row[0],
                    lccurrencyid=one_row[1],
                    lcloadtypeid=one_row[2],
                    lccarrierid=one_row[3],
                    lccustombrokerid=one_row[4],
                    lcnote=one_row[5],
                    lcno=one_row[6],
                    lcdatecreated=one_row[7],
                    lcagreedrate=one_row[8],
                    lccurrencyshortname=one_row[9],
                    lcquantity=one_row[10],
                    lcloadtypename=one_row[11],
                    lccarriername=one_row[12],
                    lccustombrokername=one_row[13],
                    lccreatedby=one_row[14]

                ))
                self.row_num += 1
            self.update_value_signal.emit(0)
            self.update_windowmessage_signal.emit(100000, 'Data was fetched successfully')
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                         'Check your log.')
            # log with error.code AND error.message
        finally:
            my_curr.close()


class BrokerWorker(QThread):
    """This Thread queries all brokers"""

    update_progressbar_signal = pyqtSignal(int)
    update_nextrow_signal = pyqtSignal(BrokerInstance)
    update_windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_connection):
        super().__init__()
        self.app_connection = app_connection
        self.row_num = 0

    def run(self):
        try:
            self.update_windowmessage_signal.emit(100001, 'Fetching data...')
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT custombrokerid, custombrokername, "
                "custombrokerphone, custombrokerfax, "
                "custombrokertollfree, custombrokercontact "
                "FROM custombroker "
                "ORDER BY 1 DESC"
            )
            while True:
                one_row = my_curr.fetchone()
                if one_row is None:
                    break
                self.update_progressbar_signal.emit(self.row_num)
                self.update_nextrow_signal.emit(BrokerInstance(
                    custombrokerid=one_row[0],
                    custombrokername=one_row[1],
                    custombrokerphone=one_row[2],
                    custombrokerfax=one_row[3],
                    custombrokertollfree=one_row[4],
                    custombrokercontact=one_row[5]
                ))
                self.row_num += 1
            self.update_progressbar_signal.emit(0)
            self.update_windowmessage_signal.emit(100000, 'Data was fetched successfully')
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(error.code, error.message)
            # log this error
        finally:
            my_curr.close()


class CarrierWorker(QThread):
    """This Thread queries all carriers"""

    update_progressbar_signal = pyqtSignal(int)
    update_nextrow_signal = pyqtSignal(CarrierInstance)
    update_windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_connection):
        super().__init__()
        self.app_connection = app_connection
        self.row_num = 0

    def run(self):
        try:
            self.update_windowmessage_signal.emit(100001, 'Fetching data...')
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT carrierid, carriername, carrieraddress, "
                "carriercity, carrierstate, carriercountry, "
                "carrierpostalcode, carrierphone, carrierfax, "
                "carriertollfree, carriercontact "
                "FROM carrier "
                "ORDER BY 1 DESC"
            )
            while True:
                one_row = my_curr.fetchone()
                if one_row is None:
                    break
                self.update_progressbar_signal.emit(self.row_num)
                self.update_nextrow_signal.emit(CarrierInstance(
                    carrierid=one_row[0],
                    carriername=one_row[1],
                    carrieraddress=one_row[2],
                    carriercity=one_row[3],
                    carrierstate=one_row[4],
                    carriercountry=one_row[5],
                    carrierpostalcode=one_row[6],
                    carrierphone=one_row[7],
                    carrierfax=one_row[8],
                    carriertollfree=one_row[9],
                    carriercontact=one_row[10]
                ))
                self.row_num += 1
            self.update_progressbar_signal.emit(0)
            self.update_windowmessage_signal.emit(100000, 'Data was fetched successfully')
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           'Check your log.')
            # log with error.code and error.message
        finally:
            my_curr.close()


class ConsigneeWorker(QThread):
    """This Thread queries all consignees"""

    update_progressbar_signal = pyqtSignal(int)
    update_nextrow_signal = pyqtSignal(ConsigneeInstance)
    update_windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_connection):
        super().__init__()
        self.app_connection = app_connection
        self.row_num = 0

    def run(self):
        try:
            self.update_windowmessage_signal.emit(100001, 'Fetching data...')
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT consigneeid, consigneename, consigneeaddress, "
                "consigneecity, consigneestate, consigneecountry, "
                "consigneepostalcode, consigneephone, consigneefax, "
                "consigneetollfree, consigneecontact "
                "FROM consignee "
                "ORDER BY 1 DESC"
            )
            while True:
                one_row = my_curr.fetchone()
                if one_row is None:
                    break
                self.update_progressbar_signal.emit(self.row_num)
                self.update_nextrow_signal.emit(ConsigneeInstance(
                    consigneeid=one_row[0],
                    consigneename=one_row[1],
                    consigneeaddress=one_row[2],
                    consigneecity=one_row[3],
                    consigneestate=one_row[4],
                    consigneecountry=one_row[5],
                    consigneepostalcode=one_row[6],
                    consigneephone=one_row[7],
                    consigneefax=one_row[8],
                    consigneetollfree=one_row[9],
                    consigneecontact=one_row[10]
                ))
                self.row_num += 1
            self.update_progressbar_signal.emit(0)
            self.update_windowmessage_signal.emit(100000, 'Data was fetched successfully')
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           'Check your log.')
            # log with error.code and error.message
        finally:
            my_curr.close()


class CurrencyWorker(QThread):
    """This Thread queries all currencies"""

    update_progressbar_signal = pyqtSignal(int)
    update_nextrow_signal = pyqtSignal(CurrencyInstance)
    update_windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_connection):
        super().__init__()
        self.app_connection = app_connection
        self.row_num = 0

    def run(self):
        try:
            self.update_windowmessage_signal.emit(100001, 'Fetching data...')
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT currencyid, currencyshortname, currencyname, currencyimagepath "
                "FROM currency "
                "ORDER BY 1 DESC"
            )
            while True:
                one_row = my_curr.fetchone()
                if one_row is None:
                    break
                self.update_progressbar_signal.emit(self.row_num)
                self.update_nextrow_signal.emit(CurrencyInstance(
                    currencyid=one_row[0],
                    currencyshortname=one_row[1],
                    currencyname=one_row[2],
                    currencyimagepath=one_row[3]
                ))
                self.row_num += 1
            self.update_progressbar_signal.emit(0)
            self.update_windowmessage_signal.emit(100000, 'Data was fetched successfully')
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(error.code, error.message)
            # log this error
        finally:
            my_curr.close()


class LoadConfirmationConnectToDatabase(QThread):
    """This Thread establishes the connection to the database"""

    connection_signal = pyqtSignal(cx_Oracle.Connection)
    windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_settings):
        super().__init__()
        self.app_settings = app_settings
        self.is_connection_valid = False
        self.app_settings.connection_worker = self
        self.iter_counter = 0

    def run(self):
        try:
            if self.app_settings.service_name is None:
                dsn = cx_Oracle.makedsn(host=self.app_settings.server,
                                        port=self.app_settings.port,
                                        sid=self.app_settings.sid)
            else:
                dsn = cx_Oracle.makedsn(host=self.app_settings.server,
                                        port=self.app_settings.port,
                                        service_name=self.app_settings.service_name)
            my_conn = cx_Oracle.connect(self.app_settings.user, self.app_settings.password, dsn)
            my_conn.autocommit = True
            self.connection_signal.emit(my_conn)
            self.windowmessage_signal.emit(100010, 'Connection established')
            while True:
                self.iter_counter += 1
                print(f'Entering cycle: {self.is_connection_valid} - {self.iter_counter}')
                time.sleep(5)
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_socket.settimeout(5)
                try:
                    test_socket.connect((self.app_settings.server, self.app_settings.port))
                    test_socket.shutdown(socket.SHUT_RDWR)
                    if not self.is_connection_valid:
                        self.app_settings.connection_worker = self
                        self.windowmessage_signal.emit(100010, 'Connection established')
                        self.is_connection_valid = True
                except:
                    if self.is_connection_valid:
                        self.windowmessage_signal.emit(-100001, 'Connection lost. Reconnecting...')
                        self.is_connection_valid = False
                    break
        except Exception as e:
            self.windowmessage_signal.emit(-100002, f'Something wrong with connection {str(e)}')


class LoadTypeWorker(QThread):
    """This Thread queries all load types"""

    update_progressbar_signal = pyqtSignal(int)
    update_nextrow_signal = pyqtSignal(LoadTypeInstance)
    update_windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_connection):
        super().__init__()
        self.app_connection = app_connection
        self.row_num = 0

    def run(self):
        try:
            self.update_windowmessage_signal.emit(100001, 'Fetching data...')
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT loadtypeid, loadtypename "
                "FROM loadtype "
                "ORDER BY 1 DESC"
            )
            while True:
                one_row = my_curr.fetchone()
                if one_row is None:
                    break
                self.update_progressbar_signal.emit(self.row_num)
                self.update_nextrow_signal.emit(LoadTypeInstance(
                    loadtypeid=one_row[0],
                    loadtypename=one_row[1]
                ))
                self.row_num += 1
            self.update_progressbar_signal.emit(0)
            self.update_windowmessage_signal.emit(100000, 'Data was fetched successfully')
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(error.code, error.message)
            # log this error
        finally:
            my_curr.close()


class ShipperWorker(QThread):
    """This Thread queries all shippers"""

    update_progressbar_signal = pyqtSignal(int)
    update_nextrow_signal = pyqtSignal(ShipperInstance)
    update_windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_connection):
        super().__init__()
        self.app_connection = app_connection
        self.row_num = 0

    def run(self):
        try:
            self.update_windowmessage_signal.emit(100001, 'Fetching data...')
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT shipperid, shippername, shipperaddress, "
                "shippercity, shipperstate, shippercountry, "
                "shipperpostalcode, shipperphone, shipperfax, "
                "shippertollfree, shippercontact "
                "FROM shipper "
                "ORDER BY 1 DESC"
            )
            while True:
                one_row = my_curr.fetchone()
                if one_row is None:
                    break
                self.update_progressbar_signal.emit(self.row_num)
                self.update_nextrow_signal.emit(ShipperInstance(
                    shipperid=one_row[0],
                    shippername=one_row[1],
                    shipperaddress=one_row[2],
                    shippercity=one_row[3],
                    shipperstate=one_row[4],
                    shippercountry=one_row[5],
                    shipperpostalcode=one_row[6],
                    shipperphone=one_row[7],
                    shipperfax=one_row[8],
                    shippertollfree=one_row[9],
                    shippercontact=one_row[10]
                ))
                self.row_num += 1
            self.update_progressbar_signal.emit(0)
            self.update_windowmessage_signal.emit(100000, 'Data was fetched successfully')
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           'Check your log.')
            # log with error.code and error.message
        finally:
            my_curr.close()


class UsersWorker(QThread):
    """This Thread queries all users"""

    update_progressbar_signal = pyqtSignal(int)
    update_nextrow_signal = pyqtSignal(UserInstance)
    update_windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_connection):
        super().__init__()
        self.app_connection = app_connection
        self.row_num = 0

    def run(self):
        try:
            self.update_windowmessage_signal.emit(100001, 'Fetching data...')
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "select id, fname, sname, password "
                "from users "
                "order by 1 DESC"
            )
            while True:
                one_row = my_curr.fetchone()
                if one_row is None:
                    break
                self.update_progressbar_signal.emit(self.row_num)
                self.update_nextrow_signal.emit(UserInstance(
                    userid=one_row[0],
                    userfname=one_row[1],
                    usersname=one_row[2],
                    password=one_row[3]
                ))
                self.row_num += 1
            self.update_progressbar_signal.emit(0)
            self.update_windowmessage_signal.emit(100000, 'Data was fetched successfully')
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(error.code, error.message)
            # log this error
        finally:
            my_curr.close()


class GenerateReportWorker(QThread):
    """This Thread generates pdf report"""

    report_generation_done = pyqtSignal(str)
    update_windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_settings):
        super().__init__()
        self.app_settings = app_settings
        self.setup_database_connection()

    def setup_database_connection(self):
        if self.app_settings:
            self.database_connection = {
                'driver': 'oracle',
                'jdbc_driver': 'oracle.jdbc.driver.OracleDriver',
                'host': self.app_settings.server,
                'port': self.app_settings.port,
                'db_sid': self.app_settings.sid,
                'username': self.app_settings.user,
                'password': self.app_settings.password
            }

    def run(self):
        try:
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
            pyreportjasper_instance = pyreportjasper.PyReportJasper()
            pyreportjasper_instance.config(
                report_template_filepath,
                generated_report_filepath,
                db_connection=self.database_connection,
                parameters={},
                output_formats=["pdf"],
                locale='en_US'
            )
            pyreportjasper_instance.process_report()
            print(f'in run {generated_report_filepath}')
            # self.report_generation_done.emit(generated_report_filepath)
            # self.update_windowmessage_signal.emit(
            #     100003,
            #     'Load Confirmation PDF report was generated successfully'
            # )
            self.quit()
        except Exception as ex:
            pass
            # self.update_windowmessage_signal.emit(
            #     -100000,
            #     f'Error generating the report\n {str(ex)}'
            #     )
