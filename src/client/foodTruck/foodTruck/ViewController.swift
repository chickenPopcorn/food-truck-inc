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

class ViewController: UIViewController, GMSMapViewDelegate {
    
    @IBOutlet weak var gmsMapView: GMSMapView!
    
    
    override func loadView() {
        let camera = GMSCameraPosition.camera(withLatitude: 1.285,
                                                          longitude:103.848,
                                                          zoom:12)
        let mapView = GMSMapView.map(withFrame: .zero, camera: camera)
        mapView.isMyLocationEnabled = true
        mapView.settings.myLocationButton = true
        
        let marker = GMSMarker()
        marker.position = CLLocationCoordinate2D(latitude:1.28683043874784, longitude: 103.845024481416)
        marker.title = "Uncle Luoyang"
        marker.snippet = "Food Truck"
        marker.map = mapView
        
        mapView.delegate = self
        self.view = mapView
    }
    
    // MARK: GMSMapViewDelegate
    
    func mapView(_ mapView: GMSMapView, didTapAt coordinate: CLLocationCoordinate2D) {
        print("You tapped at \(coordinate.latitude), \(coordinate.longitude)")
    }
    

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    func mapView(_ mapView: GMSMapView, didTapInfoWindowOf marker: GMSMarker) {
        self.dismiss(animated: true, completion: nil)
        self.performSegue(withIdentifier: "goto_menu", sender: nil)
    }
    
    private func mapView(mapView: GMSMapView, didTapAtCoordinate coordinate: CLLocationCoordinate2D) {
        print("You tapped at \(coordinate.latitude), \(coordinate.longitude)")
    }
    
}

