import Foundation
import SwiftData

@Model
final class Note {
    var id: UUID = UUID()
    var title: String
    var date: Date
    var content: String
    @Relationship var tags: [Tag]

    init(title: String, date: Date, content: String) {
        self.title = title
        self.date = date
        self.content = content
        self.tags = []
    }
}
