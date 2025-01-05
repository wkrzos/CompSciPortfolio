//
//  dungeon_lackeyApp.swift
//  dungeon-lackey
//
//  Created by stud on 05/11/2024.
//

import SwiftUI
import SwiftData

@main
struct dungeon_lackeyApp: App {
    var sharedModelContainer: ModelContainer = {
        let schema = Schema([
            Note.self,
            Tag.self
        ])
        let modelConfiguration = ModelConfiguration(schema: schema, isStoredInMemoryOnly: false)

        do {
            return try ModelContainer(for: schema, configurations: [modelConfiguration])
        } catch {
            fatalError("Could not create ModelContainer: \(error)")
        }
    }()

    var body: some Scene {
        WindowGroup {
            NoteDetailsView()
        }
        .modelContainer(sharedModelContainer)
    }
}
