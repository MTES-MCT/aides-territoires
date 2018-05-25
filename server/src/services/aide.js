// la fonction principale du moteur de recherche pour le site
const AideModel = require("../mongoose/Aide");

const getAide = id => {
  return AideModel.findById(id);
};

const searchAides = async (filters, sort) => {
  const aides = await getAides({ ...filters });
  const resultsGroups = [];
  // on essaie d'abord d'apporter le résultat le plus localisé.
  // Si on a le code du périmètre d'application (code région, code département etc),
  // on créer un premier groupe de résultats avec les aides correspondantes
  if (filters.perimetreApplicationCode) {
    const aides = await getAides(filters);
    resultsGroups.push({
      count: Object.keys(aides).length,
      type: filters.perimetreApplicationType[0],
      label: filters.perimetreApplicationCode,
      aides: aides
    });
  }
  const response = {
    count: Object.keys(aides).length,
    results: resultsGroups
  };
  return response;
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
