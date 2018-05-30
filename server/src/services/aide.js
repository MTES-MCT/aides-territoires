// la fonction principale du moteur de recherche pour le site
const AideModel = require("../mongoose/Aide");
const axios = require("axios");

const getAide = id => {
  return AideModel.findById(id);
};

const searchAides = async (filters, sort) => {
  const resultsGroups = [];
  let total = 0;
  let newFilters = {};
  let aides = {};

  // si on a un seul type de perimetre d'application (ex : Commune)
  // et un code insee (ex : 44000), on fait une recherche "localisée" en premier,
  // c'est à dire qu'on va d'abord présenter les résultats liés à la commune 44 spécifiquement.
  // Si on ne trouve rien, on va chercher des aides pour le département Loire Atlantique puis pour la région
  // Pays de la Loire
  //
  // Après cela on affichera ls aides pour toutes les communes,
  // puis tous les départements
  // puis toutes les régions
  // etc...

  // on essaie d'abord d'apporter les résultats le plus localisés si
  // un code est précié..
  // (code région, code département etc),
  // on créer un premier groupe de résultats avec les aides correspondantes)
  /*
  if (filters.perimetreApplicationCode) {
    if (filters.perimetreApplicationType === "commune") {
      // chercher d'abord pour la commune
      aides = await getAllAidesByTerritoire("commune", filters, true);
      resultsGroups.push({
        totalCount: Object.keys(aides).length,
        type: `votre_commune`,
        label: `pour votre commune`,
        aides: aides
      });
      const result = await axios.get(
        `https://geo.api.gouv.fr/departements/${
          filters.perimetreApplicationCode
        }`
      );
      console.log(result);
      // chercher pour le département de la commune. Il faut récupérer son code insee
    }
  }
  */

  // toutes les aides communales
  aides = await getAllAidesByTerritoire("commune", filters);
  resultsGroups.push({
    count: Object.keys(aides).length,
    type: "commune",
    label: "Département",
    aides: aides
  });

  // toutes les aides départementales

  aides = await getAllAidesByTerritoire("departement", filters);
  resultsGroups.push({
    count: Object.keys(aides).length,
    type: "departement",
    label: "Département",
    aides: aides
  });

  aides = await getAllAidesByTerritoire("region", filters);
  resultsGroups.push({
    count: Object.keys(aides).length,
    type: "region",
    label: "Région",
    aides: aides
  });

  aides = await getAllAidesByTerritoire("outre_mer", filters);
  resultsGroups.push({
    count: Object.keys(aides).length,
    type: "outre_mer",
    label: "Outre mer",
    aides: aides
  });

  aides = await getAllAidesByTerritoire("metropole", filters);
  resultsGroups.push({
    count: Object.keys(aides).length,
    type: "metropole",
    label: "metropole",
    aides: aides
  });

  // metropole + outre_mer

  aides = await getAllAidesByTerritoire("france", filters);
  resultsGroups.push({
    count: Object.keys(aides).length,
    type: "france",
    label: "France",
    aides: aides
  });

  aides = await getAllAidesByTerritoire("europe", filters);
  resultsGroups.push({
    count: Object.keys(aides).length,
    type: "europe",
    label: "Europe",
    aides: aides
  });

  // toutes les aides régionales
  const response = {
    totalCount: getTotalCountFromResultsGroups(resultsGroups),
    resultsGroups
  };
  return response;
};

function getTotalCountFromResultsGroups(resultsGroups) {
  const count = resultsGroups.reduce(
    (accumulator, resultGroup) => resultGroup.count + accumulator,
    0
  );
  return count;
}

const getAllAidesByTerritoire = async (
  perimetreId,
  filters,
  restrictByCode = false
) => {
  const newFilters = { ...filters };
  newFilters.perimetreApplicationType = perimetreId;
  // enlever la localisation sur par code si ce n'est pas explicitement demandé
  if (restrictByCode == false && newFilters.perimetreApplicationCode) {
    delete newFilters.perimetreApplicationCode;
  }
  return await getAides(newFilters);
};

const getAides = (filters = {}, sort = {}) => {
  // convert all array to mongoose $in syntax
  // example : {etape:{$in:["operationnel", "pre_operationnel", "fonctionnement"]}}
  for (filter in filters) {
    if (Array.isArray(filters[filter])) {
      filters[filter] = { $in: filters[filter] };
    }
  }
  if (filters.motsCles) {
    filters.motsCles =  { "$regex": filters.motsCles, "$options": "i" } 
  }
  //  { "authors": /Alex/i },
  console.log(JSON.stringify(filters, 0, 2))
  const query = AideModel.find(filters);
  query.sort(sort);
  return query;
};

module.exports = {
  getAide,
  getAides,
  searchAides
};
