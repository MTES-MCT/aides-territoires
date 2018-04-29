const mongoose = require("mongoose");
const {
  PERIMETRE_APPLICATION_TYPE,
  getEnumAsArray,
  getEnumAsGraphQLEnumType
} = require("../enumTypes");

const schema = new mongoose.Schema(
  {
    name: String,
    description: String,
    criteresEligibilite: String,
    type: {
      type: String,
      enum: getEnumAsArray("AIDE_TYPES")
    },
    perimetreApplicationType: {
      type: String,
      enum: getEnumAsArray("PERIMETRE_APPLICATION_TYPES")
    },
    perimetreApplicationName: {
      type: String
    },
    perimetreApplicationCode: {
      type: String
    },
    etape: {
      type: String,
      enum: getEnumAsArray("AIDE_ETAPES")
    },
    status: {
      type: String,
      enum: getEnumAsArray("AIDE_STATUS")
    },
    perimetreDiffusionType: {
      type: String,
      enum: getEnumAsArray("PERIMETRE_APPLICATION_TYPES")
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
      enum: getEnumAsArray("AIDE_BENEFICIAIRES")
    }
  },
  { timestamps: true }
);

module.exports = mongoose.model("Aide", schema);
