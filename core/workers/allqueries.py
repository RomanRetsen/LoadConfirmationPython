"""allqueries module is similar to allworkers module but without multi-threading

allqueries module contains SQL queries that are quick running and not time consuming,
meaning not required to be executed in separate threads.
They are responsible for obtaining and creating object instance based on id,
or populating widgets (for example combo-box) with some data.
These are: LoadConfirmationWorker, BrokerWorker, CarrierWroker, ConsgineeWorker,
            CurrencyWorker, LoadTypeWroker, ShipperWorker, UsersWorker,
            LoadCofirmationConnectToDatabase, GenerateReportWorker

"""
import hashlib
import cx_Oracle
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGraphicsObject
from all_persistence_class import (LoadConfirmationInstance, LoadTypeInstance,
                                   CurrencyInstance, CarrierInstance,
                                   BrokerInstance, ShipperInstance,
                                   ConsigneeInstance, ShipperRefInstance,
                                   ConsigneeRefInstance, UserInstance)


class LoadConfirmationsQueries(QGraphicsObject):

    update_windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_connection):
        super().__init__()
        self.app_connection = app_connection

    def loads_count(self):
        """Function returns number of records in loadconfirmation table"""
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute('SELECT count(*) FROM loadconfirmation')
            carrier_fetch_result = my_curr.fetchone()
            return carrier_fetch_result[0]
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           ' Check your log.')
            # log with error.code AND error.message
        finally:
            my_curr.close()


    def get_loadconfirmation_byid(self, loadconfirmationid:str) -> LoadConfirmationInstance:
        """ Function creates load confirmation instance


        Function extract one record of specific load confirmation based on load confirmation id.
        Then it creates and returns instance of the class LoadConfirmation based on this information
        """
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT l.lcid, l.lccurrencyid, l.lcloadtypeid, "
                "l.lccarrierid, l.lccustombrokerid, l.lcnote, "
                "l.lcno, l.lccreated, l.lcagreedrate, "
                "c.currencyshortname, l.lcquantity, t.loadtypename, "
                "r.carriername, b.custombrokername, u.fname || '  ' ||u.sname "
                "FROM loadconfirmation l,users u, currency c, "
                "loadtype t, carrier r, custombroker b "
                "WHERE l.lccurrencyid = c.currencyid "
                "AND l.lcloadtypeid = t.loadtypeid "
                "AND l.lccarrierid = r.carrierid "
                "AND l.lccustombrokerid = b.custombrokerid "
                "AND l.lccreatedby = u.id "
                "AND l.lcid = "
                + loadconfirmationid
            )
            one_row = my_curr.fetchone()
            if one_row is None:
                self.update_windowmessage_signal.emit(-100000, 'No data available')
                return 1
            else:
                return LoadConfirmationInstance(
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
                )
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return 1
        finally:
            my_curr.close()

    def get_all_loadtypes(self) -> list:
        """Function returns all load types

         Function returns list of LoadTypeInstance for all load type
         """
        list_of_load_type_instances = []
        try:
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
                list_of_load_type_instances.append(LoadTypeInstance(
                    loadtypeid=one_row[0],
                    loadtypename=one_row[1]
                ))
            return list_of_load_type_instances
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(
                -100000,
                'Error has occurred during population of loadtype combobox. '
                'Check your log.'
            )
            # log this error
        finally:
            my_curr.close()


    def get_all_currencies(self) -> list:
        """Function returns all currencies

         Function returns list of CurrencyInstance for all currencies
         """
        list_of_currency_instances = []
        try:
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
                list_of_currency_instances.append(CurrencyInstance(
                    currencyid=one_row[0],
                    currencyshortname=one_row[1],
                    currencyname=one_row[2],
                    currencyimagepath=one_row[3]
                ))
            return list_of_currency_instances
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(
                -100000,
                'Error has occurred during population of currency combobox. '
                'Check your log.'
            )
            # log this error
        finally:
            my_curr.close()

    def get_all_carriers(self) -> list:
        """Function returns all carriers

         Function returns list of CarrierInstance for all carriers
         """
        all_carriers = []
        try:
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
                all_carriers.append(CarrierInstance(
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
            return all_carriers
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(
                -100000,
                'Error has occurred during population of currencies combobox. '
                'Check your log.'
            )
            # log this error
        finally:
            my_curr.close()

    def get_all_shippers(self) -> list:
        """Function returns all shippers

         Function returns list of ShipperInstance for all shippers
         """
        all_shippers = []
        try:
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
                all_shippers.append(ShipperInstance(
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
            return all_shippers
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(
                -100000,
                'Error has occurred during population of shippers combobox. '
                'Check your log.'
            )
            # log this error
        finally:
            my_curr.close()

    def get_all_consignees(self) -> list:
        """Function returns all consignees

         Function returns list of ConsigneeInstance for all consignees
         """
        all_consignees = []
        try:
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
                all_consignees.append(ConsigneeInstance(
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
            return all_consignees
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(
                -100000,
                'Error has occurred during population of consignees combobox. '
                'Check your log.'
            )
            # log this error
        finally:
            my_curr.close()

    def get_all_brokers(self) -> list:
        """Function returns all brokers

         Function returns list of BrokerInstance for all brokers
         """
        all_consignees = []
        try:
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
                all_consignees.append(BrokerInstance(
                    custombrokerid=one_row[0],
                    custombrokername=one_row[1],
                    custombrokerphone=one_row[2],
                    custombrokerfax=one_row[3],
                    custombrokertollfree=one_row[4],
                    custombrokercontact=one_row[5]
                ))
            return all_consignees
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(
                -100000,
                'Error has occurred during population of brokers combobox. '
                'Check your log.'
            )
            # log this error
        finally:
            my_curr.close()

    def delete_loadconfirmation(self, requested_loadconfirmation):
        """Function deletes load confirmation record


        """
        try:
            self.app_connection.autocommit = False
            my_curr = self.app_connection.cursor()
            out_return_parameter = my_curr.var(cx_Oracle.NUMBER)
            my_curr.callproc('SUPPORT_PACKAGE.delete_loadconfirmation',
                             [
                                 requested_loadconfirmation.lcid,
                                 requested_loadconfirmation.lcno,
                                 out_return_parameter
                             ])
            out_return_value = out_return_parameter.getvalue()
            if out_return_value == -2:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error inserting data. \n'
                    'Check if deleting load confirmation with same # already exists'
                )
                self.app_connection.rollback()
                return 1
            elif out_return_value == -1:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error deleting data. \n'
                    'No data for deletion available.'
                )
                self.app_connection.rollback()
                return 1
            elif out_return_value == 1:
                self.app_connection.commit()
                self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                return 0
        except cx_Oracle.Error as exception:
            self.app_connection.rollback()
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return -1
        finally:
            self.app_connection.autocommit = True
            my_curr.close()

    def insert_loadconfirmation(
            self,
            requested_loadconfirmation,
            chosen_shippers,
            chosen_consignees
    ):
        try:
            self.app_connection.autocommit = False
            my_curr = self.app_connection.cursor()
            out_return_parameter = my_curr.var(cx_Oracle.NUMBER)
            out_user_parameter = my_curr.var(cx_Oracle.STRING)
            # out_return_parameter.setvalue(0, 0)
            my_curr.callproc('SUPPORT_PACKAGE.insert_loadconfirmation_proc',
                             [
                                 requested_loadconfirmation.lcno,
                                 requested_loadconfirmation.lcagreedrate,
                                 requested_loadconfirmation.lccurrencyid,
                                 requested_loadconfirmation.lcquantity,
                                 requested_loadconfirmation.lcloadtypeid,
                                 requested_loadconfirmation.lccarrierid,
                                 requested_loadconfirmation.lccustombrokerid,
                                 requested_loadconfirmation.lcnote,
                                 out_return_parameter,
                                 out_user_parameter
                             ])
            out_return_value = out_return_parameter.getvalue()
            out_user_value = out_user_parameter.getvalue()
            if out_return_value == -2:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error inserting data. \n'
                    'Check if inserting load confirmation # already exists'
                )
                self.app_connection.rollback()
                return 1
            elif out_return_value == -1:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error inserting data. \n'
                    'There was conflict of ID during insertion. Try same operation again'
                )
                self.app_connection.rollback()
                return 1
            else:
                requested_loadconfirmation.lcid = out_return_value
                requested_loadconfirmation.lccreatedby = out_user_value
                for shipper_ref in chosen_shippers:
                    my_curr.callproc('SUPPORT_PACKAGE.insert_shipper_ref',
                                     [
                                         requested_loadconfirmation.lcid,
                                         shipper_ref.shipperid,
                                         shipper_ref.shipperdate,
                                         shipper_ref.shippertime
                                     ])
                for consignee_ref in chosen_consignees:
                    my_curr.callproc('SUPPORT_PACKAGE.insert_consignee_ref',
                                     [
                                         requested_loadconfirmation.lcid,
                                         consignee_ref.consigneeid,
                                         consignee_ref.consigneedate,
                                         consignee_ref.consigneetime
                                     ])
                self.app_connection.commit()
                self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                return 0
        except cx_Oracle.Error as exception:
            self.app_connection.rollback()
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return -1
        finally:
            self.app_connection.autocommit = True
            my_curr.close()

    def modify_loadconfirmation(
            self,
            requested_loadconfirmation,
            chosen_shippers,
            chosen_consignees
    ):
        try:
            self.app_connection.autocommit = False
            my_curr = self.app_connection.cursor()
            out_return_parameter = my_curr.var(cx_Oracle.NUMBER)
            # out_return_parameter.setvalue(0, 0)
            my_curr.callproc('SUPPORT_PACKAGE.update_loadconfirmation_proc',
                             [
                                 requested_loadconfirmation.lcid,
                                 requested_loadconfirmation.lcno,
                                 requested_loadconfirmation.lcagreedrate,
                                 requested_loadconfirmation.lccurrencyid,
                                 requested_loadconfirmation.lcquantity,
                                 requested_loadconfirmation.lcloadtypeid,
                                 requested_loadconfirmation.lccarrierid,
                                 requested_loadconfirmation.lccustombrokerid,
                                 requested_loadconfirmation.lcnote,
                                 out_return_parameter
                             ])
            out_return_value = out_return_parameter.getvalue()
            if out_return_value == -1:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error inserting data. \n'
                    'Check if inserting load confirmation # already exists\n'
                    'Or uniqueness of load confirmation number was not corrupted'
                )
                self.app_connection.rollback()
                return 1
            elif out_return_value == 1:
                for shipper_ref in chosen_shippers:
                    my_curr.callproc('SUPPORT_PACKAGE.insert_shipper_ref',
                                     [
                                         requested_loadconfirmation.lcid,
                                         shipper_ref.shipperid,
                                         shipper_ref.shipperdate,
                                         shipper_ref.shippertime
                                     ])
                for consignee_ref in chosen_consignees:
                    my_curr.callproc('SUPPORT_PACKAGE.insert_consignee_ref',
                                     [
                                         requested_loadconfirmation.lcid,
                                         consignee_ref.consigneeid,
                                         consignee_ref.consigneedate,
                                         consignee_ref.consigneetime
                                     ])
                self.app_connection.commit()
                self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                return 0
        except cx_Oracle.Error as exception:
            self.app_connection.rollback()
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return -1
        finally:
            self.app_connection.autocommit = True
            my_curr.close()

    def get_all_shippers_by_lcid(self, loadconfirmationid) -> list:
        return_list = []
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT sr.shipper_refid, sr.lcid, sr.shipperid, "
                "sr.shipperdate, sr.shippertime, "
                "s.shippername, s.shipperaddress, s.shippercity, "
                "s.shipperstate, s.shippercountry, s.shipperpostalcode, "
                "s.shipperphone, shipperfax, shippertollfree, "
                "s.shippercontact "
                "from shipper_ref sr, shipper s "
                "where sr.shipperid = s.shipperid "
                "and sr.lcid = "
                +  str(loadconfirmationid)
            )
            # Generating list of tuples - [(ShipperRefInstance, ShipperInstance), ......]
            while True:
                one_row = my_curr.fetchone()
                if one_row is None:
                    break
                return_list.append((
                    ShipperRefInstance(
                        shipperrefid=one_row[0],
                        loadconfirmationid=one_row[1],
                        shipperid=one_row[2],
                        shipperdate=one_row[3],
                        shippertime=one_row[4]
                    ),
                    ShipperInstance(
                        shipperid=one_row[2],
                        shippername=one_row[5],
                        shipperaddress=one_row[6],
                        shippercity=one_row[7],
                        shipperstate=one_row[8],
                        shippercountry=one_row[9],
                        shipperpostalcode=one_row[10],
                        shipperphone=one_row[11],
                        shipperfax=one_row[12],
                        shippertollfree=one_row[13],
                        shippercontact=one_row[14]
                    )
                ))
            if len(return_list) == 0:
                self.update_windowmessage_signal.emit(-100000, 'No shipper data available for this load confirmation')
                return 1
            else:
                return return_list
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(
                -100000,
                'Error has occurred during fetching.'
                'Check your log.'
            )
            # log this error
        finally:
            my_curr.close()

    def get_all_consignees_by_lcid(self, loadconfirmationid) -> list:
        return_list = []
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT sr.consignee_refid, sr.lcid, sr.consigneeid, "
                "sr.consigneedate, sr.consigneetime, "
                "s.consigneename, s.consigneeaddress, s.consigneecity, "
                "s.consigneestate, s.consigneecountry, s.consigneepostalcode, "
                "s.consigneephone, consigneefax, consigneetollfree, "
                "s.consigneecontact "
                "from consignee_ref sr, consignee s "
                "where sr.consigneeid = s.consigneeid "
                "and sr.lcid = "
                +  str(loadconfirmationid)
            )
            # Generating list of tuples - [(ConsigneeRefInstance, ConsigneeInstance), ......]
            while True:
                one_row = my_curr.fetchone()
                if one_row is None:
                    break
                return_list.append((
                    ConsigneeRefInstance(
                        consigneerefid=one_row[0],
                        loadconfirmationid=one_row[1],
                        consigneeid=one_row[2],
                        consigneedate=one_row[3],
                        consigneetime=one_row[4]
                    ),
                    ConsigneeInstance(
                        consigneeid=one_row[2],
                        consigneename=one_row[5],
                        consigneeaddress=one_row[6],
                        consigneecity=one_row[7],
                        consigneestate=one_row[8],
                        consigneecountry=one_row[9],
                        consigneepostalcode=one_row[10],
                        consigneephone=one_row[11],
                        consigneefax=one_row[12],
                        consigneetollfree=one_row[13],
                        consigneecontact=one_row[14]
                    )
                ))
            if len(return_list) == 0:
                self.update_windowmessage_signal.emit(-100000, 'No consignee data available for this load confirmation')
                return 1
            else:
                return return_list
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(
                -100000,
                'Error has occurred during fetching'
                'Check your log.'
            )
            # log this error
        finally:
            my_curr.close()

    def get_carrier_by_lcid(self, loadconfirmationid) -> CarrierInstance:
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT c.carrierid, c.carriername, c.carrieraddress, "
                "c.carriercity, c.carrierstate, c.carriercountry, "
                "c.carrierpostalcode, c.carrierphone, c.carrierfax, "
                "c.carriertollfree, c.carriercontact "
                "FROM carrier c, loadconfirmation l "
                "WHERE c.carrierid = l.lccarrierid "
                "AND l.lcid = " + str(loadconfirmationid))
            one_row = my_curr.fetchone()
            if one_row is None:
                self.update_windowmessage_signal.emit(-100000, 'No carrier data available for this load confirmation')
                return 1
            else:
                return CarrierInstance(
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
                )
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return 1
        finally:
            my_curr.close()

    def get_broker_by_lcid(self, loadconfirmationid) -> BrokerInstance:
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT b.custombrokerid, b.custombrokername, b.custombrokerphone, "
                "b.custombrokerfax, b.custombrokertollfree, b.custombrokercontact "
                "FROM custombroker b, loadconfirmation l "
                "WHERE b.custombrokerid = l.lccustombrokerid "
                "AND l.lcid = " + str(loadconfirmationid)
            )
            one_row = my_curr.fetchone()
            if one_row is None:
                self.update_windowmessage_signal.emit(-100000, 'No broker data available for this load confirmation')
                return 1
            else:
                return BrokerInstance(
                    custombrokerid=one_row[0],
                    custombrokername=one_row[1],
                    custombrokerphone=one_row[2],
                    custombrokerfax=one_row[3],
                    custombrokertollfree=one_row[4],
                    custombrokercontact=one_row[5]
                )
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return 1
        finally:
            my_curr.close()

    def get_currency_by_lcid(self, loadconfirmationid) -> CurrencyInstance:
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT c.currencyid, c.currencyshortname, "
                "c.currencyname, c.currencyimagepath "
                "FROM currency c, loadconfirmation l "
                "WHERE c.currencyid = l.lccurrencyid "
                "AND l.lcid = " + str(loadconfirmationid)
            )
            one_row = my_curr.fetchone()
            if one_row is None:
                self.update_windowmessage_signal.emit(-100000, 'No currency data available for this load confirmation')
                return 1
            else:
                return CurrencyInstance(
                    currencyid=one_row[0],
                    currencyshortname=one_row[1],
                    currencyname=one_row[2],
                    currencyimagepath=one_row[3]
                )
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return 1
        finally:
            my_curr.close()

    def get_loadtype_by_lcid(self, loadconfirmationid) -> LoadTypeInstance:
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT lt.loadtypeid, lt.loadtypename "
                "FROM loadtype lt, loadconfirmation lc "
                "WHERE lt.loadtypeid = lc.lcloadtypeid "
                "AND lc.lcid = " + str(loadconfirmationid)
            )
            one_row = my_curr.fetchone()
            if one_row is None:
                self.update_windowmessage_signal.emit(-100000, 'No loadtype data available for this load confirmation')
                return 1
            else:
                return LoadTypeInstance(
                    loadtypeid=one_row[0],
                    loadtypename=one_row[1]
                )
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return 1
        finally:
            my_curr.close()

    def users_count(self):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute('select count(*) from users')
            user_fetch_result = my_curr.fetchone()
            return user_fetch_result[0]
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(error.code, error.message)
        # log this error
        finally:
            my_curr.close()

    def get_user_byid(self, userid:str) -> UserInstance:
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute('SELECT id, fname, sname, password FROM users WHERE id = ' + userid)
            one_row = my_curr.fetchone()
            if one_row is None:
                self.update_windowmessage_signal.emit(-100000, 'No data available')
                return 1
            else:
                return UserInstance(
                    userid=one_row[0],
                    userfname=one_row[1],
                    usersname=one_row[2],
                    password=one_row[3]
                )
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return 1
        finally:
            my_curr.close()

    def delete_user(self, requestedUser):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute('SELECT count(*) FROM users WHERE id = ' + str(requestedUser.userid))
            one_row = my_curr.fetchone()
            if one_row[0]==1 and requestedUser.userfname!='Administrator':
                my_curr.execute(
                    'SELECT count(*) from loadconfirmation l '
                    'WHERE l.lccreatedby = '
                    + str(requestedUser.userid))
                one_row = my_curr.fetchone()
                if one_row[0] == 0:
                    my_curr.execute(
                        'DELETE FROM users WHERE  id = '
                        + str(requestedUser.userid)
                    )
                    my_curr.execute(
                        'SELECT count(*) FROM users WHERE id = '
                        + str(requestedUser.userid)
                    )
                    one_row = my_curr.fetchone()
                    if one_row[0] == 0:
                        self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                        return 0
                    else:
                        self.update_windowmessage_signal.emit(-100000, 'Error deleting data')
                        return 1
                else:
                    self.update_windowmessage_signal.emit(
                        -100000,
                        'Error deleting data. '
                        'There is(are) record(s) in main table using data from this record'
                    )
                    return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'No data for deletion available '
                    'or attempting to delete Administator'
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return 1
        finally:
            my_curr.close()

    def modify_user(self, requestedUser):
        try:
            my_curr = self.app_connection.cursor()
            return_value = my_curr.var(cx_Oracle.NUMBER)
            # function "change" from package "U" (inside database scheme)
            # is checking if user with updated name is already exist
            my_curr.callfunc('SUPPORT_PACKAGE.modify_user', return_value,
                             [
                                 requestedUser.userid,
                                 requestedUser.userfname,
                                 requestedUser.usersname
                             ])
            # VERY IMPORTANT!!!
            # oracle function return 1 in case of success , 0 - fail
            if return_value.getvalue() == 1:
                self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                return 0
            elif return_value.getvalue() == 0:
                self.update_windowmessage_signal.emit(-100000,
                                                      'Error updating data. '
                                                      'Check if updated name already exist'
                                                      )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return -1
        finally:
            my_curr.close()

    def insert_user(self, requestedUser):
        try:
            my_curr = self.app_connection.cursor()
            return_value = my_curr.var(cx_Oracle.NUMBER)
            # function "change" from package "U" (inside database scheme)
            # is checking if user with updated name is already exist
            password_hexdigesty = hashlib.sha256(requestedUser.password.encode()).hexdigest()
            execute_func = my_curr.callfunc('SUPPORT_PACKAGE.insert_user', return_value,
                                            [
                                                requestedUser.userfname,
                                                requestedUser.usersname,
                                                password_hexdigesty
                                            ])
            # VERY IMPORTANT!!!
            # oracle function return 0 in case of  fail to insert
            # or id of the newerly inserted user in case of success
            if return_value.getvalue() != 0:
                requestedUser.userid = return_value.getvalue()
                requestedUser.password = password_hexdigesty
                self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                return 0
            else:
                self.update_windowmessage_signal.emit(-100000,
                                                      'Error inserting data. '
                                                      'Check if insert user already exist'
                                                      )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return -1
        finally:
            my_curr.close()

    def modify_login_user_password(self, old_password, new_password):
        try:
            my_curr = self.app_connection.cursor()
            return_value_param = my_curr.var(cx_Oracle.NUMBER)
            my_curr.callfunc('SUPPORT_PACKAGE.modify_loginuser_password',
                             return_value_param,
                             [
                                 hashlib.sha256(old_password.encode()).hexdigest(),
                                 hashlib.sha256(new_password.encode()).hexdigest()
                             ])
            return_value = return_value_param.getvalue()
            if return_value == -2:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error changing password \n'
                    'Old password does not match.'
                )
                return 1
            elif return_value == -1:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error changing password. \n'
                    'User info was corrupted.'
                )
                return 1
            elif return_value == 1:
                self.update_windowmessage_signal.emit(
                    100002,
                    'Operation completed successfully\n'
                    'New password was set.'
                )
                return 0
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return -1
        finally:
            my_curr.close()

    def modify_user_password_byid(self, requested_user , new_password):
        try:
            my_curr = self.app_connection.cursor()
            return_value_param = my_curr.var(cx_Oracle.NUMBER)
            my_curr.callfunc('SUPPORT_PACKAGE.modify_user_password_byid',
                             return_value_param,
                             [
                                 requested_user.userid,
                                 hashlib.sha256(new_password.encode()).hexdigest()
                             ])
            return_value = return_value_param.getvalue()
            if return_value == -1:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error changing password. \n'
                    'User info was corrupted.'
                )
                return 1
            elif return_value == 1:
                self.update_windowmessage_signal.emit(
                    100002,
                    'Operation completed successfully\n'
                    'New password was set.'
                )
                return 0
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return -1
        finally:
            my_curr.close()


