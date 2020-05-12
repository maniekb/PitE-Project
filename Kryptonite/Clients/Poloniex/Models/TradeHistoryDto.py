class TradeHistoryDto:
    def __init__(self, global_trade_id, trade_id, date, type, rate,
                 amount, total, order_umber):
        self.global_trade_id = global_trade_id
        self.trade_id = trade_id
        self.date = date
        self.type = type
        self.rate = rate
        self.amount = amount
        self.total = total
        self.order_umber = order_umber


def to_trade_history(dct):
    return TradeHistoryDto(dct['globalTradeID'], dct['tradeID'], dct['date'], dct['type'],
                           dct['rate'], dct['amount'], dct['total'], dct['orderNumber'])
