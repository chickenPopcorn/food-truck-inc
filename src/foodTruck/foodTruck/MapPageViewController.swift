//
//  MapPageViewController.swift
//  foodTruck
//
//  Created by ruicong xie on 12/7/16.
//  Copyright © 2016 ruicong xie. All rights reserved.
//

import UIKit
import GoogleMaps
import CoreLocation
import Alamofire
import SwiftyJSON

class MapPageViewController: UIViewController, GMSMapViewDelegate ,CLLocationManagerDelegate {

    var selectedVendor: String = ""
    var selectedVendorUsername: String = ""
    var locValue = CLLocationCoordinate2D()


    
    @IBOutlet weak var gmsMapView: GMSMapView!
    var locationManager = CLLocationManager()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        gmsMapView.delegate = self
        locationManager = CLLocationManager()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyKilometer
        locationManager.requestAlwaysAuthorization()
        locationManager.requestLocation()
        // Do any additional setup after loading the view.
        
//        let camera = GMSCameraPosition.camera(withLatitude: 40.8094912875224,  longitude: -73.9635899662971, zoom:14)
//        self.gmsMapView.camera = camera
//        self.gmsMapView.isMyLocationEnabled = true
//        self.gmsMapView.settings.myLocationButton = true
//        let marker = GMSMarker()
//        marker.position = CLLocationCoordinate2D(
//            latitude:Double(String(describing: 40.8094912875224))!,
//            longitude: Double(String(describing: -73.9635899662971))!)
//        marker.title = "testing"
//        marker.snippet = "testing"
//        marker.map = self.gmsMapView
        

        
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        print("Failed to find user's location: \(error.localizedDescription)")
    }
    
    override func viewWillAppear(_ animated: Bool) {
        
    }
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        if let location = locations.first {
            print("Found user's location: \(location)")
            googleMapSettings(loc: location.coordinate)
            let camera = GMSCameraPosition.camera(withLatitude: location.coordinate.latitude, longitude:location.coordinate.longitude, zoom:14)
            self.gmsMapView.camera = camera
            self.gmsMapView.isMyLocationEnabled = true
            self.gmsMapView.settings.myLocationButton = true
        }
    }
    
    private func googleMapSettings(loc:CLLocationCoordinate2D){
       
        Alamofire.request(serverDomain+"/search/geo/\(loc.latitude)/\(loc.longitude)")
            .responseJSON { response in
                // check for errors
                print("sending request")
                guard response.result.error == nil else {
                    // got an error in getting the data, need to handle it
                    print(response.result.error!)
                    return
                }
                // make sure we got some JSON since that's what we expect
                guard let json = response.result.value as? [String: Any] else {
                    print("Error: \(response.result.error)")
                    return
                }
                
                
                let j = JSON(json.first!.value)
                
                for (_, value) in j{
                    //generate some food trucks
                    let marker = GMSMarker()
                    marker.position = CLLocationCoordinate2D(
                        latitude:Double(String(describing: value["_source"]["geo"]["lat"]))!,
                        longitude: Double(String(describing: value["_source"]["geo"]["lon"]))!)
                    marker.title = value["_source"]["store_name"].stringValue
                    marker.snippet = value["_source"]["user_name"].stringValue
                    marker.map = self.gmsMapView
   
                }
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    private func didTapMyLocationButtonForMapView(mapView: GMSMapView) -> Bool {
        // reset marker:
        return false
        
    }
    
    func mapView(_ mapView: GMSMapView, didTapInfoWindowOf marker: GMSMarker) {
        self.selectedVendor = marker.title!
        self.selectedVendorUsername = marker.snippet!
        self.dismiss(animated: true, completion: nil)
        self.performSegue(withIdentifier: "go_to_menu", sender: self)
    }
    
//    func mapView(_ mapView: GMSMapView, didTapAt coordinate: CLLocationCoordinate2D) {
//        print("You tapped at \(coordinate.latitude), \(coordinate.longitude)")
//    }

    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if let vc = segue.destination as? MenuViewController{
            print("prepare for detail segue")
            vc.vendor = self.selectedVendor
            vc.vendorUsername = self.selectedVendorUsername
        }
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
