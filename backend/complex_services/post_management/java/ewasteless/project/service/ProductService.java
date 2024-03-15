package ewasteless.project.service;

// Spring imports
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

// Firebase import
import com.google.cloud.firestore.*;

// Java imports
import java.util.List;
import java.util.Optional;
import java.util.ArrayList;

// Model import
import ewasteless.project.classes.Product;

@Service
public class ProductService {

    @Autowired
    private Firestore dbFirestore;

    public Product getProductById(String PID) throws Exception {
        return dbFirestore.collection("products").document(PID).get().get().toObject(Product.class);
    }
}


