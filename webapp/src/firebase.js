// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getStorage } from "firebase/storage";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyC59Y1OuO-vAxqqBDz_4MPwDwA5f3h-eGc",
  authDomain: "vipmusictoimage.firebaseapp.com",
  projectId: "vipmusictoimage",
  storageBucket: "vipmusictoimage.appspot.com",
  messagingSenderId: "820147520483",
  appId: "1:820147520483:web:6df8dcea339ac3d87ed6d6",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

export const FIREBASE_STORAGE = getStorage(app);
