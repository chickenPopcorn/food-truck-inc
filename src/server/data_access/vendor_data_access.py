from forms import VendorAddMenuItem, VendorDeleteMenuItem

class VendorDataAccess:
    def __init__(self, vendors, vendor):
        self.vendors = vendors
        if not self.vendors.find_one({

        }):
            vendors.insert_one(
            {
                "username": vendor,
                "loc": { "lng": 0, "lat": 0 },
                "name": "TestFoodTruck",
                "menu_items":[]
            })

        self.vendor = vendor

    def add_menu_item(self, requestForm):
        status, message = False, ""
        form = VendorAddMenuItem(requestForm)
        if form.validate():
            if not self.vendors.find_one({
                "$and": [{"username": self.vendor},
                          {"menu_items": { "$elemMatch": { 'item_name': form.itemname.data}}}]
            }):
                self.vendors.update_one({
                    "username": self.vendor},
                    {"$push": { 'menu_items':{ "item_name": form.itemname.data, "price": form.price.data, }}})
                status = True
                message = "item added successfully to menu"
            else:
                message = "item already exist in the menu"
        else:
            message = "invalid form input"
        return VendorDataAccess.return_output(status, message)

    def delete_menu_item(self, requestForm):
        status, message = False, ""
        form = VendorDeleteMenuItem(requestForm)
        if form.validate():
            if not self.vendors.find_one({
                "$and": [{"username": self.vendor},
                          {"menu_items": { "$elemMatch": { 'item_name': form.itemname.data}}}]}):
                message = "item doesn't exit in menu"
            else:
                self.vendors.update_one({
                    "username": self.vendor},
                    {"$pull": { 'menu_items':{"item_name": form.itemname.data}}})
                status = True
                message = "item deleted successfully from menu"
        else:
            message = "item name required"

        return VendorDataAccess.return_output(status, message)

    @staticmethod
    def return_output(status, message):
        return {
            'status': status,
            'message': message,
        }