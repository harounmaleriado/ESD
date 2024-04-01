const admin = require('firebase-admin');
const serviceAccount = require('./Documents/ESD/backend/payment/techexchange-76048-firebase-adminsdk-r9jba-fed1cc73c1.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

module.exports = admin;
