//
//  MainPageViewController.swift
//  foodTruck
//
//  Created by ruicong xie on 11/21/16.
//  Copyright © 2016 ruicong xie. All rights reserved.
//


import UIKit

class SignUpViewController: UIViewController {
    
    @IBOutlet weak var usernameText: UITextField!
    @IBOutlet weak var firstNameText: UITextField!
    @IBOutlet weak var lastNameText: UITextField!
    @IBOutlet weak var emailText: UITextField!
    @IBOutlet weak var passwordText: UITextField!
    @IBOutlet weak var confirmPwdText: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Do any additional setup after loading the view.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func signupTapped(sender: UIButton) {
        //sign up
        if(passwordText.text != confirmPwdText.text){
            //Create the AlertController
            let actionSheetController: UIAlertController = UIAlertController(title: "Alert", message: "confirmation password doesn't match the password", preferredStyle: .alert)
            
            //Create and add the Cancel action
            let cancelAction: UIAlertAction = UIAlertAction(title: "Cancel", style: .cancel) { action -> Void in
                //Do some stuff
            }
            actionSheetController.addAction(cancelAction)
            
            //Present the AlertController
            self.present(actionSheetController, animated: true, completion: nil)
            return
        }
        
        let username = usernameText.text!
        let password = passwordText.text!
        let confirm = confirmPwdText.text!
        let email = emailText.text!
        let firstName = firstNameText.text!
        let lastName = lastNameText.text!
        let _url = URL(string: "http://127.0.0.1:5000/register/\(sender.currentTitle!)")
        var request = URLRequest(url: _url!)
        request.httpMethod = "POST"
    
        let payload = "username=\(username)&password=\(password)&confirm=\(confirm)&email=\(email)&firstname=\(firstName)&lastname=\(lastName)"
        request.httpBody = payload.data(using: String.Encoding.utf8)
       let session = URLSession.shared
        
        let task = session.dataTask(with: request, completionHandler: {data, response, error -> Void in
            print("Response: \(response)")
            let strData = NSString(data: (data)!, encoding: String.Encoding.utf8.rawValue)
            print("Body: \(strData)")
            
            if let httpResponse = response as? HTTPURLResponse {
                if(httpResponse.statusCode == 200){
                    OperationQueue.main.addOperation {
                        //Create the AlertController
                        let actionSheetController: UIAlertController = UIAlertController(title: "Success", message: "You have registered successfully", preferredStyle: .alert)
                        //Create and add the Cancel action
                        let cancelAction: UIAlertAction = UIAlertAction(title: "OK", style: .cancel) { action -> Void in
                            self.dismiss(animated: true, completion: nil)
                        }
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
    
    @IBAction func gotoSignIn(sender: AnyObject) {
        self.dismiss(animated: true, completion: nil)
    }
    
}
