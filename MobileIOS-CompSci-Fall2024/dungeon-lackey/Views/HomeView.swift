import SwiftUI

struct HomeView: View {
    var body: some View {
        NavigationView {
            VStack {
                NavigationLink(destination: NoteDetailsView(note: Note(title: "Sample Note", date: Date(), content: "This is a sample note."))) {
                    Text("el buton")
                        .padding()
                        .foregroundColor(.white)
                        .background(Color.blue)
                        .cornerRadius(8)
                }
                NavigationLink(destination: NoteDetailsView(note: Note(title: "Sample Note 2", date: Date(), content: "This is a sample note. 2"))) {
                    Text("el buton")
                        .padding()
                        .foregroundColor(.white)
                        .background(Color.blue)
                        .cornerRadius(8)
                }
                
            }
            .navigationTitle("Home")
        }
    }
}

#Preview {
    HomeView()
}
