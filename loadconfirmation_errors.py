""""""
class MissingBrokerInfoError(Exception):

    def __init__(self, loadconfirmation_queries):
        loadconfirmation_queries.update_windowmessage_signal.emit(
            -100000,
            'You must add custom broker to newly created load confirmation'
        )

class MissingCarrierInfoError(Exception):

    def __init__(self, loadconfirmation_queries):
        loadconfirmation_queries.update_windowmessage_signal.emit(
            -100000,
            'You must add carrier to newly created load confirmation'
        )

class MissingShipperInfoError(Exception):

    def __init__(self, loadconfirmation_queries):
        loadconfirmation_queries.update_windowmessage_signal.emit(
            -100000,
            'You must add at least one shipper to newly created load confirmation'
        )

class MissingConsigneeInfoError(Exception):

    def __init__(self, loadconfirmation_queries):
        loadconfirmation_queries.update_windowmessage_signal.emit(
            -100000,
            'You must add at least one consignee to newly created load confirmation'
        )

class MissingNumberQuantityRateError(Exception):

    def __init__(self, loadconfirmation_queries):
        loadconfirmation_queries.update_windowmessage_signal.emit(
            -100000,
            'You must assign load confirmation number, quantity and agreed rate'
        )

class MissingChosenImageError(Exception):

    def __init__(self, currencies_queries):
        currencies_queries.update_windowmessage_signal.emit(
            -100000,
            'You must selected an image for this currency.'
        )

class ImageDimensionError(Exception):

    def __init__(self, currencies_queries):
        currencies_queries.update_windowmessage_signal.emit(
            -100000,
            "You must adjust selected image's  dimension: W-60 X H-28."
        )
