const mongoose = require("mongoose");

module.exports = new mongoose.Schema({
  name: { type: String, required: true },
  mail: { type: String, required: true },
  password: { type: String, required: true }
});
