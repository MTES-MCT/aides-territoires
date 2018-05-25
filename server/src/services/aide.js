// la fonction principale du moteur de recherche pour le site
const AideModel = require("../mongoose/Aide");

exports.getAide = id => {
  return AideModel.findById(id);
};

exports.searchAides = () => {
  return {
    count: 15,
    results: [
      {
        count: 12,
        type: "departement",
        aides: [
          {
            nom: "aide numéro 1"
          },
          {
            nom: "aide numéro 2"
          }
        ]
      },
      {
        type: "motClefs",
        count: 3,
        aides: [
          {
            nom: "aide numéro 3"
          },
          {
            nom: "aide numéro 4"
          }
        ]
      }
    ]
  };
};

exports.getAides = (filters = {}, sort = {}) => {
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