class UsersQueries(QGraphicsObject):

    update_windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_connection):
        super().__init__()
        self.app_connection = app_connection

    def users_count(self):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute('select count(*) from users')
            user_fetch_result = my_curr.fetchone()
            return user_fetch_result[0]
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(error.code, error.message)
        # log this error
        finally:
            my_curr.close()

    def get_user_byid(self, userid:str) -> UserInstance:
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute('SELECT id, fname, sname, password FROM users WHERE id = ' + userid)
            one_row = my_curr.fetchone()
            if one_row is None:
                self.update_windowmessage_signal.emit(-100000, 'No data available')
                return 1
            else:
                return UserInstance(
                    userid=one_row[0],
                    userfname=one_row[1],
                    usersname=one_row[2],
                    password=one_row[3]
                )
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return 1
        finally:
            my_curr.close()

    def delete_user(self, requestedUser):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute('SELECT count(*) FROM users WHERE id = ' + str(requestedUser.userid))
            one_row = my_curr.fetchone()
            if one_row[0]==1 and requestedUser.userfname!='Administrator':
                my_curr.execute(
                    'SELECT count(*) from loadconfirmation l '
                    'WHERE l.lccreatedby = '
                    + str(requestedUser.userid))
                one_row = my_curr.fetchone()
                if one_row[0] == 0:
                    my_curr.execute(
                        'DELETE FROM users WHERE  id = '
                        + str(requestedUser.userid)
                    )
                    my_curr.execute(
                        'SELECT count(*) FROM users WHERE id = '
                        + str(requestedUser.userid)
                    )
                    one_row = my_curr.fetchone()
                    if one_row[0] == 0:
                        self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                        return 0
                    else:
                        self.update_windowmessage_signal.emit(-100000, 'Error deleting data')
                        return 1
                else:
                    self.update_windowmessage_signal.emit(
                        -100000,
                        'Error deleting data. '
                        'There is(are) record(s) in main table using data from this record'
                    )
                    return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'No data for deletion available '
                    'or attempting to delete Administator'
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return 1
        finally:
            my_curr.close()

    def modify_user(self, requestedUser):
        try:
            my_curr = self.app_connection.cursor()
            return_value = my_curr.var(cx_Oracle.NUMBER)
            # function "change" from package "U" (inside database scheme)
            # is checking if user with updated name is already exist
            my_curr.callfunc('SUPPORT_PACKAGE.modify_user', return_value,
                             [
                                 requestedUser.userid,
                                 requestedUser.userfname,
                                 requestedUser.usersname
                             ])
            # VERY IMPORTANT!!!
            # oracle function return 1 in case of success , 0 - fail
            if return_value.getvalue() == 1:
                self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                return 0
            elif return_value.getvalue() == 0:
                self.update_windowmessage_signal.emit(-100000,
                                                      'Error updating data. '
                                                      'Check if updated name already exist'
                                                      )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return -1
        finally:
            my_curr.close()

    def insert_user(self, requestedUser):
        try:
            my_curr = self.app_connection.cursor()
            return_value = my_curr.var(cx_Oracle.NUMBER)
            # function "change" from package "U" (inside database scheme)
            # is checking if user with updated name is already exist
            password_hexdigesty = hashlib.sha256(requestedUser.password.encode()).hexdigest()
            execute_func = my_curr.callfunc('SUPPORT_PACKAGE.insert_user', return_value,
                                            [
                                                requestedUser.userfname,
                                                requestedUser.usersname,
                                                password_hexdigesty
                                            ])
            # VERY IMPORTANT!!!
            # oracle function return 0 in case of  fail to insert
            # or id of the newerly inserted user in case of success
            if return_value.getvalue() != 0:
                requestedUser.userid = return_value.getvalue()
                requestedUser.password = password_hexdigesty
                self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                return 0
            else:
                self.update_windowmessage_signal.emit(-100000,
                                                      'Error inserting data. '
                                                      'Check if insert user already exist'
                                                      )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return -1
        finally:
            my_curr.close()

    def modify_login_user_password(self, old_password, new_password):
        try:
            my_curr = self.app_connection.cursor()
            return_value_param = my_curr.var(cx_Oracle.NUMBER)
            my_curr.callfunc('SUPPORT_PACKAGE.modify_loginuser_password',
                             return_value_param,
                             [
                                 hashlib.sha256(old_password.encode()).hexdigest(),
                                 hashlib.sha256(new_password.encode()).hexdigest()
                             ])
            return_value = return_value_param.getvalue()
            if return_value == -2:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error changing password \n'
                    'Old password does not match.'
                )
                return 1
            elif return_value == -1:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error changing password. \n'
                    'User info was corrupted.'
                )
                return 1
            elif return_value == 1:
                self.update_windowmessage_signal.emit(
                    100002,
                    'Operation completed successfully\n'
                    'New password was set.'
                )
                return 0
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return -1
        finally:
            my_curr.close()

    def modify_user_password_byid(self, requested_user , new_password):
        try:
            my_curr = self.app_connection.cursor()
            return_value_param = my_curr.var(cx_Oracle.NUMBER)
            my_curr.callfunc('SUPPORT_PACKAGE.modify_user_password_byid',
                             return_value_param,
                             [
                                 requested_user.userid,
                                 hashlib.sha256(new_password.encode()).hexdigest()
                             ])
            return_value = return_value_param.getvalue()
            if return_value == -1:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error changing password. \n'
                    'User info was corrupted.'
                )
                return 1
            elif return_value == 1:
                self.update_windowmessage_signal.emit(
                    100002,
                    'Operation completed successfully\n'
                    'New password was set.'
                )
                return 0
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return -1
        finally:
            my_curr.close()


