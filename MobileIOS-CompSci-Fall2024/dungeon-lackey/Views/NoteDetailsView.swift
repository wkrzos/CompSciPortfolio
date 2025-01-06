    import SwiftUI

    struct NoteDetailsView: View {
        @Environment(\.dismiss) private var dismiss
        @State private var noteTitle: String = "Note 1"
        @State private var createdDate: String = "01.02.2013"
        @State private var tags: [Tag] = [Tag(name: "Tag1", tagDescription: "Tag1"), Tag(name: "Tag2", tagDescription: "Tag2"), Tag(name: "Tag3", tagDescription: "Tag3")]
        @State private var noteContent: String = ""
        @State private var isEditing: Bool = false

        var body: some View {
            NavigationView {
                VStack {
                    // Header Section
                    VStack(alignment: .leading, spacing: 8) {
                        TextField("Note Title", text: $noteTitle)
                            .font(.largeTitle)
                            .fontWeight(.bold)
                            .padding(.top, 8)

                        VStack(alignment: .leading, spacing: 8) {
                            HStack(alignment: .top) {
                                Image(systemName: "clock")
                                    .foregroundColor(.gray)
                                Text("Created")
                                    .font(.caption)
                                    .foregroundColor(.gray)
                                    .frame(width: 70, alignment: .leading)
                                Text(createdDate)
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
                                Text(tags.map { $0.name }.joined(separator: ", "))
                                    .font(.caption)
                                    .foregroundColor(.blue)
                            }
                        }
                        Divider()
                    }
                    .padding(.horizontal)

                    // Content Section
                    ZStack(alignment: .topLeading) {
                        if noteContent.isEmpty {
                            Text("Write your note here...")
                                .foregroundColor(.gray)
                                .padding(8)
                                .frame(maxWidth: .infinity, alignment: .leading)
                        }
                        TextEditor(text: $noteContent)
                            .frame(maxWidth: .infinity, maxHeight: .infinity)
                            .padding(4)
                    }
                    .padding(.horizontal)

                    Spacer()
                }
                .navigationTitle("Note Details")
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
                        Button(action: {
                            // Delete logic here
                        }) {
                            Image(systemName: "trash")
                        }
                    }
                }
            }
        }
    }

    #Preview {
        NoteDetailsView()
    }
