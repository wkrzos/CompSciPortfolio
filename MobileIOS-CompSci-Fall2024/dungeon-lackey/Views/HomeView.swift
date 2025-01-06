import SwiftUI

struct HomeView: View {
    var body: some View {
        NavigationView {
            VStack {
                // Existing NavigationLinks for notes
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
                
                // New Sample Campaign Button
                NavigationLink(destination: CampaignView(campaign: sampleCampaign)) {
                    Text("Sample Campaign")
                        .padding()
                        .foregroundColor(.white)
                        .background(Color.green)
                        .cornerRadius(8)
                }
            }
            .navigationTitle("Home")
        }
    }
    
    // Sample campaign for demonstration
    private var sampleCampaign: Campaign {
        let campaign = Campaign(
            title: "Sample Campaign",
            backgroundPicture: "castle_blueprint",
            nextSession: Date()
        )
        
        let sampleTags = [
            Tag(name: "Fantasy", tagDescription: "High fantasy setting"),
            Tag(name: "Adventure", tagDescription: "Quest-based campaign")
        ]
        
        // Add some sample tags and notes
        campaign.tags = sampleTags
        
        campaign.notes = [
            Note(title: "Intro Session", date: Date(), content: "Welcome to the campaign!"),
            Note(title: "The Lost Artifact", date: Date(), content: "Details about the lost artifact.")
        ]
        
//        campaign.notes.forEach { note in
//            note.tags = sampleTags
//        }
        
        return campaign
    }
}

#Preview {
    HomeView()
}
