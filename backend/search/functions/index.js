const functions = require("firebase-functions");
const admin = require("firebase-admin");
const algoliasearch = require("algoliasearch");

admin.initializeApp();
// const db = admin.firestore();

const algoliaClient = algoliasearch(
    "60IC04XR8A",
    "8766f78f6c717baf768884e6ca4d36a5",
);
const algoliaIndex = algoliaClient.initIndex("search_posts");

exports.syncPostsToAlgolia = functions.firestore
    .document("posts/{postId}")
    .onWrite(async (change, context) => {
      const postId = context.params.postId;
      const data = change.after.exists ? change.after.data() : null;

      if (data) {
      // If the document is created or updated, index it
        const objectToIndex = {
          objectID: postId,
          ...data,
        };
        await algoliaIndex.saveObject(objectToIndex);
      } else {
      // If the document is deleted, remove it from the index
        await algoliaIndex.deleteObject(postId);
      }
    });

