//
//  AddNote.swift
//  dungeon-lackey
//
//  Created by stud on 05/11/2024.
//

import SwiftUI
import SwiftData

struct AddNoteView: View {
    @Environment(\.modelContext) private var context
    @Environment(\.dismiss) var dismiss
    
    @State private var title = ""
    @State private var date = Date()
    @State private var content = ""
    
    @Query var allTags: [Tag]
    @State private var selectedTags: Set<Tag> = []
    @State private var searchQuery = ""

    
    var body: some View {
        Form {
            TextField("Title", text:$title)
            DatePicker("Date", selection: $date, displayedComponents: .date)
            TextEditor(text: $content)
                .frame(height: 200)
            
            TextField("Search tags", text: $searchQuery)
                .padding(.top)
            List(filteredTags, id: \.id) { tag in
                Button(action: {
                    if selectedTags.contains(tag) {
                        selectedTags.remove(tag)
                    } else {
                        selectedTags.insert(tag)
                    }
                }) {
                    Text("#\(tag.name)")
                        .foregroundColor(selectedTags.contains(tag) ? .blue : .primary)
                }
            }
            .frame(height:200)
            .listStyle(.plain)
            
            Button("Save Note"){
                saveNote()
            }
            .disabled(title.isEmpty || content.isEmpty)
        }
        .padding()
    }
    
    private var filteredTags: [Tag] {
        allTags.filter { searchQuery.isEmpty || $0.name.localizedCaseInsensitiveContains(searchQuery)}
    }
    
    private func saveNote(){
        let newNote = Note(title: title, date: date, tags: selectedTags, content: content)
        
        print(newNote.title)
        
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
