const mongoose = require("mongoose");

const { formatEnumForMongoose } = require("../services/enums");
const enums = require("../enums/aide");

const schema = new mongoose.Schema(
  {
    nom: String,
    description: String,
    criteresEligibilite: String,
    type: {
      type: String,
      enum: formatEnumForMongoose(enums.type)
    },
    perimetreApplicationType: {
      type: String,
      enum: formatEnumForMongoose(enums.perimetreApplicationType)
    },
    perimetreApplicationNom: {
      type: String
    },
    perimetreApplicationCode: {
      type: String
    },
    etape: {
      type: String,
      enum: formatEnumForMongoose(enums.etape)
    },
    statusPublication: {
      type: String,
      enum: formatEnumForMongoose(enums.statusPublication)
    },
    perimetreDiffusionType: {
      type: String,
      enum: formatEnumForMongoose(enums.perimetreDiffusionType)
    },
    perimetreDiffusionTypeAutre: {
      type: String
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
      enum: formatEnumForMongoose(enums.beneficiaires)
    },
    beneficiairesAutre: {
      type: String
    },
    formeDeDiffusion: {
      type: String,
      enum: formatEnumForMongoose(enums.formeDeDiffusion)
    },
    destination: {
      type: [String],
      enum: formatEnumForMongoose(enums.destination)
    }
  },
  { timestamps: true }
);

module.exports = mongoose.model("Aide", schema);
