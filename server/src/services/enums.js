const { GraphQLEnumType, GraphQLList } = require("graphql");
const logger = require("../services/logger");
const allEnumerations = require("../config/enums");

module.exports = {
  getEnumByIdForMongoose,
  getEnumByIdForGraphQL,
  getAllEnums
};

function getEnumById(enumId) {
  return allEnumerations.find(value => enumId === value.id);
}

function getAllEnums() {
  return allEnumerations;
}

/**
 * Formater nos enums pour mongoose, qui attend un array de la forme suivante :
 * ['Coffee', 'Tea'],
 * @param {String} enumId
 */
function getEnumByIdForMongoose(enumId) {
  const enumeration = getEnumById(enumId);
  const results = enumeration.values.map(value => value.id);
  return results;
}

/**
 * Formater nos enums pour Graphql, qui attend un object de la forme suivante :
 * var RGBType = new GraphQLEnumType({
 *   name: 'RGB',
 *   values: {
 *     RED: { value: 0 },
 *     GREEN: { value: 1 },
 *     BLUE: { value: 2 }
 *   }
 * });
 * @param {String} enumId
 * @param {String} graphQLName - attribut name unique GraphQ
 */
function getEnumByIdForGraphQL(graphQLName, enumId) {
  const enumeration = getEnumById(enumId);
  if (!enumeration) {
    throw new Error("aucune énumération trouvée pour l'id " + enumId);
  }
  const result = {
    name: graphQLName,
    values: {}
  };
  enumeration.values.forEach(value => {
    result.values[value.id] = { value: value.id };
  });
  return new GraphQLEnumType(result);
}
