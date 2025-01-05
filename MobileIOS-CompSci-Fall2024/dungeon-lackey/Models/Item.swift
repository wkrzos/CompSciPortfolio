//
//  Item.swift
//  dungeon-lackey
//
//  Created by stud on 05/11/2024.
//

import Foundation
import SwiftData

@Model
final class Item {
    var timestamp: Date
    
    init(timestamp: Date) {
        self.timestamp = timestamp
    }
}
