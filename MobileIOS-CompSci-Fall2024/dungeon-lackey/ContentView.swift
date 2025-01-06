import SwiftUI
import SwiftData

struct ContentView: View {
    @Environment(\.modelContext) private var modelContext
    @Query private var notes: [Note]

    var body: some View {
        NavigationView {
            List {
                ForEach(notes) { note in
                    NavigationLink(destination: NoteDetailsView(note: note)) {
                        Text(note.title)
                    }
                }
            }
            .navigationTitle("Notes")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Add Note") {
                        addSampleNote()
                    }
                }
            }
        }
    }

    private func addSampleNote() {
        let newNote = Note(title: "Sample Note", date: Date(), content: "This is a sample note.")
        modelContext.insert(newNote)
    }
}


#Preview {
    ContentView()
}
