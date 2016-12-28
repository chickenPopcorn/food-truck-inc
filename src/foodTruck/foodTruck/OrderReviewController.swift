//
//  OrderReviewController.swift
//  foodTruck
//
//  Created by houlianglv on 12/8/16.
//  Copyright © 2016 ruicong xie. All rights reserved.
//

import UIKit
import BraintreeDropIn
import Braintree

class OrderReviewController: UIViewController, UINavigationControllerDelegate,UITableViewDelegate, UITableViewDataSource {
    
    var orderReview = [OrderItem]()
    var total: Double = 0.0
    var vendorUsername = ""
    
    @IBOutlet weak var orderTable: UITableView!
    let cellReuseIdentifier = "orderReviewCell"
    
    @IBOutlet weak var totalAmount: UILabel!
    let clientToken = "eyJ2ZXJzaW9uIjoyLCJhdXRob3JpemF0aW9uRmluZ2VycHJpbnQiOiJmMmQxNzFmOGIwOWQyNGYxZGE5YzMwN2YzY2E2NjlmY2JlNTE1ZDIxZmI3YzQ1ZDViMTRhMGExNGE2Y2I0YTYwfGNyZWF0ZWRfYXQ9MjAxNi0xMi0xN1QwNzoyMTo0Mi4zNzIzNDg5ODYrMDAwMFx1MDAyNm1lcmNoYW50X2lkPTM0OHBrOWNnZjNiZ3l3MmJcdTAwMjZwdWJsaWNfa2V5PTJuMjQ3ZHY4OWJxOXZtcHIiLCJjb25maWdVcmwiOiJodHRwczovL2FwaS5zYW5kYm94LmJyYWludHJlZWdhdGV3YXkuY29tOjQ0My9tZXJjaGFudHMvMzQ4cGs5Y2dmM2JneXcyYi9jbGllbnRfYXBpL3YxL2NvbmZpZ3VyYXRpb24iLCJjaGFsbGVuZ2VzIjpbXSwiZW52aXJvbm1lbnQiOiJzYW5kYm94IiwiY2xpZW50QXBpVXJsIjoiaHR0cHM6Ly9hcGkuc2FuZGJveC5icmFpbnRyZWVnYXRld2F5LmNvbTo0NDMvbWVyY2hhbnRzLzM0OHBrOWNnZjNiZ3l3MmIvY2xpZW50X2FwaSIsImFzc2V0c1VybCI6Imh0dHBzOi8vYXNzZXRzLmJyYWludHJlZWdhdGV3YXkuY29tIiwiYXV0aFVybCI6Imh0dHBzOi8vYXV0aC52ZW5tby5zYW5kYm94LmJyYWludHJlZWdhdGV3YXkuY29tIiwiYW5hbHl0aWNzIjp7InVybCI6Imh0dHBzOi8vY2xpZW50LWFuYWx5dGljcy5zYW5kYm94LmJyYWludHJlZWdhdGV3YXkuY29tLzM0OHBrOWNnZjNiZ3l3MmIifSwidGhyZWVEU2VjdXJlRW5hYmxlZCI6dHJ1ZSwicGF5cGFsRW5hYmxlZCI6dHJ1ZSwicGF5cGFsIjp7ImRpc3BsYXlOYW1lIjoiQWNtZSBXaWRnZXRzLCBMdGQuIChTYW5kYm94KSIsImNsaWVudElkIjpudWxsLCJwcml2YWN5VXJsIjoiaHR0cDovL2V4YW1wbGUuY29tL3BwIiwidXNlckFncmVlbWVudFVybCI6Imh0dHA6Ly9leGFtcGxlLmNvbS90b3MiLCJiYXNlVXJsIjoiaHR0cHM6Ly9hc3NldHMuYnJhaW50cmVlZ2F0ZXdheS5jb20iLCJhc3NldHNVcmwiOiJodHRwczovL2NoZWNrb3V0LnBheXBhbC5jb20iLCJkaXJlY3RCYXNlVXJsIjpudWxsLCJhbGxvd0h0dHAiOnRydWUsImVudmlyb25tZW50Tm9OZXR3b3JrIjp0cnVlLCJlbnZpcm9ubWVudCI6Im9mZmxpbmUiLCJ1bnZldHRlZE1lcmNoYW50IjpmYWxzZSwiYnJhaW50cmVlQ2xpZW50SWQiOiJtYXN0ZXJjbGllbnQzIiwiYmlsbGluZ0FncmVlbWVudHNFbmFibGVkIjp0cnVlLCJtZXJjaGFudEFjY291bnRJZCI6ImFjbWV3aWRnZXRzbHRkc2FuZGJveCIsImN1cnJlbmN5SXNvQ29kZSI6IlVTRCJ9LCJjb2luYmFzZUVuYWJsZWQiOmZhbHNlLCJtZXJjaGFudElkIjoiMzQ4cGs5Y2dmM2JneXcyYiIsInZlbm1vIjoib2ZmIn0="


