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
      type: [String],
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
      type: [String],
      enum: formatEnumForMongoose(enums.formeDeDiffusion)
    },
    formeDeDiffusionAutre: {
      type: String
    },
    destination: {
      type: [String],
      enum: formatEnumForMongoose(enums.destination)
    },
    destinationAutre: {
      type: String
    },
    thematiques: {
      type: [String],
      enum: formatEnumForMongoose(enums.thematiques)
    },
    dateDebut: {
      type: Date
    },
    dateEcheance: {
      type: Date
    },
    tauxSubvention: {
      type: String
    },
    contact: {
      type: String
    },
    status: {
      type: String,
      enum: formatEnumForMongoose(enums.status)
    },
    motsCles: {
      type: String
    },
    categorieParticuliere: {
      type: formatEnumForMongoose(enums.categorieParticuliere)
    },
    //  La demande peut être faite par un tiers pour le compte du porteur de projet
    // ou bien doit-elle être faite par le porteur de projet lui même
    demandeTiersPossible: {
      type: Boolean
    }
  },
  { timestamps: true }
);

module.exports = mongoose.model("Aide", schema);
