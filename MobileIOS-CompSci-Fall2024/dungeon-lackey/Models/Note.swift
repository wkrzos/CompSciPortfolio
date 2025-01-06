import Foundation
import SwiftData

@Model
final class Note {
    var id: UUID = UUID()
    var title: String
    var date: Date
    var content: String
    var tags: [Tag] = [] // Replace Set with Array for compatibility

    init(title: String, date: Date, content: String) {
        self.title = title
        self.date = date
        self.content = content
    }
}
