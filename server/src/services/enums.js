const { GraphQLEnumType, GraphQLList } = require("graphql");
const logger = require("../services/logger");
const allEnumerations = require("../config/enums");

module.exports = {
  formatEnumForMongoose,
  formatEnumForGraphQL,
  getEnumByIdForMongoose,
  getEnumByIdForGraphQL
};

function getEnumById(enumId) {
  return allEnumerations.find(value => enumId === value.id);
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
function getEnumByIdForGraphQL(enumId, graphQLName) {
  const enumeration = getEnumById(enumId);
  const result = {
    name: graphQLName
  };
  enumeration.options.forEach(value => {
    result.values[value.id] = { value: value.id };
  });
  return new GraphQLEnumType(result);
}

function formatEnumForMongoose(enumType) {
  return enumType.map(r => r.value);
}

function formatEnumForGraphQL(graphQLName, enumType, multiple = true) {
  if (!enumType) {
    logger.error(
      "fonction formatEnumForGraphQL : L'énumération n'est pas définie pour " +
        graphQLName
    );
  }
  const graphQLType = {
    name: graphQLName,
    values: {}
  };
  enumType.map(data => {
    graphQLType.values[data.value] = {
      value: data.value,
      departement: data.label
    };
  });
  if (multiple) {
    return new GraphQLList(new GraphQLEnumType(graphQLType));
  }
  return new GraphQLEnumType(graphQLType);
}
