const mongoose = require("mongoose");

const schema = require("./aideSchema");
module.exports = mongoose.model("Aide", schema);
