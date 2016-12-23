from forms import CustomerOrderForm, UpdateOrderStatusForm
from datetime import datetime
from bson import ObjectId

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

    def update_order_status(self, requestForm):
        status, message = False, ""
        form = UpdateOrderStatusForm(requestForm)
        if form.validate():
            _id = None
            try:
                _id = ObjectId(form.id.data)
            except:
                message = "Invalid Id!"
                return OrderDataAccess.return_output(status, message, str(_id))

            res = self.transactions.update(
                {"_id": _id},
                {
                    "$set": {"status": "Ready for pick up"}
                }
            )
            if res["nModified"] == 0:
                message = 'Id does not exist!'
            else:
                status = True
                message = 'Update Order Successfully!'
        else:
            message = 'Invalid form!'
            _id = None
        return OrderDataAccess.return_output(status, message, str(_id))
