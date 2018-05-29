// la fonction principale du moteur de recherche pour le site
const AideModel = require("../mongoose/Aide");

const getAide = id => {
  return AideModel.findById(id);
};

const searchAides = async (filters, sort) => {
  const resultsGroups = [];
  let total = 0;
  let newFilters = {};
  let aides = {};
  const territoires = filters.perimetreApplicationType
    ? filters.perimetreApplicationType
    : [];

  // on essaie d'abord d'apporter les résultats le plus localisés si
  // un code est précié..
  // (code région, code département etc),
  // on créer un premier groupe de résultats avec les aides correspondantes)
  /*
  if ((territoire && territoire === "departement") || territoire === "region") {
    if (filters.perimetreApplicationCode) {
      aides = await getAides(filters);
      resultsGroups.push({
        totalCount: Object.keys(aides).length,
        type: `votre_${territoire}`,
        label: `votre ${territoire}`,
        aides: aides
      });
    }
  }
  */

  // toutes les aides communales
  if (territoires.length === 0 || territoires.includes("commune")) {
    aides = await getAllAidesByTerritoire("commune", filters);
    resultsGroups.push({
      count: Object.keys(aides).length,
      type: "commune",
      label: "Département",
      aides: aides
    });
  }

  // toutes les aides départementales
  if (territoires.length === 0 || territoires.includes("departement")) {
    aides = await getAllAidesByTerritoire("departement", filters);
    resultsGroups.push({
      count: Object.keys(aides).length,
      type: "departement",
      label: "Département",
      aides: aides
    });
  }

  if (territoires.length === 0 || territoires.includes("region")) {
    aides = await getAllAidesByTerritoire("region", filters);
    resultsGroups.push({
      count: Object.keys(aides).length,
      type: "region",
      label: "Région",
      aides: aides
    });
  }

  if (territoires.length === 0 || territoires.includes("outre_mer")) {
    aides = await getAllAidesByTerritoire("outre_mer", filters);
    resultsGroups.push({
      count: Object.keys(aides).length,
      type: "outre_mer",
      label: "Outre mer",
      aides: aides
    });
  }

  if (territoires.length === 0 || territoires.includes("metropole")) {
    aides = await getAllAidesByTerritoire("metropole", filters);
    resultsGroups.push({
      count: Object.keys(aides).length,
      type: "metropole",
      label: "metropole",
      aides: aides
    });
  }

  // metropole + outre_mer
  if (territoires.length === 0 || territoires.includes("france")) {
    aides = await getAllAidesByTerritoire("france", filters);
    resultsGroups.push({
      count: Object.keys(aides).length,
      type: "france",
      label: "France",
      aides: aides
    });
  }

  if (territoires.length === 0 || territoires.includes("europe")) {
    aides = await getAllAidesByTerritoire("europe", filters);
    resultsGroups.push({
      count: Object.keys(aides).length,
      type: "europe",
      label: "Europe",
      aides: aides
    });
  }

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

const getAllAidesByTerritoire = async (perimetreId, filters) => {
  const newFilters = { ...filters };
  newFilters.perimetreApplicationType = [perimetreId];
  if (newFilters.perimetreApplicationCode) {
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
  const query = AideModel.find(filters);
  query.sort(sort);
  return query;
};

module.exports = {
  getAide,
  getAides,
  searchAides
};
