
// userProfile.js

function openUserProfile() {
    // Check if the user is signed in
    firebase.auth().onAuthStateChanged(function(user) {
        if (user) {
            // User is signed in, so now make a request for the user's data
            axios.get(`/api/users/uid/${user.uid}`)
                .then(response => {
                    // This is where you would update the HTML with the user's data
                    const userData = response.data;
                    document.getElementById('username').innerText = userData.username;
                    document.getElementById('email').innerText = userData.email;
                    document.getElementById('name').innerText = userData.name;
                    // ...and so on for other pieces of user data you want to display
                })
                .catch(error => {
                    console.error('Error fetching user data:', error);
                    // Handle errors here, such as redirecting to a login page or showing an error message
                });
        } else {
            // No user is signed in. Redirect to login page or show an error.
        }
    });
}
    

// Call the function when the window is loaded to ensure firebase is initialized
window.onload = function() {
    openUserProfile();
};


