const mongoose = require("mongoose");

const schema = new mongoose.Schema(
  {
    name: String,
    description: String
  },
  { timestamps: true }
);

module.exports = mongoose.model("TypeDeTerritoire", schema);
