const { GraphQLEnumType, GraphQLList } = require("graphql");
const logger = require("../services/logger");

exports.formatEnumForMongoose = enumType => {
  return enumType.map(r => r.value);
};

exports.formatEnumForGraphQL = (graphQLName, enumType, multiple = true) => {
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
};
