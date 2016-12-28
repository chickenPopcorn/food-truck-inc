//
//  VendorTimeLocationViewController.swift
//  foodTruck
//
//  Created by Ruicong Xie on 12/17/16.
//  Copyright © 2016 ruicong xie. All rights reserved.
//

import UIKit
import GoogleMaps
import CoreLocation




class VendorTimeLocationViewController: UIViewController,GMSMapViewDelegate ,CLLocationManagerDelegate {
    
    let marker = GMSMarker()
    let storeName = "Testing"
    var locationManager = CLLocationManager()
    var coord = CLLocationCoordinate2D()
    
    
    
    
    @IBAction func goToMenu(_ sender: Any) {
        self.dismiss(animated: true, completion: nil)
        self.performSegue(withIdentifier: "go_to_menu", sender: nil)
    }

    @IBOutlet weak var startTime: UIDatePicker!
    @IBOutlet weak var endTime: UIDatePicker!

    @IBOutlet weak var gmsMapView: GMSMapView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        googleMapSettings()
        gmsMapView.delegate = self
        locationManager = CLLocationManager()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBest
        locationManager.requestAlwaysAuthorization()
        locationManager.startUpdatingLocation()
    }
    
    private func googleMapSettings(){
        marker.title = self.storeName
        let camera = GMSCameraPosition.camera(withLatitude: 40.809456, longitude:-73.962764, zoom:16)
        self.gmsMapView.camera = camera
        gmsMapView.isMyLocationEnabled = true
        gmsMapView.settings.myLocationButton = true
        
    }

    private func didTapMyLocationButtonForMapView(mapView: GMSMapView) -> Bool {
        // reset marker:
        return false
    }
    
    
    func mapView(_ mapView: GMSMapView, didTapAt coordinate: CLLocationCoordinate2D) {
        print("You tapped at \(coordinate.latitude), \(coordinate.longitude)")
        marker.position = CLLocationCoordinate2D(
                    latitude:Double(String(describing: coordinate.latitude))!,
                    longitude: Double(String(describing: coordinate.longitude))!)
        coord.latitude = coordinate.latitude
        coord.longitude = coordinate.longitude
        marker.snippet = "Food Truck"
        marker.map = self.gmsMapView
    }
    
    @IBAction func updateLocationAndTime(_ sender: Any) {
        
        let _url = URL(string: serverDomain+"/add_new")
        
        print("this is working")
        
        var request = URLRequest(url: _url!)
        request.httpMethod = "POST"
        print(startTime.date)
        print(endTime.date)
        let payload = "lat=\(coord.latitude)&lon=\(coord.longitude)&start_time=\(startTime.date)&close_time=\(endTime.date)"
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
                    let alert = UIAlertController(title: "Shop Status", message: "It's now open", preferredStyle: UIAlertControllerStyle.alert)
                    alert.addAction(UIAlertAction(title: "Ok, let's make some money!", style: UIAlertActionStyle.default, handler: nil))
                    self.present(alert, animated: true, completion: nil)
                }
            }
        })
        dataTask.resume()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        startTime.datePickerMode = .time
        endTime.datePickerMode = .time
        
        
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
