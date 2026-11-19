// Firebase project of the optional cloud accounts (public web config; safe to ship).
// This fork ships WITHOUT one: the upstream game's project is not ours to use. With an empty apiKey there are no
// accounts at all (ACCOUNTS false): everybody plays as a guest with a local profile, multiplayer runs on room codes
// with unverified names, and friends / cloud saves / TP are hidden. To turn accounts on, create a free Firebase
// project (Google sign-in + Firestore), put its web config here and start the server with AEVUM_FIREBASE_PROJECT=<id>.
export const FIREBASE = Object.freeze({
  apiKey: '',
  authDomain: '',
  projectId: '',
  storageBucket: '',
  messagingSenderId: '',
  appId: '',
});
export const ACCOUNTS = !!FIREBASE.apiKey;

export default FIREBASE;
