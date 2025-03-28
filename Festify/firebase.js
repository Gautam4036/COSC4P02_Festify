// firebase.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-analytics.js";
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  onAuthStateChanged,
  signOut
} from "https://www.gstatic.com/firebasejs/11.2.0/firebase-auth.js";
import {
  getFirestore,
  doc,
  setDoc,
  getDoc,
  collection,
  getDocs,
  addDoc,
  query,
  where,
  updateDoc,
  deleteDoc,
  increment
} from "https://www.gstatic.com/firebasejs/11.2.0/firebase-firestore.js";
import { getStorage, ref, uploadBytes, getDownloadURL } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-storage.js";

// TODO: Replace with your Firebase project configuration
const firebaseConfig = {
  apiKey: "AIzaSyDe0ZCrJCtspANzB-is2Hh8gvkyvLNcRmA",
  authDomain: "fir-festify.firebaseapp.com",
  projectId: "fir-festify",
  storageBucket: "fir-festify.firebasestorage.app",
  messagingSenderId: "827425396836",
  appId: "1:827425396836:web:f3e9a41e9515e3f2b3a771",
  measurementId: "G-TNBDKZEDH1"
};

const app = initializeApp(firebaseConfig);

const analytics = getAnalytics(app);

const auth = getAuth(app);

const db = getFirestore(app);

const storage = getStorage(app);


/* ------------------------------
   Authentication Functions
------------------------------ */
export async function signUpUser(email, password) {
  const userCred = await createUserWithEmailAndPassword(auth, email, password);
  return userCred;
}

export async function signInUser(email, password) {
  const userCred = await signInWithEmailAndPassword(auth, email, password);
  return userCred;
}

export function signOutUser() {
  return signOut(auth);
}

export function onUserStateChanged(callback) {
  return onAuthStateChanged(auth, callback);
}

// Define an asynchronous function to save or update the user's profile data
export async function saveUserProfile(uid, profileData) {
  // Get the reference to the user document in the "users" collection by the provided uid
  const docRef = doc(db, "users", uid);

  // Set the profile data in the document, merging it with the existing data if any
  await setDoc(docRef, profileData, { merge: true });
}

// Function to save a ticket purchase to a user's account
export async function saveUserTicket(userId, ticketData) {
  try {
    // Create a reference to the tickets subcollection for this user
    const ticketsCollectionRef = collection(db, "users", userId, "tickets");
    
    // Add the ticket data with a timestamp
    const ticketWithTimestamp = {
      ...ticketData,
      purchasedAt: new Date(),
    };
    
    // Add the document to the tickets subcollection
    const docRef = await addDoc(ticketsCollectionRef, ticketWithTimestamp);
    console.log("Ticket saved with ID:", docRef.id);
    return docRef.id;
  } catch (error) {
    console.error("Error saving ticket:", error);
    throw error;
  }
}

// Function to fetch all tickets for a user
export async function getUserTickets(userId) {
  try {
    // Get reference to the user's tickets subcollection
    const ticketsCollectionRef = collection(db, "users", userId, "tickets");
    
    // Get all documents in the subcollection
    const querySnapshot = await getDocs(ticketsCollectionRef);
    
    // Map the documents to an array of ticket objects with their IDs
    const tickets = querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
    
    return tickets;
  } catch (error) {
    console.error("Error fetching user tickets:", error);
    return [];
  }
}

// Define an asynchronous function to get the profile of a user by their unique ID (uid)
export async function getUserProfile(uid) {
  // Get the reference to the user document in the "users" collection by the provided uid
  const docRef = doc(db, "users", uid);

  // Fetch the document snapshot from the database
  const snapshot = await getDoc(docRef);

  // Check if the document exists and return the data, otherwise return null
  return snapshot.exists() ? snapshot.data() : null;
}


// Define an asynchronous function to fetch all events
export async function fetchEvents() {
  try {
    console.log('Attempting to fetch events from Firestore...');
    // Get the reference to the "events" collection in the database
    const eventsCol = collection(db, "events");
    console.log('Events collection reference created');

    // Execute the query to get the events snapshot
    console.log('Executing getDocs query...');
    const eventsSnapshot = await getDocs(eventsCol);
    console.log('Query executed, snapshot received');

    // Map through the snapshot documents to create an array of event objects with their id and data
    const eventsList = eventsSnapshot.docs.map(doc => {
      const data = doc.data();
      console.log('Event data:', data);
      return { id: doc.id, ...data };
    });

    console.log('Total events fetched:', eventsList.length);
    // Return the list of events
    return eventsList;
  } catch (error) {
    // Log any errors that occur during the fetch operation
    console.error("Error fetching events:", error);
    console.error("Error details:", error.message);
    console.error("Error stack:", error.stack);

    // Return an empty array in case of an error
    return [];
  }
}


