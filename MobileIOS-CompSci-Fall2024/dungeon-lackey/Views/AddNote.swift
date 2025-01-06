//
//  AddNote.swift
//  dungeon-lackey
//
//  Created by stud on 05/11/2024.
//

import SwiftUI
import SwiftData

struct AddNote: View {
    @Environment(\.modelContext) private var context
    @Environment(\.dismiss) var dismiss
    
    @State private var title = ""
    @State private var date = Date()
    @State private var content = ""
    
    @Query(filter: #Predicate<Tag> { _ in true }) var allTags: [Tag]
    @State private var selectedTags: Set<Tag> = []
    @State private var searchQuery = ""

    var body: some View {
        Form {
            Section(header: Text("Note Details")) {
                TextField("Title", text: $title)
                DatePicker("Date", selection: $date, displayedComponents: .date)
                ZStack(alignment: .topLeading) {
                    if content.isEmpty {
                        Text("Enter your note content...")
                            .foregroundColor(.gray)
                            .padding(.top, 8)
                            .padding(.leading, 4)
                    }
                    TextEditor(text: $content)
                        .frame(height: 200)
                }
            }
            
            Section(header: Text("Tags")) {
                TextField("Search tags", text: $searchQuery)
                    .padding(.top)
                
                List(filteredTags, id: \.id) { tag in
                    Button(action: {
                        toggleTagSelection(tag)
                    }) {
                        HStack {
                            Text("#\(tag.name)")
                            Spacer()
                            if selectedTags.contains(tag) {
                                Image(systemName: "checkmark")
                                    .foregroundColor(.blue)
                            }
                        }
                        .contentShape(Rectangle())
                    }
                }
                .frame(height: 200)
                .listStyle(.plain)
            }
            
            Button("Save Note") {
                saveNote()
            }
            .disabled(title.isEmpty || content.isEmpty)
        }
        .padding()
        .navigationTitle("Add Note")
        .navigationBarTitleDisplayMode(.inline)
    }
    
    private var filteredTags: [Tag] {
        allTags.filter { searchQuery.isEmpty || $0.name.localizedCaseInsensitiveContains(searchQuery) }
    }
    
    private func toggleTagSelection(_ tag: Tag) {
        if selectedTags.contains(tag) {
            selectedTags.remove(tag)
        } else {
            selectedTags.insert(tag)
        }
    }
    
    private func saveNote() {
        let newNote = Note(title: title, date: date, content: content)
        newNote.tags = Array(selectedTags) // Convert Set to Array
        
        context.insert(newNote)
        
        do {
            try context.save()
            print("Note saved: \(newNote.title)")
            dismiss()
        } catch {
            print("Note save failed: \(error.localizedDescription)")
        }
    }
}