    func showDropIn(clientTokenOrTokenizationKey: String) {
        let request =  BTDropInRequest()
        let dropIn = BTDropInController(authorization: clientTokenOrTokenizationKey, request: request)
        { (controller, result, error) in
            if (error != nil) {
                print("ERROR")
            } else if (result?.isCancelled == true) {
                print("CANCELLED")
            } else if result != nil {
                // Use the BTDropInResult properties to update your UI
                // result.paymentOptionType
                // result.paymentMethod
                // result.paymentIcon
                // result.paymentDescription
            }
            controller.dismiss(animated: true, completion: nil)
        }
        self.present(dropIn!, animated: true, completion: nil)
    }
   
    
    override func viewDidLoad() {
        super.viewDidLoad()
        showDropIn(clientTokenOrTokenizationKey: clientToken)
        print("menu list is ")
        print(self.orderReview.count)
        self.orderTable.delegate = self
        self.orderTable.dataSource = self
        
        for i in (0..<orderReview.count) {
            total+=orderReview[i].price * Double(orderReview[i].quantity)
        }
        self.totalAmount.text = "Total Amount: $"+String(total)
        
        
//        let tokenizationKey = "sandbox_5w3ybbkv_2yffqc6bmkqftb94"
//        let apiClient = BTAPIClient(authorization: tokenizationKey)

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    private func submitAOrder(itemnam: String, quantity: String, price: String) {
        let _url = URL(string: serverDomain+"/submit_order")

        var request = URLRequest(url: _url!)
        request.httpMethod = "POST"
        let payload: String = "vendor=\(self.vendorUsername)&itemname=\(itemnam.lowercased())&quantity=\(quantity)&price=\(price)"
        
        print(payload)
        request.httpBody = payload.data(using: String.Encoding.utf8)

        
        let session = URLSession.shared
        let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
            if (error != nil) {
                print(error!)
            } else {
                let httpResponse = response as? HTTPURLResponse
                print(httpResponse!)
                if httpResponse?.statusCode == 200{
                    print("sent one")
                    print(response!)
                }
            }
        })
        
        dataTask.resume()
    }


    @IBAction func onPaymentTapped(_ sender: UIButton) {
        for (_, value) in orderReview.enumerated(){
            submitAOrder(itemnam: value.name, quantity: String(value.quantity), price: String(value.price))
        }
        let alert = UIAlertController(title: "Order Received", message: "We will SMS you when it's ready!", preferredStyle: UIAlertControllerStyle.alert)
        alert.addAction(UIAlertAction(title: "OK", style: UIAlertActionStyle.default, handler: nil))
        self.present(alert, animated: true, completion: nil)
        
        

//        self.counterLabel.text = "Payment Success!"
//        timer = Timer(timeInterval: 5.0, target: self, selector: #selector(OrderReviewController.orderReceived), userInfo: nil, repeats: false)
//
//        RunLoop.current.add(timer, forMode: RunLoopMode.commonModes)
//
//        timer = Timer(timeInterval: 10.0, target: self, selector: #selector(OrderReviewController.orderProcessing), userInfo: nil, repeats: false)
//
//        RunLoop.current.add(timer, forMode: RunLoopMode.commonModes)
//
//
//
//        timer = Timer(timeInterval: 20.0, target: self, selector: #selector(OrderReviewController.orderReady), userInfo: nil, repeats: false)
//
//        RunLoop.current.add(timer, forMode: RunLoopMode.commonModes)

    }

//    func orderReceived(timer: Timer) {
//        self.counterLabel.text = "Your Order Confirmed!"
//    }
//
//    func orderProcessing(timer: Timer) {
//        self.counterLabel.text = "Vendor is processing your order..."
//    }
//
//    func orderReady(timer: Timer) {
//        self.counterLabel.text = "Order is ready for pick-up!"
//        //Create the AlertController
//        let actionSheetController: UIAlertController = UIAlertController(title: "Breaking News", message: "Your Order is Ready for Pick up!", preferredStyle: .alert)
//
//        //Create and add the Cancel action
//        let cancelAction: UIAlertAction = UIAlertAction(title: "OK", style: .cancel) { action -> Void in
//            //Do some stuff
//        }
//        actionSheetController.addAction(cancelAction)
//
//        //Present the AlertController
//        self.present(actionSheetController, animated: true, completion: nil)
//    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return orderReview.count
    }
    
    private func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        // Table view cells are reused and should be dequeued using a cell identifier.
        let cell:OrderViewCell = tableView.dequeueReusableCell( withIdentifier: cellReuseIdentifier) as! OrderViewCell
        
        // Fetches the appropriate meal for the data source layout.
        let orderItem = orderReview[indexPath.row]
        self.total += Double(orderItem.quantity)*orderItem.price
        cell.nameLabel.text = orderItem.name
        cell.photoImageView.image = orderItem.photo
        cell.priceLabel.text = "Price: $"+String(orderItem.price)
        cell.quantityLabel.text = "Order: "+String(orderItem.quantity)
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
