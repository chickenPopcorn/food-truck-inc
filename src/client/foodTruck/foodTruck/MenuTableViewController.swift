//
//  MenuTableViewController.swift
//  foodTruck
//
//  Created by ruicong xie on 11/23/16.
//  Copyright © 2016 ruicong xie. All rights reserved.
//

import UIKit

class MenuTableViewController: UITableViewController {
    
    var menu = [MenuItem]()
    
    @IBAction func backToMap(_ sender: Any) {
        self.dismiss(animated: true, completion: nil)
        self.performSegue(withIdentifier: "gobackto_map", sender: nil)
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        print("viewDidLoad")
        loadSampleMenu()
        // Uncomment the following line to preserve selection between presentations
        // self.clearsSelectionOnViewWillAppear = false

        // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
        // self.navigationItem.rightBarButtonItem = self.editButtonItem()
    }
    
    func loadSampleMenu() {
        let photo1 = UIImage(named: "MenuItem1")!
        let item1 = MenuItem(name: "Caprese Salad", photo: photo1, price: 6.5)!
        
        let photo2 = UIImage(named: "MenuItem2")!
        let item2 = MenuItem(name: "Chicken and Potatoes", photo: photo2, price: 7.5)!
        
        let photo3 = UIImage(named: "MenuItem3")!
        let item3 = MenuItem(name: "Pasta with Meatballs", photo: photo3, price: 8.5)!
        
        menu += [item1, item2, item3]
    }
    
    @IBAction func order(_ sender: Any) {
        
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    // MARK: - Table view data source

    override func numberOfSections(in tableView: UITableView) -> Int {
        // #warning Incomplete implementation, return the number of sections
        return 1
    }

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // #warning Incomplete implementation, return the number of rows
        return menu.count
    }

    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {

        
        // Table view cells are reused and should be dequeued using a cell identifier.
        let cellIdentifier = "MenuTableViewCell"
        let cell = tableView.dequeueReusableCell(withIdentifier: cellIdentifier, for: indexPath) as! MenuTableViewCell
        
        // Fetches the appropriate meal for the data source layout.
        let menuItem = menu[indexPath.row]
        
        cell.nameLabel.text = menuItem.name
        cell.photoImageView.image = menuItem.photo
        cell.priceLabel.text = "$"+String(menuItem.price)
        
        return cell
    }
    

    /*
    // Override to support conditional editing of the table view.
    override func tableView(_ tableView: UITableView, canEditRowAt indexPath: IndexPath) -> Bool {
        // Return false if you do not want the specified item to be editable.
        return true
    }
    */

    /*
    // Override to support editing the table view.
    override func tableView(_ tableView: UITableView, commit editingStyle: UITableViewCellEditingStyle, forRowAt indexPath: IndexPath) {
        if editingStyle == .delete {
            // Delete the row from the data source
            tableView.deleteRows(at: [indexPath], with: .fade)
        } else if editingStyle == .insert {
            // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
        }    
    }
    */

    /*
    // Override to support rearranging the table view.
    override func tableView(_ tableView: UITableView, moveRowAt fromIndexPath: IndexPath, to: IndexPath) {

    }
    */

    /*
    // Override to support conditional rearranging of the table view.
    override func tableView(_ tableView: UITableView, canMoveRowAt indexPath: IndexPath) -> Bool {
        // Return false if you do not want the item to be re-orderable.
        return true
    }
    */

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
