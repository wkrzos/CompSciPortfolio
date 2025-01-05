//
//  Tag.swift
//  dungeon-lackey
//
//  Created by stud on 05/11/2024.
//

import Foundation
import SwiftData

@Model
final class Tag {
    var id: UUID = UUID()
    var name: String
    var tagDescription: String
    var notes: [Note] = [] // Replace Set with Array for compatibility

    init(name: String, tagDescription: String) {
        self.name = name
        self.tagDescription = tagDescription
    }
}