class ShipperQueries(QGraphicsObject):

    update_windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_connection):
        super().__init__()
        self.app_connection = app_connection

    def shippers_count(self):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute('SELECT count(*) FROM shipper')
            shipper_fetch_result = my_curr.fetchone()
            return shipper_fetch_result[0]
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           ' Check your log.')
            # log with error.code and error.message
        finally:
            my_curr.close()

    def get_shipper_by_id(self, shipperid:str) -> ShipperInstance:
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT shipperid, shippername, shipperaddress, "
                "shippercity, shipperstate, shippercountry, "
                "shipperpostalcode, shipperphone, shipperfax, "
                "shippertollfree, shippercontact "
                "FROM shipper "
                "WHERE shipperid = " + shipperid)
            one_row = my_curr.fetchone()
            if one_row is None:
                self.update_windowmessage_signal.emit(-100000, 'No data available')
                return 1
            else:
                return ShipperInstance(
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
                )
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return 1
        finally:
            my_curr.close()


    def delete_shipper(self, requested_shipper):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                'SELECT count(*) FROM shipper '
                'WHERE shipperid = '
                + str(requested_shipper.shipperid)
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 1:
                my_curr.execute(
                    'SELECT count(*) from shipper_ref c '
                    'WHERE c.shipperid = '
                    + str(requested_shipper.shipperid))
                one_row = my_curr.fetchone()
                if one_row[0] == 0:
                    my_curr.execute(
                        'DELETE FROM shipper '
                        'WHERE  shipperid = '
                        + str(requested_shipper.shipperid)
                    )
                    my_curr.execute(
                        'SELECT count(*) FROM shipper '
                        'WHERE shipperid = '
                        + str(requested_shipper.shipperid)
                    )
                    one_row = my_curr.fetchone()
                    if one_row[0] == 0:
                        self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                        return 0
                    else:
                        self.update_windowmessage_signal.emit(-100000, 'Error deleting data')
                        return 1
                else:
                    self.update_windowmessage_signal.emit(
                        -100000,
                        'Error deleting data. '
                        'There is(are) record(s) in main table using data from this record'
                    )
                    return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'No data for deletion available. '
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. '
                                                           'Check your log.')
            # log
            return 1
        finally:
            my_curr.close()

    def modify_shipper(self, requested_shipper):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT count(*) FROM shipper "
                "WHERE shipperid = "
                + str(requested_shipper.shipperid)
                + " OR shippername = '"
                + requested_shipper.shippername
                + "'"
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 1:
                my_curr.execute(
                    "UPDATE shipper "
                    "SET shippername = :1, "
                    "shipperaddress = :2, "
                    "shippercity = :3, "
                    "shipperstate = :4, "
                    "shippercountry = :5, "
                    "shipperpostalcode = :6, "
                    "shipperphone = :7, "
                    "shipperfax = :8, "
                    "shippertollfree = :9, "
                    "shippercontact = :10 "
                    "WHERE shipperid = :11" ,
                    [
                        requested_shipper.shippername,
                        requested_shipper.shipperaddress,
                        requested_shipper.shippercity,
                        requested_shipper.shipperstate,
                        requested_shipper.shippercountry,
                        requested_shipper.shipperpostalcode,
                        requested_shipper.shipperphone,
                        requested_shipper.shipperfax,
                        requested_shipper.shippertollfree,
                        requested_shipper.shippercontact,
                        str(requested_shipper.shipperid)
                    ]
                )
                self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                return 0
            elif one_row[0] == 2:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error updating data. Updating shipper name already exists.'
                )
                return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error updating data. No data for updating available '
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           'Check your log.')
            # log with error.code and error.message
            return -1
        finally:
            my_curr.close()


    def insert_shipper(self, requested_shipper):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT count(*) "
                "FROM shipper "
                "WHERE shippername = '" + str(requested_shipper.shippername) + "'"
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 0:
                my_curr.execute(
                    "INSERT INTO shipper("
                    "shippername, shipperaddress, shippercity, "
                    "shipperstate, shippercountry, shipperpostalcode, "
                    "shipperphone, shipperfax, shippertollfree, "
                    "shippercontact) "
                    "VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10) ",
                    [requested_shipper.shippername, requested_shipper.shipperaddress,
                     requested_shipper.shippercity, requested_shipper.shipperstate,
                     requested_shipper.shippercountry, requested_shipper.shipperpostalcode,
                     requested_shipper.shipperphone,  requested_shipper.shipperfax,
                     requested_shipper.shippertollfree, requested_shipper.shippercontact]
                )
                my_curr.execute(
                    "SELECT count(*) "
                    "FROM shipper "
                    "WHERE shippername = '" + str(requested_shipper.shippername) + "'"
                )
                one_row = my_curr.fetchone()
                if one_row[0] == 1:
                    my_curr.execute(
                        "SELECT shipperid "
                        "FROM shipper "
                        "WHERE shippername = '" + str(requested_shipper.shippername) + "'"
                    )
                    one_row = my_curr.fetchone()
                    requested_shipper.shipperid = one_row[0]
                    self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                    return 0
                else:
                    self.update_windowmessage_signal.emit(-100000,
                                                          'Error inserting data.'
                                                          'Insert query did not commit.')
                    return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error inserting data. '
                    'Check if inserting shipper name already exists'
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000,
                                                  'Error has occurred executing query. '
                                                  'Check your log.')
            # log
            return -1
        finally:
            my_curr.close()


