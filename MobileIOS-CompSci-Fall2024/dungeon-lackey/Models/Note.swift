//
//  Note.swift
//  dungeon-lackey
//
//  Created by stud on 05/11/2024.
//

import Foundation
import SwiftData

@Model
final class Note {
    var id: UUID = UUID()
    
    var title: String
    var date: Date
    var tags: Set<Tag>
    var content: String
    
    init(title: String, date: Date, tags: Set<Tag>, content: String) {
        self.title = title
        self.date = date
        self.tags = tags
        self.content = content
    }
}

 
