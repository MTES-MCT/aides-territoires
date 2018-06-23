const mongoose = require("mongoose");
const Schema = mongoose.Schema;
const { getEnumByIdForMongoose } = require("../services/enums");

const schema = new mongoose.Schema(
  {
    auteur: { type: Schema.Types.ObjectId, ref: "User" },
    nom: String,
    description: String,
    criteresEligibilite: String,
    type: {
      type: String,
      enum: getEnumByIdForMongoose("type")
    },
    perimetreApplicationType: {
      type: String,
      enum: getEnumByIdForMongoose("perimetreApplicationType")
    },
    perimetreApplicationNom: {
      type: String
    },
    perimetreApplicationCode: {
      type: String
    },
    etape: {
      type: [String],
      enum: getEnumByIdForMongoose("etape")
    },
    statusPublication: {
      type: String,
      enum: getEnumByIdForMongoose("statusPublication")
    },
    perimetreDiffusionType: {
      type: String,
      enum: getEnumByIdForMongoose("perimetreDiffusionType")
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
      enum: getEnumByIdForMongoose("beneficiaires")
    },
    beneficiairesAutre: {
      type: String
    },
    formeDeDiffusion: {
      type: [String],
      enum: getEnumByIdForMongoose("formeDeDiffusion")
    },
    formeDeDiffusionAutre: {
      type: String
    },
    destination: {
      type: [String],
      enum: getEnumByIdForMongoose("destination")
    },
    destinationAutre: {
      type: String
    },
    thematiques: {
      type: [String],
      enum: getEnumByIdForMongoose("thematiques")
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
      enum: getEnumByIdForMongoose("status")
    },
    motsCles: {
      type: String
    },
    categorieParticuliere: {
      type: getEnumByIdForMongoose("categorieParticuliere")
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
