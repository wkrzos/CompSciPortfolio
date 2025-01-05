//
//  Tag.swift
//  dungeon-lackey
//
//  Created by stud on 05/11/2024.
//

import Foundation
import SwiftData

@Model
class Tag: Codable, Hashable {
    var id: UUID = UUID()
    var name: String
    var tagDescription: String
    
    init(name: String, tagDescription: String) {
        self.name = name
        self.tagDescription = tagDescription
    }
    
    required init(from decoder: any Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        id = try container.decode(UUID.self, forKey: .id)
        name = try container.decode(String.self, forKey: .name)
        tagDescription = try container.decode(String.self, forKey: .tagDescription)
    }
    
    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(id, forKey: .id)
        try container.encode(name, forKey: .name)
        try container.encode(tagDescription, forKey: .tagDescription)
    }
    
    private enum CodingKeys: String, CodingKey {
        case id, name, tagDescription
    }
    
    static func == (lhs: Tag, rhs: Tag) -> Bool {
        return lhs.id == rhs.id
    }
    
    func hash(into hasher: inout Hasher){
        hasher.combine(id)
    }
}
