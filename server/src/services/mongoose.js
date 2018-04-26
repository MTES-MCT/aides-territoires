const mongoose = require("mongoose");
mongoose.Promise = global.Promise;
const db = mongoose.connection;
db.on("error", console.error.bind(console, "connection error:"));
db.once("open", () => console.log("Mongoose connection established"));
module.exports = mongoose.connect(process.env.MONGODB_URL);
