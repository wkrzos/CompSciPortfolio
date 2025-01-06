import SwiftUI

struct BottomNavigationBar: View {
    var body: some View {
        HStack {
            NavigationLink(destination: HomeView()) {
                VStack {
                    Image(systemName: "house")
                    Text("Home")
                        .font(.caption)
                }
                .frame(maxWidth: .infinity)
            }
            
            NavigationLink(destination: SearchView()) {
                VStack {
                    Image(systemName: "magnifyingglass")
                    Text("Search")
                        .font(.caption)
                }
                .frame(maxWidth: .infinity)
            }
            
            NavigationLink(destination: AddNoteView()) {
                VStack {
                    Image(systemName: "plus")
                    Text("Add Note")
                        .font(.caption)
                }
                .frame(maxWidth: .infinity)
            }
            
            NavigationLink(destination: OtherView()) {
                VStack {
                    Image(systemName: "list.bullet")
                    Text("Other")
                        .font(.caption)
                }
                .frame(maxWidth: .infinity)
            }
        }
        .padding()
        .background(Color(UIColor.systemGray6))
    }
}

#Preview {
    BottomNavigationBar()
}

