//
//  MenuTableViewCell.swift
//  foodTruck
//
//  Created by ruicong xie on 11/23/16.
//  Copyright © 2016 ruicong xie. All rights reserved.
//

import UIKit

class MenuTableViewCell: UITableViewCell {

    

        
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var priceLabel: UILabel!
    @IBOutlet weak var quantityLabel: UILabel!
    
    var quantity = 0
        
    @IBOutlet weak var photoImageView: UIImageView!
        
        
    @IBAction func addButton(_ sender: Any) {
        quantity += 1
    }
        
    @IBAction func deleteButtom(_ sender: Any) {
        if quantity > 0{
            quantity -= 1
        }
    }
        
        



    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
