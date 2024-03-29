import firebase from 'firebase/compat/app'
import 'firebase/compat/firestore'
import { getStorage } from 'firebase/storage'

// import { initializeApp } from 'firebase/app';
// import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: 'AIzaSyD7hOJreemAPzn7XUesVX9NeyIYDE_zKbg',
  authDomain: 'wad2planet-a216a.firebaseapp.com',
  projectId: 'wad2planet-a216a',
  storageBucket: 'wad2planet-a216a.appspot.com',
  messagingSenderId: '322824509181',
  appId: '1:322824509181:web:2308f5b2f2b688e1bdd094',
  measurementId: 'G-BLBVZN1NMX'
}

const app = firebase.initializeApp(firebaseConfig)

const db = firebase.firestore()
export { db }
const storage = getStorage(app)
export { storage }
