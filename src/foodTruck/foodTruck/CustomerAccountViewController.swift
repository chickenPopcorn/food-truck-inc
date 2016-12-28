//
//  CustomerAccountViewController.swift
//  foodTruck
//
//  Created by Ruicong Xie on 12/16/16.
//  Copyright © 2016 ruicong xie. All rights reserved.
//

import UIKit
import SwiftyJSON

class CustomerAccountViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {
    
    @IBOutlet weak var customerName: UILabel!
    @IBOutlet weak var orderTable: UITableView!
   
    
    @IBAction func goToMap(_ sender: Any) {
        self.dismiss(animated: true, completion: nil)
        self.performSegue(withIdentifier: "go_to_map", sender: nil)
    }
   
    
    var name : String = ""
    
    
    var orderHistory  = [OrderHistoryItem]()

    
    override func viewWillAppear(_ animated: Bool) {
        loadOrderHistory()
    }
    
    private func loadOrderHistory() {
        let _url = URL(string: serverDomain+"/get_customer_orders")
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
                        self.customerName.text = "\(value["customer_name"].stringValue.capitalized)'s Order History"
                        DispatchQueue.main.async{
                            self.loadAOrderHistory(itemName: value["itemname"].stringValue, itemPrice: value["price"].stringValue, imageUrl: value["image_url"].stringValue, status: value["status"].stringValue, quantity: value["quantity"].stringValue)
                            print("loading menu")
                         
                        }
                    }
                    self.do_table_refresh()
                }
            }
        })
        
        dataTask.resume()
    }

    func loadAOrderHistory(itemName: String, itemPrice: String, imageUrl: String, status: String, quantity: String){
        let url = URL(string: imageUrl)
        let data = try? Data(contentsOf: url!)
        let photo = UIImage(data: data!)
        let historyItem = OrderHistoryItem(name: itemName.capitalized, photo: photo, price: Double(itemPrice)!)!
        historyItem.status = status
        historyItem.quantity = Int(quantity)!
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
        //        loadOrderHistory()
        
        
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
        cell.status.text = menuItem.status
        cell.quantityLabel.text = String("Quantity: "+"1")
        
        return cell
    }
    
    
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
