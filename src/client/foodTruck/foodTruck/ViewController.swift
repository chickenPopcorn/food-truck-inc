//
//  ViewController.swift
//  foodTruck
//
//  Created by ruicong xie on 11/10/16.
//  Copyright © 2016 ruicong xie. All rights reserved.
//


import UIKit
import GoogleMaps

var serverDomain = "http://localhost:5000"

class ViewController: UIViewController{
    
    @IBOutlet weak var gmsMapView: GMSMapView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        // Create a GMSCameraPosition that tells the map to display the
        // coordinate -33.86,151.20 at zoom level 6.
        let camera = GMSCameraPosition.camera(withLatitude: 40.809986, longitude: -73.962635, zoom: 17.0)
        let mapView = GMSMapView.map(withFrame: CGRect.zero, camera: camera)
        mapView.isMyLocationEnabled = true
        view = mapView
        
        // Creates a marker in the center of the map.
        let marker = GMSMarker()
        marker.position = CLLocationCoordinate2D(latitude:40.809986, longitude: -73.962635)
        marker.title = "Uncle Luoyang"
        marker.snippet = "Food Truck"
        marker.map = mapView
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
}

