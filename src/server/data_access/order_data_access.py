from forms import CustomerOrderForm, UpdateOrderStatusForm
from datetime import datetime
from bson import ObjectId
from bson.json_util import dumps

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

    @staticmethod
    def return_update(status, message, cell, vendor):
        return {
            'status': status,
            'message': message,
            'result': {
                'cell': cell,
                'vendor': vendor
            }
        }

    def customer_order(self, requestForm, vendorMenu, customerLogin):
        status, message = False, ""
        form = CustomerOrderForm(requestForm)
        if form.validate():
            items = vendorMenu.find_one({"username": form.vendor.data})['menu']
            image = None
            for item in items:
                if item["itemName"]== form.itemname.data:
                    image = item["image_url"]
            name = customerLogin.find_one({"username": self.username})
            full_name = name["firstname"]+ " " + name["lastname"]
            entry = {
                "status": "processing",
                "timestamp": datetime.utcnow(),
                "vendor": form.vendor.data,
                "customer": self.username,
                "customer_name": full_name,
                "price": form.price.data,
                "quantity": form.quantity.data,
                "itemname": form.itemname.data,
                "image_url": image
            }
            _id = self.transactions.insert(entry)
            # print _id
            status = True
            message = 'Order Submitted Successfully!'
        else:
            message = 'Invalid form!'
            _id = None
        return OrderDataAccess.return_output(status, message, str(_id))

    def update_order_status(self, requestForm, customerInfo, vendorInfo):
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
            trans = self.transactions.find_one({"_id": _id})
            # print trans["customer"]
            customer = trans["customer"]
            num = customerInfo.find_one({"username": customer})["cell"]
            vendor_name = vendorInfo.find_one({"username": trans["vendor"]})['storeName']
            status = True
            message = 'Update Order Successfully!'
        else:
            message = 'Invalid form!'
            _id = None
        return OrderDataAccess.return_update(status, message, num, vendor_name)
