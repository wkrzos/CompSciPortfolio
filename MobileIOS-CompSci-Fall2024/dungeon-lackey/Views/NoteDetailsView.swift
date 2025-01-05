import SwiftUI

struct NoteDetailsView: View {
    @State private var noteTitle: String = "Note 1"
    @State private var createdDate: String = "01.02.2013"
    @State private var tags: String = "Empty"
    @State private var sessionSummary: String = "\"The Shadow of Eldarath\" Lorem ipsum dolor sit amet, adventurers..."
    @State private var highlights: [String] = [
        "Ingressus est in mysterium Crypta Antiqua, quas praesidiis arcanis oppressae.",
        "Vestiges of Arcanis Sigilum were uncovered near the altar.",
        "Lorem (bard) charmed the Black Widow Queen for crucial information."
    ]
    @State private var npcsEncountered: [String] = [
        "Gravius the Obscure - Necromancer with a penchant for ancient riddles.",
        "Kaela the Wanderer - Merchant of cursed wares."
    ]
    @State private var lootAcquired: [String] = [
        "Enchanted blade, \"Gladius Ignis\" (+2 fire damage)."
    ]

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    // Metadata
                    HStack {
                        VStack(alignment: .leading) {
                            Text("Created")
                                .font(.caption)
                                .foregroundColor(.gray)
                            Text(createdDate)
                                .font(.body)
                        }
                        Spacer()
                        VStack(alignment: .leading) {
                            Text("Tags")
                                .font(.caption)
                                .foregroundColor(.gray)
                            Text(tags)
                                .font(.body)
                                .italic()
                        }
                    }

                    Divider()

                    // Session Summary
                    Text("Session Summary")
                        .font(.headline)
                    Text(sessionSummary)
                        .font(.body)

                    Divider()

                    // Highlights
                    Text("Highlights:")
                        .font(.headline)
                    VStack(alignment: .leading, spacing: 8) {
                        ForEach(highlights, id: \.self) { highlight in
                            HStack(alignment: .top) {
                                Text("•")
                                Text(highlight)
                            }
                        }
                    }

                    Divider()

                    // NPCs Encountered
                    Text("NPCs Encountered:")
                        .font(.headline)
                    VStack(alignment: .leading, spacing: 8) {
                        ForEach(npcsEncountered.indices, id: \.self) { index in
                            Text("\(index + 1). \(npcsEncountered[index])")
                        }
                    }

                    Divider()

                    // Loot Acquired
                    Text("Loot Acquired:")
                        .font(.headline)
                    VStack(alignment: .leading, spacing: 8) {
                        ForEach(lootAcquired, id: \.self) { loot in
                            HStack(alignment: .top) {
                                Text("•")
                                Text(loot)
                            }
                        }
                    }
                }
                .padding()
            }
            .navigationTitle(noteTitle)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Back") {
                        // Action for back navigation
                    }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    HStack {
                        Button(action: {
                            // Action for editing
                        }) {
                            Image(systemName: "pencil")
                        }
                        Button(action: {
                            // Action for deleting
                        }) {
                            Image(systemName: "trash")
                        }
                    }
                }
            }
        }
    }
}

#Preview {
    NoteDetailsView()
}