// Define an asynchronous function to fetch events for a specific user
export async function fetchUserEvents(userId) {
  try {
    // Get the reference to the "events" collection in the database
    const eventsCol = collection(db, "events");

    // Create a query to filter events where the organizerId matches the provided userId
    const q = query(eventsCol, where("organizerId", "==", userId));

    // Execute the query to get the events snapshot
    const eventsSnapshot = await getDocs(q);

    // Map through the snapshot documents to create an array of event objects with their id and data
    const eventsList = eventsSnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));

    // Return the list of events
    return eventsList;
  } catch (error) {
    // Log any errors that occur during the fetch operation
    console.error("Error fetching user events:", error);

    // Return an empty array in case of an error
    return [];
  }
}

// Define an asynchronous function to create a new event with the provided event data
export async function createNewEvent(eventData) {
  try {
    const docRef = await addDoc(collection(db, "events"), eventData);
    console.log("Event created with ID:", docRef.id);
    return docRef.id;
  } catch (error) {
    console.error("Error creating event:", error);
    throw error;
  }
}

// Define an asynchronous function to get event by ID
export async function getEventById(eventId) {
  try {
    const eventDoc = await getDoc(doc(db, "events", eventId));
    if (eventDoc.exists()) {
      return { id: eventDoc.id, ...eventDoc.data() };
    }
    return null;
  } catch (error) {
    console.error("Error getting event:", error);
    throw error;
  }
}
// Add this new function to handle image upload
export async function uploadEventImage(file) {
  try {
    const storageRef = ref(storage, 'event-images/' + Date.now() + '_' + file.name);
    const snapshot = await uploadBytes(storageRef, file);
    const downloadURL = await getDownloadURL(snapshot.ref);
    return downloadURL;
  } catch (error) {
    console.error("Error uploading image:", error);
    throw error;
  }
}

export async function updateTickets(eventId, amount) {
  try {
    const eventRef = doc(db, "events", eventId);
    await updateDoc(eventRef, { tickets: increment(-amount) });
    console.log(`Tickets decremented by ${amount} for event: ${eventId}`);
  } catch (error) {
    console.error(`Error decrementing tickets for event ${eventId}:`, error);
  }
}

export async function updateRevenue(eventId, payment){
  try {
    const docRef = doc(db, "events", eventId);
    const docSnap = await getDoc(docRef);

    if (docSnap.exists()) {
      const currentRevenue = docSnap.data().totalRevenue || 0; // Get existing revenue, default to 0
      const newRevenue = currentRevenue + payment; // Add new payment

      await updateDoc(docRef, {
        totalRevenue: newRevenue
      });
    }
  } catch (error) {
    console.error("Error updating revenue:", error);
  }
}

// Define an asynchronous function to update an event
export async function updateEvent(eventId, eventData) {
  try {
    const eventRef = doc(db, "events", eventId);
    await updateDoc(eventRef, eventData);
    console.log("Event updated successfully");
    return true;
  } catch (error) {
    console.error("Error updating event:", error);
    throw error;
  }
}

export async function deleteEvent(eventId) {
  try {
    const eventRef = doc(db, "events", eventId);
    await deleteDoc(eventRef);
    return true;
  } catch (error) {
    console.error("Error deleting event:", error);
    throw error;
  }
}

// Function to save feedback to the 'feedback' collection
export async function saveFeedback(feedbackData) {
  try {
    // Create a reference to the 'feedback' collection
    const feedbackCollectionRef = collection(db, "feedback");
    
    // Add the feedback data with a timestamp
    const feedbackWithTimestamp = {
      ...feedbackData,
      createdAt: new Date(),
    };
    
    // Add the document to the 'feedback' collection
    const docRef = await addDoc(feedbackCollectionRef, feedbackWithTimestamp);
    console.log("Feedback saved with ID:", docRef.id);
    return docRef.id;
  } catch (error) {
    console.error("Error saving feedback:", error);
    throw error;
  }
}

