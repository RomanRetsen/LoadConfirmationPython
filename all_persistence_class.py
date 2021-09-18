"""This module all object classes used in the application

Initializers for all classes are enriched with default values
"""
class UserInstance():

    def __init__(self,
                 userid=None, userfname=None, usersname=None, password=None
                 ):
        self.userid = userid
        self.userfname = userfname
        self.usersname = usersname
        self.password = password

class BrokerInstance():

    def __init__(self,
                 custombrokerid=None, custombrokername=None, custombrokerphone=None,
                 custombrokerfax=None, custombrokertollfree=None, custombrokercontact=None
                 ):
        self.custombrokerid = custombrokerid
        self.custombrokername = custombrokername
        self.custombrokerphone = custombrokerphone
        self.custombrokerfax = custombrokerfax
        self.custombrokertollfree = custombrokertollfree
        self.custombrokercontact = custombrokercontact

class CarrierInstance():

    def __init__(self,
                 carrierid=None, carriername=None, carrieraddress=None,
                 carriercity=None, carrierstate=None, carriercountry=None,
                 carrierpostalcode=None, carrierphone=None, carrierfax=None,
                 carriertollfree=None, carriercontact=None
                 ):
        self.carrierid = carrierid
        self.carriername = carriername
        self.carrieraddress = carrieraddress
        self.carriercity = carriercity
        self.carrierstate = carrierstate
        self.carriercountry = carriercountry
        self.carrierpostalcode = carrierpostalcode
        self.carrierphone = carrierphone
        self.carrierfax = carrierfax
        self.carriertollfree = carriertollfree
        self.carriercontact = carriercontact

class ConsigneeInstance():

    def __init__(self,
                 consigneeid=None, consigneename=None, consigneeaddress=None,
                 consigneecity=None, consigneestate=None, consigneecountry=None,
                 consigneepostalcode=None, consigneephone=None, consigneefax=None,
                 consigneetollfree=None, consigneecontact=None
                 ):
        self.consigneeid = consigneeid
        self.consigneename = consigneename
        self.consigneeaddress = consigneeaddress
        self.consigneecity = consigneecity
        self.consigneestate = consigneestate
        self.consigneecountry = consigneecountry
        self.consigneepostalcode = consigneepostalcode
        self.consigneephone = consigneephone
        self.consigneefax = consigneefax
        self.consigneetollfree = consigneetollfree
        self.consigneecontact = consigneecontact

class ConsigneeRefInstance():

    def __init__(self, consigneerefid=None, loadconfirmationid=None,
                 consigneeid=None, consigneedate=None, consigneetime=None
                 ):
        self.consigneerefid = consigneerefid
        self.loadconfirmationid = loadconfirmationid
        self.consigneeid = consigneeid
        self.consigneedate = consigneedate
        self.consigneetime = consigneetime

class ShipperInstance():

    def __init__(self, shipperid=None, shippername=None, shipperaddress=None,
                 shippercity=None, shipperstate=None, shippercountry=None,
                 shipperpostalcode=None, shipperphone=None, shipperfax=None,
                 shippertollfree=None, shippercontact=None
                 ):
        self.shipperid = shipperid
        self.shippername = shippername
        self.shipperaddress = shipperaddress
        self.shippercity = shippercity
        self.shipperstate = shipperstate
        self.shippercountry = shippercountry
        self.shipperpostalcode = shipperpostalcode
        self.shipperphone = shipperphone
        self.shipperfax = shipperfax
        self.shippertollfree = shippertollfree
        self.shippercontact = shippercontact

class ShipperRefInstance():

    def __init__(self, shipperrefid=None, loadconfirmationid=None,
                 shipperid=None, shipperdate=None, shippertime=None
                 ):
        self.shipperrefid = shipperrefid
        self.loadconfirmationid = loadconfirmationid
        self.shipperid = shipperid
        self.shipperdate = shipperdate
        self.shippertime = shippertime

class LoadConfirmationInstance():

    def __init__(self,
                 lcid=None, lccurrencyid=None, lcloadtypeid=None,
                 lccarrierid=None, lccustombrokerid=None, lcnote=None,
                 lcno=None, lcdatecreated=None, lcagreedrate=None,
                 lccurrencyshortname=None, lcquantity=None, lcloadtypename=None,
                 lccarriername=None, lccustombrokername=None, lccreatedby=None
                 ):
        self.lcid = lcid
        self.lccurrencyid = lccurrencyid
        self.lcloadtypeid = lcloadtypeid
        self.lccarrierid = lccarrierid
        self.lccustombrokerid = lccustombrokerid
        self.lcnote = lcnote
        self.lcno = lcno
        self.lcdatecreated = lcdatecreated
        self.lcagreedrate = lcagreedrate
        self.lccurrencyshortname = lccurrencyshortname
        self.lcquantity = lcquantity
        self.lcloadtypename = lcloadtypename
        self.lccarriername = lccarriername
        self.lccustombrokername = lccustombrokername
        self.lccreatedby = lccreatedby

class LoadTypeInstance():

    def __init__(self,
                 loadtypeid=None, loadtypename=None
                 ):
        self.loadtypeid = loadtypeid
        self.loadtypename = loadtypename

class CurrencyInstance():

    def __init__(self,
                 currencyid=None, currencyshortname=None, currencyname=None, currencyimagepath=None
                 ):
        self.currencyid = currencyid
        self.currencyshortname = currencyshortname
        self.currencyname = currencyname
        self.currencyimagepath = currencyimagepath













