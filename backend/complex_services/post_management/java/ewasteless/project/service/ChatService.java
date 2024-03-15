package ewasteless.project.service;

import com.google.cloud.firestore.Firestore;
import com.google.api.core.ApiFuture;
import com.google.cloud.firestore.DocumentReference;
import com.google.cloud.firestore.DocumentSnapshot;
import com.google.cloud.firestore.WriteResult;

import ewasteless.project.DTO.ChatDTO;
import ewasteless.project.classes.Chat;
import ewasteless.project.classes.Comment;
import ewasteless.project.classes.User;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.concurrent.ExecutionException;

@Service
public class ChatService {

    private final Firestore firestore;

    @Autowired
    public ChatService(Firestore firestore) {
        this.firestore = firestore;
    }

    public String createChat(ChatDTO chatDTO) throws ExecutionException, InterruptedException {
        // Reference to the new chat document with a generated ID
        DocumentReference newChatRef = firestore.collection("chats").document();
    
        // Create the Chat object using the DTO
        Chat chat = new Chat();
        chat.setCID(newChatRef.getId()); // Set the generated document ID as the CID
        chat.setBID(chatDTO.getBID());
        chat.setSID(chatDTO.getSID());
        chat.setBrand(chatDTO.getBrand());
        chat.setModel(chatDTO.getModel());

        // Save the chat object to Firestore
        ApiFuture<WriteResult> futureChat = newChatRef.set(chat);
        // Wait for the operation to complete and retrieve the write result
        WriteResult writeResult = futureChat.get();

        // Return the created chat document ID or other relevant information
        return newChatRef.getId();
    }

    

    public String addCommentToChat(String CID, Comment comment) throws Exception {
        
        
        comment.setCreatedTimestamp(Instant.now());
        DocumentReference postRef = firestore.collection("posts").document(CID);
        ApiFuture<WriteResult> writeResult = postRef.collection("comments").document().create(comment);
        
        DocumentReference userRef = firestore.collection("users").document(comment.getUID());
        ApiFuture<DocumentSnapshot> futureUserSnapshot = userRef.get();
        DocumentSnapshot userSnapshot = futureUserSnapshot.get();
    
        if (userSnapshot.exists()) {
            User user = userSnapshot.toObject(User.class);
            int currentForumScore = user.getForumScore();
    
            // Increment the forumScore by 1
            int newForumScore = currentForumScore + 1;
            
            // Update the user's forumScore
            ApiFuture<WriteResult> futureUpdateUser = userRef.update("forumScore", newForumScore);
    
            
            WriteResult userUpdateResult = futureUpdateUser.get();
        
            } else {              
                throw new Exception("User does not exist with ID: " + comment.getUID());
            }         
            return postRef.get().get().getUpdateTime().toString();
    }
}

