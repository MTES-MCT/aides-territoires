const mongoose = require("mongoose");

const schema = new mongoose.Schema(
  {
    email: {
      type: String,
      required: true
    },
    password: {
      type: String,
      required: true
    },
    name: {
      type: String,
      required: true
    },
    // les différents roles d'un utilisateur, un tableau des ids de roles
    // vor le fichier permissions.js
    roles: {
      type: Array,
      required: true
    }
  },
  { timestamps: true }
);

module.exports = mongoose.model("User", schema);
