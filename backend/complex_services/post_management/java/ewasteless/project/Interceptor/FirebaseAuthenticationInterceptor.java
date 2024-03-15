package ewasteless.project.Interceptor;

import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseAuthException;
import com.google.firebase.auth.FirebaseToken;

import ewasteless.project.ExceptionHandling.UnauthorizedException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;



@Component
public class FirebaseAuthenticationInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String token = request.getHeader("Authorization");
        if (token == null || !token.startsWith("Bearer ")) {
            throw new UnauthorizedException("Invalid token");
        }
        token = token.replace("Bearer ", "");
        try {
            FirebaseToken decodedToken = FirebaseAuth.getInstance().verifyIdToken(token);
            // Optionally, you can store the decoded token in the request attributes for the controllers to use
            request.setAttribute("uid", decodedToken.getUid());
            
            return true;
        } catch (FirebaseAuthException ex) {
            throw new UnauthorizedException("Token verification failed", ex);
        }
    }
}

