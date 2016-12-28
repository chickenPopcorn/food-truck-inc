//
//  MenuViewController.swift
//  foodTruck
//
//  Created by ruicong xie on 12/7/16.
//  Copyright © 2016 ruicong xie. All rights reserved.
//

import UIKit
import SwiftyJSON

class MenuViewController: UIViewController,UITableViewDelegate, UITableViewDataSource {
    
    @IBOutlet weak var pageTitle: UINavigationItem!
    
    var vendor: String = ""
    var vendorUsername: String = ""
    
    var orders = [OrderItem]()
    
    @IBOutlet weak var menuTable: UITableView!
    let cellReuseIdentifier = "cell"
    
    var menu = [MenuItem]()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print("MenuViewDidLoad")
        print("the vendor is >>> " + self.vendor)
        self.menuTable.delegate = self
        self.menuTable.dataSource = self
        pageTitle.title = self.vendor+"'s Menu"
        requestMenu()
    }
    
    private func requestMenu() {
        let request = NSMutableURLRequest(url: URL(string: serverDomain+"/get_menu_item/\(vendorUsername)")!)
        request.httpMethod = "GET"
        let session = URLSession.shared
        
        let task = session.dataTask(with: request as URLRequest, completionHandler: {data, response, error -> Void in
            print("Response: \(response)")
            let strData = NSString(data: (data)!, encoding: String.Encoding.utf8.rawValue)!
            print("Body: \(strData)")
            
            if let httpResponse = response as? HTTPURLResponse {
                if(httpResponse.statusCode == 200){
                    //sign up successfully
                    //all ui change must happen in main thread. I think the issue is that async http request is in different thread.
                    //so use this method to push code back to main thread
                    
                    let jsonData = JSON(data: data!) /* get your json data */
                    for (_, value) in jsonData{
                        DispatchQueue.main.async{
                            self.loadAMenuItem(itemName: value["itemName"].stringValue, itemPrice: value["itemPrice"].stringValue, imageUrl: value["image_url"].stringValue)
                            print("loading menu")
                        }
                    }
                    self.do_table_refresh()
                }
            } else {
                assertionFailure("unexpected response")
            }
            
        })
        task.resume()
    }
    
    func do_table_refresh(){
        DispatchQueue.main.async{
            self.menuTable.reloadData()
        }
    }
    func loadAMenuItem (itemName: String, itemPrice: String, imageUrl: String){
        print("itemane is \(itemName) item price is \(itemPrice)")
        let url = URL(string: imageUrl)
        let data = try? Data(contentsOf: url!)
        let photo = UIImage(data: data!)
        menu += [MenuItem(name: itemName.capitalized, photo: photo, price: Double(itemPrice)!)!]
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    // MARK: - Table view data source
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
          return menu.count
    }
    
    private func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        return 1
    }
    

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        // Table view cells are reused and should be dequeued using a cell identifier.
        let cell:MenuViewCell = tableView.dequeueReusableCell( withIdentifier: "cell") as! MenuViewCell
        // Fetches the appropriate meal for the data source layout.
        let menuItem = menu[indexPath.row]
        
        cell.nameLabel.text = menuItem.name
        cell.photoImageView.image = menuItem.photo
        cell.priceLabel.text = "$"+String(menuItem.price)
        
        return cell
    }
    
    override func shouldPerformSegue(withIdentifier identifier: String?, sender: Any?) -> Bool {
        return getTotalOrder() > 0
    }

    func getTotalOrder() -> Int{
        var count = 0
        self.orders.removeAll()
        for section in 0..<self.menuTable.numberOfSections {
            for row in 0..<self.menuTable.numberOfRows(inSection: section) {
                let indexPath = NSIndexPath(row: row, section: section)
                let cell = self.menuTable.cellForRow(at: indexPath as IndexPath) as! MenuViewCell
                // do what you want with the cell
                // Fetches the appropriate meal for the data source layout.
                let menuItem = menu[indexPath.row]
                let item = OrderItem(name: menuItem.name, photo: menuItem.photo, price: menuItem.price)
                if cell.quantity > 0{
                    item?.quantity = cell.quantity
                    self.orders.append(item!)
                    count += 1
                }
            }
        }
        return count
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if let vc = segue.destination as? OrderReviewController{
            print("prepare for order segue")
            vc.orderReview = self.orders
            vc.vendorUsername = self.vendorUsername
        }
    }
}
