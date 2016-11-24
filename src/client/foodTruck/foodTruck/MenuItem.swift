//
//  MenuItem.swift
//  foodTruck
//
//  Created by ruicong xie on 11/23/16.
//  Copyright © 2016 ruicong xie. All rights reserved.
//

import UIKit

class MenuItem {
    // MARK: Properties
    
    var name: String
    var photo: UIImage?
    var price: Double
    
    
    // MARK: Initialization
    
    init?(name: String, photo: UIImage?, price: Double) {
        // Initialize stored properties.
        self.name = name
        self.photo = photo
        self.price = price
        
        // Initialization should fail if there is no name or if the rating is negative.
        if name.isEmpty || price <= 0 {
            return nil
        }
    }
    
}