class LoadTypeQueries(QGraphicsObject):

    update_windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_connection):
        super().__init__()
        self.app_connection = app_connection

    def types_count(self):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute('SELECT count(*) FROM loadtype')
            type_fetch_result = my_curr.fetchone()
            return type_fetch_result[0]
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           ' Check your log.')
            # log with error.code and error.message
        finally:
            my_curr.close()

    def get_loadtype_byid(self, typeid) -> LoadTypeInstance:
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                'SELECT loadtypeid, loadtypename '
                'FROM loadtype '
                'WHERE loadtypeid = ' + typeid)
            one_row = my_curr.fetchone()
            if one_row is None:
                self.update_windowmessage_signal.emit(-100000, 'No data available')
                return 1
            else:
                return LoadTypeInstance(
                    loadtypeid=one_row[0],
                    loadtypename=one_row[1]
                )
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           ' Check your log.')
            # log with error.code and error.message
            return 1
        finally:
            my_curr.close()


    def delete_loadtype(self, requested_loadtype):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                'SELECT count(*) FROM loadtype '
                'WHERE loadtypeid = '
                + str(requested_loadtype.loadtypeid)
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 1:
                my_curr.execute(
                    'SELECT count(*) from loadconfirmation l '
                    'WHERE l.lcloadtypeid = '
                    + str(requested_loadtype.loadtypeid))
                one_row = my_curr.fetchone()
                if one_row[0] == 0:
                    my_curr.execute('DELETE FROM loadtype '
                                    'WHERE  loadtypeid = '
                                    + str(requested_loadtype.loadtypeid)
                                    )
                    my_curr.execute('SELECT count(*) FROM loadtype '
                                    'WHERE loadtypeid = '
                                    + str(requested_loadtype.loadtypeid)
                                    )
                    one_row = my_curr.fetchone()
                    if one_row[0] == 0:
                        self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                        return 0
                    else:
                        self.update_windowmessage_signal.emit(-100000, 'Error deleting data')
                        return 1
                else:
                    self.update_windowmessage_signal.emit(
                        -100000,
                        'Error deleting data. '
                        'There is(are) record(s) in main table using data from this record'
                    )
                    return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'No data for deletion available. '
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. '
                                                           'Check your log.')
            # log
            return 1
        finally:
            my_curr.close()

    def modify_loadtype(self, requested_loadtype):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT count(*) FROM loadtype "
                "WHERE loadtypeid = "
                + str(requested_loadtype.loadtypeid)
                + " OR loadtypename = '"
                + requested_loadtype.loadtypename
                + "'"
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 1:
                my_curr.execute(
                    'UPDATE loadtype '
                    'set loadtypename = :1 '
                    'WHERE loadtypeid = :2' ,
                    [requested_loadtype.loadtypename, str(requested_loadtype.loadtypeid)]
                )
                self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                return 0
            elif one_row[0] == 2:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error updating data. Updating load type name already exists.'
                )
                return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error updating data. No data for updating available '
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. '
                                                           'Check your log.')
            # log with error.code and error.message
            return -1
        finally:
            my_curr.close()


    def insert_loadtype(self, requested_loadtype):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT count(*) "
                "FROM loadtype "
                "WHERE loadtypename = '" + str(requested_loadtype.loadtypename) + "'"
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 0:
                my_curr.execute(
                    'INSERT INTO loadtype(loadtypename) '
                    'VALUES(:1) ',
                    [requested_loadtype.loadtypename]
                )
                my_curr.execute(
                    "SELECT count(*) "
                    "FROM loadtype "
                    "WHERE loadtypename = '" + str(requested_loadtype.loadtypename) + "'"
                )
                one_row = my_curr.fetchone()
                if one_row[0] == 1:
                    my_curr.execute(
                        "SELECT loadtypeid "
                        "FROM loadtype "
                        "WHERE loadtypename = '" + str(requested_loadtype.loadtypename) + "'"
                    )

                    one_row = my_curr.fetchone()
                    requested_loadtype.loadtypeid = one_row[0]
                    self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                    return 0
                else:
                    self.update_windowmessage_signal.emit(-100000,
                                                          'Error inserting data.'
                                                          'Insert query did not commit.')
                    return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error inserting data. '
                    'Check if inserting type already exists'
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           ' Check your log.')
            # log
            return -1
        finally:
            my_curr.close()


