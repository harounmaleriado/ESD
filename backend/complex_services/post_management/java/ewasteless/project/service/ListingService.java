package ewasteless.project.service;

// Spring imports
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

// Firebase imports
import com.google.cloud.firestore.CollectionReference;
import com.google.cloud.firestore.DocumentReference;
import com.google.cloud.firestore.DocumentSnapshot;
import com.google.cloud.firestore.Firestore;
import com.google.cloud.firestore.Query;    
import com.google.cloud.firestore.QuerySnapshot;

// ApiFuture import
import com.google.api.core.ApiFuture;

// Model imports
import ewasteless.project.classes.Listing;

// Java imports
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;

@Service
public class ListingService {

    @Autowired
    private Firestore dbFirestore;

    public String addListing(String username, 
                         String PID, 
                         double price, 
                         String productDescription, 
                         int postalCode,
                         String type,
                         String SID) 
                         throws ExecutionException, InterruptedException {
    
    // Get the product reference
    DocumentReference productRef = dbFirestore.collection(type).document(PID);
    

    // Create a Listing object
    Listing listing = new Listing(username, price, productDescription, postalCode, productRef, SID);
    
    // Decide the collection based on the type
    String collectionPath;
    switch (type) {
        case "CPU":
            collectionPath = "cpuListings";
            break;
        case "GPU":
            collectionPath = "gpuListings";
            break;
        case "RAM":
            collectionPath = "ramListings";
            break;
        case "HDD":
            collectionPath = "hddListings";
            break;
        case "SSD":
            collectionPath = "ssdListings";
            break;
        default:
            return "Error: Unknown type";
    }

    // Add the listing to the database
    ApiFuture<DocumentReference> future = dbFirestore.collection(collectionPath).add(listing);
    DocumentReference newListingRef = future.get();
    return newListingRef.getId();
}


    public Listing getListingById(String LID) throws Exception {
        return dbFirestore.collection("listings").document(LID).get().get().toObject(Listing.class);
    }

    public List<Listing> searchListings(String brand, String model, Double price, String sellerId) throws Exception {
        CollectionReference listings = dbFirestore.collection("listings");
        Query query = listings;
    
        if (brand != null) {
            query = query.whereEqualTo("brand", brand);
        }
        if (model != null) {
            query = query.whereEqualTo("model", model);
        }
        if (price != null) {
            query = query.whereLessThanOrEqualTo("price", price); 
        }
        if (sellerId != null) {
            query = query.whereEqualTo("sellerId", sellerId);
        }
    
        ApiFuture<QuerySnapshot> querySnapshot = query.get();
        
        List<Listing> results = new ArrayList<>();
        for (DocumentSnapshot doc : querySnapshot.get().getDocuments()) {
            results.add(doc.toObject(Listing.class));
        }
    
        return results;
    }

    public void deleteListing(String LID) throws ExecutionException, InterruptedException {
        // Attempt to delete the document from the 'listings' collection
        dbFirestore.collection("listings").document(LID).delete().get();
    }
}


