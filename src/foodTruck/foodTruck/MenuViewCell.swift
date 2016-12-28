//
//  MenuViewCell.swift
//  foodTruck
//
//  Created by ruicong xie on 12/7/16.
//  Copyright © 2016 ruicong xie. All rights reserved.
//

import UIKit

class MenuViewCell: UITableViewCell {
    
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var priceLabel: UILabel!
    @IBOutlet weak var quantityLabel: UILabel!
    
    var quantity = 0
    
    @IBOutlet weak var photoImageView: UIImageView!
    
    @IBAction func addButton(_ sender: Any) {
        quantity+=1
        quantityLabel.text = displayQuantity(order: quantity)
    }
    
    @IBAction func deleteButtom(_ sender: Any) {
        if quantity > 0{
            quantity-=1
            quantityLabel.text = displayQuantity(order: quantity)
        }
    }
    
    func displayQuantity(order: Int) -> String{
        return "Order: "+String(order)
    }
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
        quantityLabel.text = displayQuantity(order: quantity)
    }
    
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
        // Configure the view for the selected state
    }
}

