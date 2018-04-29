const mongoose = require("mongoose");

const schema = new mongoose.Schema(
  {
    name: String,
    description: String,
    criteresEligibilite: String,
    type: {
      type: String,
      enum: ["financement", "ingenierie", "autre"]
    },
    perimetreApplicationType: {
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
    perimetreApplicationName: {
      type: String
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
      enum: ["draft", "published", "review_required", "trash"]
    },
    perimetreDiffusionType: {
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
