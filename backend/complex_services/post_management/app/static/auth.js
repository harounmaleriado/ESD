

const loggedOutLinks = document.querySelectorAll(".logged-out")
const loggedInLinks = document.querySelectorAll(".logged-in")
const checklogin = (user)=>{
    if (user){
        loggedInLinks.forEach(item=>item.style.display="block")
        loggedOutLinks.forEach(item=>item.style.display="none")
    }else{
        loggedInLinks.forEach(item=>item.style.display="none")
        loggedOutLinks.forEach(item=>item.style.display="block");
    }
}

//listen for authentication changes
auth.onAuthStateChanged(user =>{
    if(user){
        console.log('User logged in: ', user)
        checklogin(user)
        document.getElementById("accountinfo").innerText=user.displayName
    }
    else{
        sessionStorage.removeItem('idToken');
        console.log('User logged out')
        checklogin()
    }
})

document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault();
    document.getElementById('Register').click() 

    
    
    const formData = {
        name: event.target.signupName.value,
        email: event.target.signupEmail.value,
        username: event.target.signupUsername.value,
        password: event.target.signupPassword.value
    };

    fetch('/newUserRegistration', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(async response => {
        if (!response.ok) {
            // Convert server response to text (assuming error message is in text format)
            const errorText = await response.text();
            // Throw error to be caught in catch block
            throw new Error(`Registration failed: ${errorText}`);
        }
    return response.json();
    })
    .then(data => {
        console.log('User registered:', data);
        alert('Registration successful!');

        //Reset the form here if registration is successful
        document.getElementById('signupForm').reset();
    })
    .catch(error => {
        console.error('Error:', error);
        alert(`Registration failed: ${error.message}`);

        // Reset the form
        document.getElementById('signupForm').reset();
    });
});
document.getElementById('signinForm').addEventListener('submit', function(event) {
    event.preventDefault();
    document.getElementById('Login').click()

    const email = signinForm['signinEmail'].value;
    const password = signinForm['signinPassword'].value;

    // Authenticate user
    firebase.auth().signInWithEmailAndPassword(email, password)
    .then((userCredential) => {
        // Get the ID Token
        idToken = userCredential.user.getIdToken();
        return idToken
    })
    .then((idToken) => {
        // Store the token 
        sessionStorage.setItem('idToken', idToken);
        // Reset the form here
        document.getElementById('signinForm').reset();
        console.log('User signed in and token stored.');
;
    })
    .catch((error) => {
        console.error("Error signing in", error);
        alert("Error signing in: " + error.message);  // Feedback to user
        document.getElementById('signinForm').reset(); // Reset form
    });

});


//signup
// const signupForm = document.querySelector('#signupForm')
// signupForm.addEventListener('submit',(e)=>{
//     e.preventDefault();
//     //get user info
//     const email=signupForm['signupEmail'].value;
//     const password=signupForm['signupPassword'].value;
//     //sign user up
//     firebase.auth().createUserWithEmailAndPassword(email,password).then(cred=>{
//         console.log(cred);
//         document.getElementById('Register').click();
//         signupForm.reset();
//     })
// })

//signout
const signout = document.querySelector('#signout');
signout.addEventListener("click",(e)=>{
    e.preventDefault();
    firebase.auth().signOut().then(()=>
    console.log("User signed out"))
})

//login
// const loginForm = document.querySelector("#signinForm")
// loginForm.addEventListener("submit",(e)=>{
//     e.preventDefault(); 
//     const email=loginForm['signinEmail'].value;
//     const password=loginForm['signinPassword'].value;

//     firebase.auth().signInWithEmailAndPassword(email,password).then(cred=>{
//         console.log(cred.user);
//         document.getElementById('Login').click();
//         loginForm.reset();
//     })
// })