class ConsigneeQueries(QGraphicsObject):

    update_windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_connection):
        super().__init__()
        self.app_connection = app_connection

    def consignees_count(self):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute('SELECT count(*) FROM consignee')
            consignee_fetch_result = my_curr.fetchone()
            return consignee_fetch_result[0]
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           ' Check your log.')
            # log with error.code and error.message
        finally:
            my_curr.close()

    def get_consignee_byid(self, consigneeid:str) -> ConsigneeInstance:
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT consigneeid, consigneename, consigneeaddress, "
                "consigneecity, consigneestate, consigneecountry, "
                "consigneepostalcode, consigneephone, consigneefax, "
                "consigneetollfree, consigneecontact "
                "FROM consignee "
                "WHERE consigneeid = " + consigneeid)
            one_row = my_curr.fetchone()
            if one_row is None:
                self.update_windowmessage_signal.emit(-100000, 'No data available')
                return 1
            else:
                return ConsigneeInstance(
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
                )
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return 1
        finally:
            my_curr.close()


    def delete_consignee(self, requested_consignee):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                'SELECT count(*) FROM consignee '
                'WHERE consigneeid = '
                + str(requested_consignee.consigneeid)
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 1:
                my_curr.execute(
                    'SELECT count(*) from consignee_ref c '
                    'WHERE c.consigneeid = '
                    + str(requested_consignee.consigneeid))
                one_row = my_curr.fetchone()
                if one_row[0] == 0:
                    my_curr.execute(
                        'DELETE FROM consignee '
                        'WHERE  consigneeid = '
                        + str(requested_consignee.consigneeid)
                    )
                    my_curr.execute(
                        'SELECT count(*) FROM consignee '
                        'WHERE consigneeid = '
                        + str(requested_consignee.consigneeid)
                    )
                    one_row = my_curr.fetchone()
                    if one_row[0] == 0:
                        self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                        return 0
                    else:
                        self.update_windowmessage_signal.emit(-100000, 'Error deleting data')
                        return 1
                else:
                    self.update_windowmessage_signal.emit(
                        -100000,
                        'Error deleting data. '
                        'There is(are) record(s) in main table using data from this record'
                    )
                    return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'No data for deletion available. '
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. '
                                                           'Check your log.')
            # log
            return 1
        finally:
            my_curr.close()

    def modify_consignee(self, requested_consignee):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT count(*) FROM consignee "
                "WHERE consigneeid = "
                + str(requested_consignee.consigneeid)
                + " OR consigneename = '"
                + requested_consignee.consigneename
                + "'"
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 1:
                my_curr.execute(
                    "UPDATE consignee "
                    "SET consigneename = :1, "
                    "consigneeaddress = :2, "
                    "consigneecity = :3, "
                    "consigneestate = :4, "
                    "consigneecountry = :5, "
                    "consigneepostalcode = :6, "
                    "consigneephone = :7, "
                    "consigneefax = :8, "
                    "consigneetollfree = :9, "
                    "consigneecontact = :10 "
                    "WHERE consigneeid = :11" ,
                    [
                        requested_consignee.consigneename,
                        requested_consignee.consigneeaddress,
                        requested_consignee.consigneecity,
                        requested_consignee.consigneestate,
                        requested_consignee.consigneecountry,
                        requested_consignee.consigneepostalcode,
                        requested_consignee.consigneephone,
                        requested_consignee.consigneefax,
                        requested_consignee.consigneetollfree,
                        requested_consignee.consigneecontact,
                        str(requested_consignee.consigneeid)
                    ]
                )
                self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                return 0
            elif one_row[0] == 2:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error updating data. Updating consignee name already exists.'
                )
                return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error updating data. No data for updating available '
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           'Check your log.')
            # log with error.code and error.message
            return -1
        finally:
            my_curr.close()


    def insert_consignee(self, requested_consignee):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT count(*) "
                "FROM consignee "
                "WHERE consigneename = '" + str(requested_consignee.consigneename) + "'"
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 0:
                my_curr.execute(
                    "INSERT INTO consignee("
                    "consigneename, consigneeaddress, consigneecity, "
                    "consigneestate, consigneecountry, consigneepostalcode, "
                    "consigneephone, consigneefax, consigneetollfree, "
                    "consigneecontact) "
                    "VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10) ",
                    [requested_consignee.consigneename, requested_consignee.consigneeaddress,
                     requested_consignee.consigneecity, requested_consignee.consigneestate,
                     requested_consignee.consigneecountry, requested_consignee.consigneepostalcode,
                     requested_consignee.consigneephone,  requested_consignee.consigneefax,
                     requested_consignee.consigneetollfree, requested_consignee.consigneecontact]
                )
                my_curr.execute(
                    "SELECT count(*) "
                    "FROM consignee "
                    "WHERE consigneename = '" + str(requested_consignee.consigneename) + "'"
                )
                one_row = my_curr.fetchone()
                if one_row[0] == 1:
                    my_curr.execute(
                        "SELECT consigneeid "
                        "FROM consignee "
                        "WHERE consigneename = '" + str(requested_consignee.consigneename) + "'"
                    )
                    one_row = my_curr.fetchone()
                    requested_consignee.consigneeid = one_row[0]
                    self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                    return 0
                else:
                    self.update_windowmessage_signal.emit(-100000,
                                                          'Error inserting data.'
                                                          'Insert query did not commit.')
                    return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error inserting data. '
                    'Check if inserting consignee name already exists'
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000,
                                                  'Error has occurred executing query. '
                                                  'Check your log.')
            # log
            return -1
        finally:
            my_curr.close()


