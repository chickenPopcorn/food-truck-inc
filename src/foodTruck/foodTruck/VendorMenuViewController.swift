//
//  VendorMenuViewController.swift
//  foodTruck
//
//  Created by Ruicong Xie on 12/22/16.
//  Copyright © 2016 ruicong xie. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON


class VendorMenuViewController: UIViewController,UITableViewDelegate, UITableViewDataSource {
    
    @IBOutlet weak var menuTable: UITableView!
    
    var menu = [MenuItem]()
    
    private func requestMenu() {
        let request = NSMutableURLRequest(url: URL(string: serverDomain+"/get_menu_item")!)
        request.httpMethod = "GET"
        let session = URLSession.shared
        
        let task = session.dataTask(with: request as URLRequest, completionHandler: {data, response, error -> Void in
            print("Response: \(response)")
            let strData = NSString(data: (data)!, encoding: String.Encoding.utf8.rawValue)!
            print("Body: \(strData)")

            if let httpResponse = response as? HTTPURLResponse {
                if(httpResponse.statusCode == 200){
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

    override func viewDidLoad() {
        super.viewDidLoad()
        requestMenu()
        self.menuTable.delegate = self
        self.menuTable.dataSource = self
        print("view load is done")
        // Do any additional setup after loading the view.
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return menu.count
    }
    
    private func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        // Table view cells are reused and should be dequeued using a cell identifier.
        let cell:VendorMenuViewCell = tableView.dequeueReusableCell( withIdentifier: "vendorMenuCell") as! VendorMenuViewCell
        // Fetches the appropriate meal for the data source layout.
        let menuItem = menu[indexPath.row]
        cell.nameLabel.text = menuItem.name
        cell.photoImageView.image = menuItem.photo
        cell.priceLabel.text = "$"+String(menuItem.price)
        return cell
    }
    
    func tableView(_ tableView: UITableView, canEditRowAt indexPath: IndexPath) -> Bool {
        return true
    }
    
    func tableView(_ tableView: UITableView, commit editingStyle: UITableViewCellEditingStyle, forRowAt indexPath: IndexPath) {
        if (editingStyle == UITableViewCellEditingStyle.delete) {
            // delete data and row
            delete_request(name: menu[indexPath.row].name)
            menu.remove(at: indexPath.row)
            tableView.deleteRows(at: [indexPath], with: .fade)
        }
    }
    
    private func delete_request(name: String){
        let request = NSMutableURLRequest(url: URL(string: serverDomain+"/delete_menu_item")!)
        request.httpMethod = "POST"
        let payload = "itemname=\(name.lowercased())"
        request.httpBody = payload.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        
        let task = session.dataTask(with: request as URLRequest, completionHandler: {data, response, error -> Void in
            print("Response: \(response)")
            let strData = NSString(data: (data)!, encoding: String.Encoding.utf8.rawValue)!
            print("Body: \(strData)")
            
        })
        task.resume()
    }

    func loadAMenuItem (itemName: String, itemPrice: String, imageUrl: String){
        print("itemane is \(itemName) item price is \(itemPrice)")
        let url = URL(string: imageUrl)
        let data = try? Data(contentsOf: url!)
        let photo = UIImage(data: data!)
        menu += [MenuItem(name: itemName.capitalized, photo: photo, price: Double(itemPrice)!)!]
    }
    

    @IBAction func addMenu(_ sender: Any) {
        self.dismiss(animated: true, completion: nil)
        self.performSegue(withIdentifier: "add_menu", sender: nil)
        
    }
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
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
