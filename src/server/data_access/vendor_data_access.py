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

    def add_menu_item(self, requestForm, image_url):
        #        print "in add menue item"
        status, message = False, ""
        form = VendorAddMenuItem(requestForm)
        if form.validate():
            if not self.vendors.find_one({"username": self.vendor}) :
                self.vendors.insert({
                    "username": self.vendor,
                    "menu": [
                        {
                            'itemName': form.itemname.data,
                            'itemPrice': form.price.data,
                            'image_url': image_url
                        }
                    ]
                })
                status = True
                message = "item added successfully to menu"
            else:
                if not self.vendors.find_one({
                    "$and": [{"username": self.vendor},
                              {"menu": {"$elemMatch": {'itemName': form.itemname.data}}}]
                }):
                    self.vendors.update_one(
                        {"username": self.vendor},
                        {"$push": {
                            'menu': {
                                "itemName": form.itemname.data,
                                "itemPrice": form.price.data,
                                "image_url": image_url
                            }
                        }})
                    status = True
                    message = "item added successfully to menu"
                else:
                    self.vendors.update_one(
                        {"username": self.vendor},
                        {"$set": {
                            'menu': {
                                "itemName": form.itemname.data,
                                "itemPrice": form.price.data,
                                "image_url": image_url
                            }
                        }})
                    message = "exist item updated successfully in the menu"
        else:
            message = "invalid form input"
        return VendorDataAccess.return_output(status, message)

    def delete_menu_item(self, requestForm):
        status, message = False, ""
        form = VendorDeleteMenuItem(requestForm)
        if form.validate():
            if not self.vendors.find_one({
                "$and": [{"username": self.vendor},
                          {"menu": {"$elemMatch": {'itemName': form.itemname.data}}}]}):
                message = "item doesn't exit in menu"
            else:
                self.vendors.update_one({
                    "username": self.vendor},
                    {"$pull": {"menu": {"itemName": form.itemname.data}}})
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
