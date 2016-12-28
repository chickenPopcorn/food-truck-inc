//
//  VendorOrderViewCell.swift
//  foodTruck
//
//  Created by Ruicong Xie on 12/22/16.
//  Copyright © 2016 ruicong xie. All rights reserved.
//

import UIKit

class VendorOrderViewCell: UITableViewCell {
    
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var priceLabel: UILabel!
    @IBOutlet weak var photoImageView: UIImageView!

    
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
