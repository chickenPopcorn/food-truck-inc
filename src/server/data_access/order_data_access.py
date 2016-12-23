from forms import CustomerOrderForm
from datetime import datetime

class OrderDataAccess:
    def __init__(self, transactions, username):
        self.transactions = transactions
        self.username = username

    @staticmethod
    def return_output(status, message, user):
        return {
            'status': status,
            'message': message,
            'result': {
                'user': user
            }
        }

    def customer_order(self, requestForm):
        status, message = False, ""
        form = CustomerOrderForm(requestForm)
        if form.validate():
            entry = {
                "status": "processing",
                "timestamp": datetime.utcnow(),
                "vendor": form.vendor.data,
                "customer": self.username,
                "items": form.items.data
            }
            # print form.items.data
            _id = self.transactions.insert(entry)
            # print _id
            status = True
            message = 'Order Submitted Successfully!'
        else:
            message = 'Invalid form!'
            _id = None
        return OrderDataAccess.return_output(status, message, str(_id))

