const mongoose = require("mongoose");

const schema = new mongoose.Schema(
  {
    name: String,
    description: String,
    type: {
      type: String,
      enum: ["financement", "ingenierie", "autre"]
    },
    perimetreApplication: {
      type: String,
      enum: [
        "departement",
        "region",
        "france",
        "outre_mer",
        "metropole",
        "europe"
      ]
    },
    perimetreApplicationCode: {
      type: String
    },
    etape: {
      type: String,
      enum: ["pre-operationnel", "operationnel", "fonctionnement"]
    },
    status: {
      type: String,
      enum: ["draft", "published", "to_review"]
    },
    perimetreDiffusion: {
      type: String,
      enum: [
        "departement",
        "region",
        "france",
        "outre_mer",
        "metropole",
        "europe"
      ]
    },
    lien: {
      type: String
    },
    populationMin: {
      type: Number
    },
    populationMax: {
      type: Number
    },
    structurePorteuse: {
      type: String
    },
    beneficiaires: {
      type: [String],
      enum: ["commune", "EPCI", "entreprises", "associations"]
    }
  },
  { timestamps: true }
);

module.exports = mongoose.model("Aide", schema);
