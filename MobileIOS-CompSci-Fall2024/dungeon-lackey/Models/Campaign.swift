import Foundation
import SwiftData

@Model
final class Campaign {
    @Attribute(.unique) var id: UUID
    var title: String
    var backgroundPicture: String
    var nextSession: Date?
    @Relationship var tags: [Tag]
    @Relationship var notes: [Note]

    init(title: String, backgroundPicture: String, nextSession: Date? = nil) {
        self.id = UUID()
        self.title = title
        self.backgroundPicture = backgroundPicture
        self.nextSession = nextSession
        self.tags = []
        self.notes = []
    }
}
