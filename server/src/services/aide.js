// la fonction principale du moteur de recherche pour le site
const AideModel = require("../mongoose/Aide");

const getAide = id => {
  return AideModel.findById(id);
};

const searchAides = async (filters, sort) => {
  const aides = await getAides(filters);
  return {
    count: Object.keys(aides).length,
    results: [
      {
        count: Object.keys(aides).length,
        type: "abc",
        aides
      }
    ]
  };
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
