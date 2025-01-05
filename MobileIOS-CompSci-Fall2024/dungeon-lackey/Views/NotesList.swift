//
//  NotesList.swift
//  dungeon-lackey
//
//  Created by stud on 05/11/2024.
//

import SwiftUI
import SwiftData

struct Notes: View {
    @Query(sort: \Note.date, order: .reverse) private var notes: [Note]
    
    var body: some View {
        NavigationView {
            List(notes, id: \.id) { note in
                VStack(alignment: .leading){
                    Text(note.title)
                        .font(.headline)
                    
                    Text(note.date, style: .date)
                        .font(.subheadline)
                        .foregroundColor(.gray)
                    
                    Text(note.content)
                        .lineLimit(2)
                    
                    HStack {
                        ForEach(Array(note.tags), id: \.id) { tag in
                            Text("#\(tag.name)")
                                .font(.caption)
                                .padding(4)
                                .background(Color.blue.opacity(0.2))
                                .cornerRadius(4)
                        }
                    }
                }
                .padding(.vertical, 8)
            }
            .navigationTitle("Notes")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    NavigationLink(destination: AddNoteView()) {
                        Text("Add note")
                    }
                }
                    ToolbarItem(placement: .navigationBarLeading) {
                        Button("Back"){
                        }
                    }
                }
            }
        }
    }

#Preview {
    Notes()
}
