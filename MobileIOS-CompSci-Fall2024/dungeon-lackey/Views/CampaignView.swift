import SwiftUI
import SwiftData

struct CampaignView: View {
    @Environment(\.dismiss) private var dismiss
    @Environment(\.modelContext) private var modelContext // SwiftData context
    @Bindable var campaign: Campaign // Campaign model instance

    @State private var searchText: String = "" // For search functionality
    @State private var isDatePickerPresented: Bool = false // Controls the date picker modal

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

                            Text(campaign.nextSession.map { DateFormatter.localizedString(from: $0, dateStyle: .medium, timeStyle: .none) } ?? "Select a date")
                                .font(.caption)
                                .foregroundColor(.blue)
                                .onTapGesture {
                                    isDatePickerPresented = true
                                }
                        }

                        HStack(alignment: .top) {
                            Image(systemName: "tag")
                                .foregroundColor(.gray)
                            Text("Tags")
                                .font(.caption)
                                .foregroundColor(.gray)
                                .frame(width: 70, alignment: .leading)
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

                // Notes List or Placeholder
                if filteredNotes.isEmpty {
                    // Display the placeholder text
                    VStack {
                        Text("The library shelves are empty, and no pages can be found. Why not start a new chapter? Add your first note and let your adventure begin!")
                            .font(.body)
                            .foregroundColor(.gray)
                            .italic()
                            .multilineTextAlignment(.center)
                            .padding()
                        Spacer()
                    }
                } else {
                    // Display the list of notes
                    List(filteredNotes) { note in
                        NavigationLink(destination: NoteDetailsView(note: note)) {
                            Text(note.title)
                                .font(.body)
                            Text(note.tags.map { $0.name }.joined(separator: ", "))
                                .font(.caption)
                                .foregroundColor(.blue)
                        }
                    }
                    .listStyle(.plain)
                    .padding(.horizontal)
                }

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
            .sheet(isPresented: $isDatePickerPresented) {
                // DatePicker modal
                VStack {
                    DatePicker("Select Session Date", selection: Binding(
                        get: { campaign.nextSession ?? Date() },
                        set: { campaign.nextSession = $0 }
                    ), displayedComponents: .date)
                        .datePickerStyle(.graphical)
                        .padding()

                    Button("Done") {
                        isDatePickerPresented = false
                    }
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(8)
                }
                .presentationDetents([.medium])
                .padding()
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