class CurrencyQueries(QGraphicsObject):

    update_windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_connection):
        super().__init__()
        self.app_connection = app_connection

    def currencies_count(self):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute('SELECT count(*) FROM currency')
            currency_fetch_result = my_curr.fetchone()
            return currency_fetch_result[0]
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           ' Check your log.')
            # log with error.code and error.message
        finally:
            my_curr.close()

    def get_currency_byid(self, currencyid) -> CurrencyInstance:
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                'SELECT currencyid, currencyshortname, currencyname, currencyimagepath '
                'FROM currency '
                'WHERE currencyid = ' + currencyid)
            one_row = my_curr.fetchone()
            if one_row is None:
                self.update_windowmessage_signal.emit(-100000, 'No data available')
                return 1
            else:
                return CurrencyInstance(
                    currencyid=one_row[0],
                    currencyshortname=one_row[1],
                    currencyname=one_row[2],
                    currencyimagepath=one_row[3]
                )
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           ' Check your log.')
            # log with error.code and error.message
            return 1
        finally:
            my_curr.close()


    def delete_currency(self, requested_currency):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                'SELECT count(*) FROM currency '
                'WHERE currencyid = '
                + str(requested_currency.currencyid)
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 1:
                my_curr.execute(
                    'SELECT count(*) from loadconfirmation l '
                    'WHERE l.lccurrencyid = '
                    + str(requested_currency.currencyid))
                one_row = my_curr.fetchone()
                if one_row[0] == 0:
                    my_curr.execute('DELETE FROM currency '
                                    'WHERE  currencyid = '
                                    + str(requested_currency.currencyid)
                                    )
                    my_curr.execute('SELECT count(*) FROM currency '
                                    'WHERE currencyid = '
                                    + str(requested_currency.currencyid)
                                    )
                    one_row = my_curr.fetchone()
                    if one_row[0] == 0:
                        self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                        return 0
                    else:
                        self.update_windowmessage_signal.emit(-100000, 'Error deleting data')
                        return 1
                else:
                    self.update_windowmessage_signal.emit(
                        -100000,
                        'Error deleting data. '
                        'There is(are) record(s) in main table using data from this record'
                    )
                    return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'No data for deletion available. '
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. '
                                                           'Check your log.')
            # log
            return 1
        finally:
            my_curr.close()

    def modify_currency(self, requested_currency):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT count(*) FROM currency "
                "WHERE currencyid = "
                + str(requested_currency.currencyid)
                + " OR currencyshortname = '"
                + requested_currency.currencyshortname
                + "'"
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 1:
                my_curr.execute(
                    'UPDATE currency '
                    'SET currencyshortname = :1, '
                    'currencyname = :2, '
                    'currencyimagepath = :3 '
                    'WHERE currencyid = :4' ,
                    [requested_currency.currencyshortname,
                     requested_currency.currencyname,
                     requested_currency.currencyimagepath,
                     str(requested_currency.currencyid)
                     ]
                )
                self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                return 0
            elif one_row[0] == 2:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error updating data. Updating  currency name already exists.'
                )
                return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error updating data. No data for updating available '
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. '
                                                           'Check your log.')
            # log with error.code and error.message
            return -1
        finally:
            my_curr.close()


    def insert_currency(self, requested_currency):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT count(*) "
                "FROM currency "
                "WHERE currencyshortname = '" + str(requested_currency.currencyshortname) + "'"
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 0:
                my_curr.execute(
                    'INSERT INTO currency(currencyshortname, currencyname, currencyimagepath) '
                    'VALUES(:1, :2, :3) ',
                    [requested_currency.currencyshortname,
                     requested_currency.currencyname,
                     requested_currency.currencyimagepath
                    ]
                )
                my_curr.execute(
                    "SELECT count(*) "
                    "FROM currency "
                    "WHERE currencyshortname = '" + str(requested_currency.currencyshortname) + "'"
                )
                one_row = my_curr.fetchone()
                if one_row[0] == 1:
                    my_curr.execute(
                        "SELECT currencyid "
                        "FROM currency "
                        "WHERE currencyshortname = '" + str(requested_currency.currencyshortname) + "'"
                    )

                    one_row = my_curr.fetchone()
                    requested_currency.currencyid = one_row[0]
                    self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                    return 0
                else:
                    self.update_windowmessage_signal.emit(-100000,
                                                          'Error inserting data.'
                                                          'Insert query did not commit.')
                    return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error inserting data. '
                    'Check if inserting currency already exists'
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           ' Check your log.')
            # log
            return -1
        finally:
            my_curr.close()


