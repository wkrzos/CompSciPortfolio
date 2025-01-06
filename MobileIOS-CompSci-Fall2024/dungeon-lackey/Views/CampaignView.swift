import SwiftUI
import SwiftData

struct CampaignView: View {
    @Environment(\.dismiss) private var dismiss
    @Environment(\.modelContext) private var modelContext // SwiftData context
    @Bindable var campaign: Campaign // Campaign model instance

    @State private var searchText: String = "" // For search functionality

    var body: some View {
        NavigationView {
            VStack {
                // Campaign Image
                Image("castle_blueprint") // Replace with dynamic or default image
                    .resizable()
                    .scaledToFit()
                    .frame(height: 200)
                    .clipped()
                    .overlay(
                        Button(action: {
                            // Logic for changing the image
                        }) {
                            Image(systemName: "pencil")
                                .padding()
                                .background(Color.white.opacity(0.8))
                                .clipShape(Circle())
                                .shadow(radius: 2)
                        }
                        .padding(),
                        alignment: .bottomTrailing
                    )

                // Header Section
                VStack(alignment: .leading, spacing: 8) {
                    TextField("Campaign Title", text: $campaign.title)
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .padding(.top, 8)

                    VStack(alignment: .leading, spacing: 8) {
                        HStack(alignment: .top) {
                            Image(systemName: "clock")
                                .foregroundColor(.gray)
                            Text("Session")
                                .font(.caption)
                                .foregroundColor(.gray)
                                .frame(width: 70, alignment: .leading)
                            Text(campaign.nextSession!, style: .date)
                                .font(.caption)
                                .foregroundColor(.gray)
                        }

                        HStack(alignment: .top) {
                            Image(systemName: "tag")
                                .foregroundColor(.gray)
                            Text("Tags")
                                .font(.caption)
                                .foregroundColor(.gray)
                                .frame(width: 70, alignment: .leading)
//                            Text(campaign.tags.joined(separator: ", "))
//                                .font(.caption)
//                                .foregroundColor(.blue)
                            Text(campaign.tags.map { $0.name }.joined(separator: ", "))
                                .font(.caption)
                                .foregroundColor(.blue)
                        }
                    }
                    Divider()
                }
                .padding(.horizontal)

                // Search and Add Button
                HStack {
                    TextField("Search", text: $searchText)
                        .padding(8)
                        .background(Color(.systemGray6))
                        .cornerRadius(8)

                    Button(action: addNote) {
                        Image(systemName: "plus")
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .clipShape(Circle())
                    }
                }
                .padding(.horizontal)

                // Notes List
                List(filteredNotes) { note in
                    NavigationLink(destination: NoteDetailsView(note: note)) {
                        Text(note.title)
                            .font(.body)
                    }
                }
                .listStyle(.plain)
                .padding(.horizontal)

                Spacer()
            }
            .navigationTitle("New Campaign")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button(action: {
                        dismiss()
                    }) {
                        HStack {
                            Image(systemName: "arrow.left")
                            Text("Back")
                        }
                    }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: deleteCampaign) {
                        Image(systemName: "trash")
                    }
                }
            }
        }
    }

    // Computed property for filtering notes based on search text
    private var filteredNotes: [Note] {
        if searchText.isEmpty {
            return campaign.notes
        } else {
            return campaign.notes.filter { $0.title.localizedCaseInsensitiveContains(searchText) }
        }
    }

    // Logic to add a new note
    private func addNote() {
        let newNote = Note(title: "New Note", date: Date(), content: "")
        campaign.notes.append(newNote)
        modelContext.insert(newNote)
    }

    // Logic to delete the campaign
    private func deleteCampaign() {
        modelContext.delete(campaign)
        dismiss()
    }
}
