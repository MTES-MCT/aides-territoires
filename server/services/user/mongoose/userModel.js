const mongoose = require("mongoose");

const schema = require("./userSchema");
module.exports = mongoose.model("User", schema);