class BrokerQueries(QGraphicsObject):

    update_windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_connection):
        super().__init__()
        self.app_connection = app_connection

    def brokers_count(self):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute('SELECT count(*) FROM custombroker')
            broker_fetch_result = my_curr.fetchone()
            return broker_fetch_result[0]
        except cx_Oracle.Error as exception:
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           ' Check your log.')
            # log with error.code and error.message

        # log this error
        finally:
            my_curr.close()

    def get_broker_by_id(self, brokerid:str) -> BrokerInstance:
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT custombrokerid, custombrokername, custombrokerphone, "
                "custombrokerfax, custombrokertollfree, custombrokercontact "
                "FROM custombroker "
                "WHERE custombrokerid = " + brokerid)
            one_row = my_curr.fetchone()
            if one_row is None:
                self.update_windowmessage_signal.emit(-100000, 'No data available')
                return 1
            else:
                return BrokerInstance(
                    custombrokerid=one_row[0],
                    custombrokername=one_row[1],
                    custombrokerphone=one_row[2],
                    custombrokerfax=one_row[3],
                    custombrokertollfree=one_row[4],
                    custombrokercontact=one_row[5]
                )
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           ' Check your log.')
            # log with error.code and error.message
            return 1
        finally:
            my_curr.close()


    def delete_broker(self, requested_broker):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                'SELECT count(*) FROM custombroker '
                'WHERE custombrokerid = '
                + str(requested_broker.custombrokerid)
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 1:
                my_curr.execute(
                    'SELECT count(*) from loadconfirmation l '
                    'WHERE l.lccustombrokerid = '
                    + str(requested_broker.custombrokerid))
                one_row = my_curr.fetchone()
                if one_row[0] == 0:
                    my_curr.execute(
                        'DELETE FROM custombroker '
                        'WHERE  custombrokerid = '
                        + str(requested_broker.custombrokerid)
                    )
                    my_curr.execute(
                        'SELECT count(*) FROM custombroker '
                        'WHERE custombrokerid = '
                        + str(requested_broker.custombrokerid)
                    )
                    one_row = my_curr.fetchone()
                    if one_row[0] == 0:
                        self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                        return 0
                    else:
                        self.update_windowmessage_signal.emit(-100000, 'Error deleting data')
                        return 1
                else:
                    self.update_windowmessage_signal.emit(
                        -100000,
                        'Error deleting data. '
                        'There is(are) record(s) in main table using data from this record'
                    )
                    return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'No data for deletion available. '
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. '
                                                           'Check your log.')
            # log
            return 1
        finally:
            my_curr.close()

    def modify_broker(self, requested_broker):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT count(*) FROM custombroker "
                "WHERE custombrokerid = "
                + str(requested_broker.custombrokerid)
                + " OR custombrokername = '"
                + requested_broker.custombrokername
                + "'"
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 1:
                my_curr.execute(
                    "UPDATE custombroker "
                    "SET custombrokername = :1, "
                    "custombrokerphone = :2, "
                    "custombrokerfax = :3, "
                    "custombrokertollfree = :4, "
                    "custombrokercontact = :5 "
                    "WHERE custombrokerid = :6" ,
                    [
                        requested_broker.custombrokername,
                        requested_broker.custombrokerphone,
                        requested_broker.custombrokerfax,
                        requested_broker.custombrokertollfree,
                        requested_broker.custombrokercontact,
                        str(requested_broker.custombrokerid)
                    ]
                )
                self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                return 0
            elif one_row[0] == 2:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error updating data. Updating broker name already exists.'
                )
                return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error updating data. No data for updating available '
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           ' Check your log.')
            # log with error.code and error.message
            return -1
        finally:
            my_curr.close()


    def insert_broker(self, requested_broker):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT count(*) "
                "FROM custombroker "
                "WHERE custombrokername = '" + str(requested_broker.custombrokername) + "'"
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 0:
                my_curr.execute(
                    "INSERT INTO custombroker("
                    "custombrokername, custombrokerphone, "
                    "custombrokerfax, custombrokertollfree, custombrokercontact) "
                    "VALUES(:1, :2, :3, :4, :5) ",
                    [requested_broker.custombrokername, requested_broker.custombrokerphone,
                     requested_broker.custombrokerfax, requested_broker.custombrokertollfree,
                     requested_broker.custombrokercontact]
                )
                my_curr.execute(
                    "SELECT count(*) "
                    "FROM custombroker "
                    "WHERE custombrokername = '" + str(requested_broker.custombrokername) + "'"
                )
                one_row = my_curr.fetchone()
                if one_row[0] == 1:
                    my_curr.execute(
                        "SELECT custombrokerid "
                        "FROM custombroker "
                        "WHERE custombrokername = '" + str(requested_broker.custombrokername) + "'"
                    )
                    one_row = my_curr.fetchone()
                    requested_broker.custombrokerid = one_row[0]
                    self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                    return 0
                else:
                    self.update_windowmessage_signal.emit(-100000,
                                                          'Error inserting data.'
                                                          'Insert query did not commit.')
                    return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error inserting data. '
                    'Check if inserting broker name already exists'
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000,
                                                  'Error has occurred executing query. '
                                                  'Check your log.')
            # log
            return -1
        finally:
            my_curr.close()


