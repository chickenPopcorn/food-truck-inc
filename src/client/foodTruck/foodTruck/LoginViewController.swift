//
//  ViewController.swift
//  foodTruck
//
//  Created by ruicong xie on 11/10/16.
//  Copyright © 2016 ruicong xie. All rights reserved.
//

import UIKit

class LoginViewController: UIViewController {
    
    @IBOutlet weak var usernameText: UITextField!
    @IBOutlet weak var passwordText: UITextField!
    
    @IBAction func login(_ sender: UIButton) {
        let username = usernameText.text!
        let password = passwordText.text!
        if(username == "" || password == ""){
            //Create the AlertController
            let actionSheetController: UIAlertController = UIAlertController(title: "Alert", message: "Login failed", preferredStyle: .alert)
            
            //Create and add the Cancel action
            let cancelAction: UIAlertAction = UIAlertAction(title: "Cancel", style: .cancel) { action -> Void in
                //Do some stuff
            }
            actionSheetController.addAction(cancelAction)
            
            //Present the AlertController
            self.present(actionSheetController, animated: true, completion: nil)
            
        }else{
            
            let _url = URL(string: "http://127.0.0.1:5000/login/\(sender.currentTitle!)")
            
            var request = URLRequest(url: _url!)
            request.httpMethod = "POST"
            let payload = "username=\(username)&password=\(password)"
            request.httpBody = payload.data(using: String.Encoding.utf8)
            let session = URLSession.shared
            
            let task = session.dataTask(with: request, completionHandler: {data, response, error -> Void in
                print("Response: \(response)")
                let strData = NSString(data: (data)!, encoding: String.Encoding.utf8.rawValue)
                print("Body: \(strData)")
                
                if let httpResponse = response as? HTTPURLResponse {
                    if(httpResponse.statusCode == 200){
                        //sign in successfully
                        OperationQueue.main.addOperation {
                            let prefs:UserDefaults = UserDefaults.standard
                            prefs.set(username, forKey: "USERNAME")
                            prefs.set(true, forKey: "ISLOGGEDIN")
                            prefs.synchronize()
                            self.dismiss(animated: true, completion: nil)
                        }
                        
                    }else{
                        OperationQueue.main.addOperation{
                            //Create the AlertController
                            let actionSheetController: UIAlertController = UIAlertController(title: "Login failed", message: "Login failed. Please input valid username or password", preferredStyle: .alert)
                            //Create and add the Cancel action
                            let cancelAction: UIAlertAction = UIAlertAction(title: "OK", style: .cancel) { action -> Void in }
                            actionSheetController.addAction(cancelAction)
                            //Present the AlertController
                            self.present(actionSheetController, animated: true, completion: nil)
                        }
                    }
                } else {
                    assertionFailure("unexpected response")
                }
            })
            task.resume()
        }

    }


    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

