package ewasteless.project.controllers;

// Spring imports
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

// Model imports 
import ewasteless.project.classes.Product;
import ewasteless.project.service.ProductService;

@RestController
@RequestMapping("/api/products")
public class ProductController {

    @Autowired
    private ProductService productService;

    @GetMapping("/{PID}")
    public ResponseEntity<Product> getProduct(@PathVariable String PID) {
        try {
            Product product = productService.getProductById(PID);
            return new ResponseEntity<>(product, HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(null, HttpStatus.NOT_FOUND);
        }
    }
}