class CarrierQueries(QGraphicsObject):

    update_windowmessage_signal = pyqtSignal(int, str)

    def __init__(self, app_connection):
        super().__init__()
        self.app_connection = app_connection

    def carriers_count(self):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute('SELECT count(*) FROM carrier')
            carrier_fetch_result = my_curr.fetchone()
            return carrier_fetch_result[0]
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           ' Check your log.')
            # log with error.code and error.message
        finally:
            my_curr.close()

    def get_carrier_byid(self, carrierid:str) -> CarrierInstance:
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT carrierid, carriername, carrieraddress, "
                "carriercity, carrierstate, carriercountry, "
                "carrierpostalcode, carrierphone, carrierfax, "
                "carriertollfree, carriercontact "
                "FROM carrier "
                "WHERE carrierid = " + carrierid)
            one_row = my_curr.fetchone()
            if one_row is None:
                self.update_windowmessage_signal.emit(-100000, 'No data available')
                return 1
            else:
                return CarrierInstance(
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
                )
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. Check your log.')
            # log
            return 1
        finally:
            my_curr.close()


    def delete_carrier(self, requested_carrier):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                'SELECT count(*) FROM carrier '
                'WHERE carrierid = '
                + str(requested_carrier.carrierid)
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 1:
                my_curr.execute(
                    'SELECT count(*) from loadconfirmation l '
                    'WHERE l.lccarrierid = '
                    + str(requested_carrier.carrierid))
                one_row = my_curr.fetchone()
                if one_row[0] == 0:
                    my_curr.execute(
                        'DELETE FROM carrier '
                        'WHERE  carrierid = '
                        + str(requested_carrier.carrierid)
                    )
                    my_curr.execute(
                        'SELECT count(*) FROM carrier '
                        'WHERE carrierid = '
                        + str(requested_carrier.carrierid)
                    )
                    one_row = my_curr.fetchone()
                    if one_row[0] == 0:
                        self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                        return 0
                    else:
                        self.update_windowmessage_signal.emit(-100000, 'Error deleting data')
                        return 1
                else:
                    self.update_windowmessage_signal.emit(
                        -100000,
                        'Error deleting data. '
                        'There is(are) record(s) in main table using data from this record'
                    )
                    return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'No data for deletion available. '
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query. '
                                                           'Check your log.')
            # log
            return 1
        finally:
            my_curr.close()

    def modify_carrier(self, requested_carrier):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT count(*) FROM carrier "
                "WHERE carrierid = "
                + str(requested_carrier.carrierid)
                + " OR carriername = '"
                + requested_carrier.carriername
                + "'"
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 1:
                my_curr.execute(
                    "UPDATE carrier "
                    "SET carriername = :1, "
                    "carrieraddress = :2, "
                    "carriercity = :3, "
                    "carrierstate = :4, "
                    "carriercountry = :5, "
                    "carrierpostalcode = :6, "
                    "carrierphone = :7, "
                    "carrierfax = :8, "
                    "carriertollfree = :9, "
                    "carriercontact = :10 "
                    "WHERE carrierid = :11" ,
                    [
                        requested_carrier.carriername,
                        requested_carrier.carrieraddress,
                        requested_carrier.carriercity,
                        requested_carrier.carrierstate,
                        requested_carrier.carriercountry,
                        requested_carrier.carrierpostalcode,
                        requested_carrier.carrierphone,
                        requested_carrier.carrierfax,
                        requested_carrier.carriertollfree,
                        requested_carrier.carriercontact,
                        str(requested_carrier.carrierid)
                    ]
                )
                self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                return 0
            elif one_row[0] == 2:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error updating data. Updating carrier name already exists.'
                )
                return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error updating data. No data for updating available '
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000, 'Error has occurred executing query.'
                                                           'Check your log.')
            # log with error.code and error.message
            return -1
        finally:
            my_curr.close()


    def insert_carrier(self, requested_carrier):
        try:
            my_curr = self.app_connection.cursor()
            my_curr.execute(
                "SELECT count(*) "
                "FROM carrier "
                "WHERE carriername = '" + str(requested_carrier.carriername) + "'"
            )
            one_row = my_curr.fetchone()
            if one_row[0] == 0:
                my_curr.execute(
                    "INSERT INTO carrier("
                    "carriername, carrieraddress, carriercity, "
                    "carrierstate, carriercountry, carrierpostalcode, "
                    "carrierphone, carrierfax, carriertollfree, "
                    "carriercontact) "
                    "VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10) ",
                    [requested_carrier.carriername, requested_carrier.carrieraddress,
                     requested_carrier.carriercity, requested_carrier.carrierstate,
                     requested_carrier.carriercountry, requested_carrier.carrierpostalcode,
                     requested_carrier.carrierphone,  requested_carrier.carrierfax,
                     requested_carrier.carriertollfree, requested_carrier.carriercontact]
                )
                my_curr.execute(
                    "SELECT count(*) "
                    "FROM carrier "
                    "WHERE carriername = '" + str(requested_carrier.carriername) + "'"
                )
                one_row = my_curr.fetchone()
                if one_row[0] == 1:
                    my_curr.execute(
                        "SELECT carrierid "
                        "FROM carrier "
                        "WHERE carriername = '" + str(requested_carrier.carriername) + "'"
                    )
                    one_row = my_curr.fetchone()
                    requested_carrier.carrierid = one_row[0]
                    self.update_windowmessage_signal.emit(100002, 'Operation completed successfully')
                    return 0
                else:
                    self.update_windowmessage_signal.emit(-100000,
                                                          'Error inserting data.'
                                                          'Insert query did not commit.')
                    return 1
            else:
                self.update_windowmessage_signal.emit(
                    -100000,
                    'Error inserting data. '
                    'Check if inserting carrier name already exists'
                )
                return 1
        except cx_Oracle.Error as exception:
            error, = exception.args
            self.update_windowmessage_signal.emit(-100000,
                                                  'Error has occurred executing query. '
                                                  'Check your log.')
            # log
            return -1
        finally:
            my_curr.close()









