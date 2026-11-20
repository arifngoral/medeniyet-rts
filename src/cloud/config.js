// Firebase project of the optional cloud accounts (public web config; safe to ship).
// This fork's own project (medeniyet-rts, 2026-11-20). With an empty apiKey there would be no
// accounts at all (ACCOUNTS false): everybody plays as a guest with a local profile, multiplayer runs on room codes
// with unverified names, and friends / cloud saves / TP are hidden. To turn accounts on, create a free Firebase
// project (Google sign-in + Firestore), put its web config here and start the server with AEVUM_FIREBASE_PROJECT=<id>.
export const FIREBASE = Object.freeze({
  apiKey: 'AIzaSyDEy1nkk5N4WwVUs5qqplWMkhe_VxLWEjQ',
  authDomain: 'medeniyet-rts.firebaseapp.com',
  projectId: 'medeniyet-rts',
  storageBucket: 'medeniyet-rts.firebasestorage.app',
  messagingSenderId: '1029323065484',
  appId: '1:1029323065484:web:c6bff8eedd543537ca13a9',
});
export const ACCOUNTS = !!FIREBASE.apiKey;

export default FIREBASE;
