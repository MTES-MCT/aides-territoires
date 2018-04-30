const mongoose = require("mongoose");
const { enums, formatEnumForMongoose } = require("../enums");
console.log(formatEnumForMongoose(enums.AIDE_TYPES));

const schema = new mongoose.Schema(
  {
    nom: String,
    description: String,
    criteresEligibilite: String,
    type: {
      type: String,
      enum: formatEnumForMongoose(enums.AIDE_TYPES)
    },
    perimetreApplicationType: {
      type: String,
      enum: formatEnumForMongoose(enums.AIDE_PERIMETRE_APPLICATION_TYPES)
    },
    perimetreApplicationNom: {
      type: String
    },
    perimetreApplicationCode: {
      type: String
    },
    etape: {
      type: String,
      enum: formatEnumForMongoose(enums.AIDE_ETAPES)
    },
    statusPublication: {
      type: String,
      enum: formatEnumForMongoose(enums.AIDE_STATUS_PUBLICATION)
    },
    perimetreDiffusionType: {
      type: String,
      enum: formatEnumForMongoose(enums.AIDE_PERIMETRE_APPLICATION_TYPES)
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
      enum: formatEnumForMongoose(enums.AIDE_BENEFICIAIRES)
    }
  },
  { timestamps: true }
);

module.exports = mongoose.model("Aide", schema);
