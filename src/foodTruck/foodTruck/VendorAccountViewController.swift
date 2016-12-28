//
//  VendorAccountController.swift
//  foodTruck
//
//  Created by Ruicong Xie on 12/17/16.
//  Copyright © 2016 ruicong xie. All rights reserved.
//

import UIKit
import SwiftyJSON
import Foundation

class VendorAccountViewController: UIViewController, UITableViewDelegate, UITableViewDataSource{
    
//    @IBOutlet weak var statusBar: UILabel!
    @IBOutlet weak var orderTable: UITableView!
    var username = ""
    var id = [String]()
    
//    var orderHistory = [VendorOrderItem]()
//
//    
//    
//       
//    func do_table_refresh(){
//        DispatchQueue.main.async{
//            self.menuTable.reloadData()
//        }
//    }
//    
//    func loadAOrderHistory (itemName: String, itemPrice: String, imageUrl: String, status: String, quantity: String, id: String){
//        let url = URL(string: imageUrl)
//        let data = try? Data(contentsOf: url!)
//        let photo = UIImage(data: data!)
//        let item = VendorOrderItem(name: itemName.capitalized, photo: photo, price: Double(itemPrice)!)
//        item?.quantity = Int(quantity)!
////        item?.status = status
////        item?.transactionID = id
//        orderHistory.append(item!)
//    }
//
//
//    
//    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
//        return orderHistory.count
//    }
//    
//    private func numberOfSectionsInTableView(tableView: UITableView) -> Int {
//        return 1
//    }
//    
//    private func loadOrderHistory() {
//        let _url = URL(string: serverDomain+"/get_vendor_orders")
//        var request = URLRequest(url: _url!)
//        request.httpMethod = "GET"
//        orderHistory.removeAll()
//        id.removeAll()
//        let session = URLSession.shared
//        let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
//            if (error != nil) {
//                print(error!)
//            } else {
//                let httpResponse = response as? HTTPURLResponse
//                print(httpResponse!)
//                if httpResponse?.statusCode == 200{
//                    let jsonData = JSON(data: data!) /* get your json data */
//                    print("json data is \(jsonData)")
//                    for (_, value) in jsonData{
//                        print ("value is \(value)")
//                        DispatchQueue.main.async{
//                            self.loadAOrderHistory(itemName: value["itemname"].stringValue, itemPrice: value["price"].stringValue, imageUrl: value["image_url"].stringValue, status: value["status"].stringValue, quantity: value["quantity"].stringValue, id: value["id"].stringValue)
//                            print("loading menu")
//                        }
//                    }
//                }
//            }
//        })
//        dataTask.resume()
//        
//    }
//    
//    private func checkOpen()  {
//        let _url = URL(string: serverDomain+"/search/open/\(self.username)")
//        var request = URLRequest(url: _url!)
//        request.httpMethod = "GET"
//        let session = URLSession.shared
//        session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
//            if (error != nil) {
//                print(error!)
//            } else {
//                let httpResponse = response as? HTTPURLResponse
//                if httpResponse?.statusCode == 200{
//                    print("its open")
//                    self.statusBar.backgroundColor = UIColor.green
//                    self.statusBar.text = "Your Store is Currently Open"
//                }
//            }
//        })
//    }
//    
//
//    func switchValueDidChange(toggle: UISwitch) {
//        
//        let _url = URL(string: serverDomain+"/update_order_status")
//        var request = URLRequest(url: _url!)
//        request.httpMethod = "POST"
//        let payload = "id=\(id[toggle.tag])"
//        request.httpBody = payload.data(using: String.Encoding.utf8)
//    
//        let session = URLSession.shared
//        let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
//            if (error != nil) {
//                print(error!)
//            } else {
//                let httpResponse = response as? HTTPURLResponse
//                print(httpResponse!)
//                if httpResponse?.statusCode == 200{
//                    toggle.isEnabled = false
//                    print("this is row")
//                    print(toggle.tag)
//                }
//                else{
//                    toggle.setOn(false, animated: true)
//                }
//            }
//        })
//        dataTask.resume()
//    }
//    
//    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
//        // Table view cells are reused and should be dequeued using a cell identifier.
//        let cell: VendorOrderViewCell = tableView.dequeueReusableCell( withIdentifier: "vendorOrderCell")
//            as! VendorOrderViewCell
//        // Fetches the appropriate meal for the data source layout.
//        let menuItem = orderHistory[indexPath.row]
//        cell.nameLabel.text = menuItem.name
//        cell.photoImageView.image = menuItem.photo
//        cell.priceLabel.text = "$"+String(menuItem.price)
////        let toggle = UISwitch()
//        print("here")
////        if (menuItem.status == "Ready for pick up"){
////            toggle.setOn(true, animated: true)
////            toggle.isEnabled = false
////        }
////        toggle.addTarget(self, action: #selector(switchValueDidChange), for: .valueChanged)
////        toggle.tag = indexPath.row
////        id[indexPath.row] = menuItem.transactionID
////        cell.accessoryView = toggle
////        print (cell.nameLabel.text!)
//        return cell
//        
//    }
//
//
//    
//    
    @IBAction func goToOpenShop(_
        sender: Any) {
        self.dismiss(animated: true, completion: nil)
        self.performSegue(withIdentifier: "open_shop", sender: nil)
        
    }
//    override func viewDidLoad() {
//        super.viewDidLoad()
//        // Do any additional setup after loading the view.
//        self.menuTable.delegate = self
//        self.menuTable.dataSource = self
////        checkOpen()
//        loadOrderHistory()
//        
//    }
//    
//    override func didReceiveMemoryWarning() {
//        super.didReceiveMemoryWarning()
//        // Dispose of any resources that can be recreated.
//    }
//
//    
    
    
        private func checkOpen()  {
            let _url = URL(string: serverDomain+"/search/open/\(self.username)")
            var request = URLRequest(url: _url!)
            request.httpMethod = "GET"
            let session = URLSession.shared
            session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
                if (error != nil) {
                    print(error!)
                } else {
                    let httpResponse = response as? HTTPURLResponse
                    if httpResponse?.statusCode == 200{
                        print("its open")
//                        self.statusBar.backgroundColor = UIColor.green
//                        self.statusBar.text = "Your Store is Currently Open"
                        
                    }
                }
            })
        }
    
    var name : String = ""
    
    
    var orderHistory  = [OrderHistoryItem]()
    
    
    override func viewWillAppear(_ animated: Bool) {
    }
    
    private func loadOrderHistory() {
        let _url = URL(string: serverDomain+"/get_vendor_orders")
        var request = URLRequest(url: _url!)
        request.httpMethod = "GET"
        orderHistory.removeAll()
        let session = URLSession.shared
        let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
            if (error != nil) {
                print(error!)
            } else {
                let httpResponse = response as? HTTPURLResponse
                print(httpResponse!)
                if httpResponse?.statusCode == 200{
                    let jsonData = JSON(data: data!) /* get your json data */
                    for (_, value) in jsonData{
                        DispatchQueue.main.async{
                            self.loadAOrderHistory(itemName: value["itemname"].stringValue, itemPrice: value["price"].stringValue, imageUrl: value["image_url"].stringValue, status: value["status"].stringValue, quantity: value["quantity"].stringValue,id: value["id"].stringValue)
                            print("loading menu")
                            
                        }
                    }
                    
                }
                self.do_table_refresh()
            }
        })
        
        dataTask.resume()
    }
    
    
    func switchValueDidChange(toggle: UISwitch) {
        toggle.isEnabled = false
        print("this is row")
        print(toggle.tag)
        
                let _url = URL(string: serverDomain+"/update_order_status")
                var request = URLRequest(url: _url!)
                request.httpMethod = "POST"
                let payload = "id=\(id[toggle.tag])"
                print (payload)
                request.httpBody = payload.data(using: String.Encoding.utf8)

                let session = URLSession.shared
                let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
                    if (error != nil) {
                        print(error!)
                    } else {
                        let httpResponse = response as? HTTPURLResponse
                        print(httpResponse!)
                        if httpResponse?.statusCode == 200{

        
                        }
                        else{
                            toggle.setOn(false, animated: true)
                        }
                    }
                })
                dataTask.resume()
            }

    
    func loadAOrderHistory(itemName: String, itemPrice: String, imageUrl: String, status: String, quantity: String, id: String){
        let url = URL(string: imageUrl)
        let data = try? Data(contentsOf: url!)
        let photo = UIImage(data: data!)
        let historyItem = OrderHistoryItem(name: itemName.capitalized, photo: photo, price: Double(itemPrice)!)!
        historyItem.status = id
        historyItem.quantity = Int(quantity)!
        print(historyItem.quantity)
        orderHistory += [historyItem]
    }
    
    func do_table_refresh(){
        DispatchQueue.main.async{
            self.orderTable.reloadData()
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.orderTable.delegate = self
        self.orderTable.dataSource = self
        loadOrderHistory()
        
        // Do any additional setup after loading the view.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    // MARK: - Table view data source
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return orderHistory.count
    }
    
    private func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        return 1
    }
    
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        // Table view cells are reused and should be dequeued using a cell identifier.
        let cell:OrderViewCell = tableView.dequeueReusableCell( withIdentifier: "orderCell") as!  OrderViewCell
        
        // Fetches the appropriate meal for the data source layout.
        let menuItem = orderHistory[indexPath.row]
        
        cell.nameLabel.text = menuItem.name
        cell.photoImageView.image = menuItem.photo
        cell.priceLabel.text = "Price: $"+String(menuItem.price)
        cell.quantityLabel.text = "Quantity: "+String(menuItem.quantity)
        let toggle = UISwitch()
        id.append(menuItem.status)
     
//        if (menuItem.status == "Ready for pick up"){
//            toggle.setOn(true, animated: true)
//            toggle.isEnabled = false
//        }
        toggle.addTarget(self, action: #selector(switchValueDidChange), for: .valueChanged)
        toggle.tag = indexPath.row
//        id[indexPath.row] = menuItem.transactionID
        cell.accessoryView = toggle
        print (cell.nameLabel.text!)
        
        return cell
    }

}
