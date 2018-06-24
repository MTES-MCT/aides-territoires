const { GraphQLSchema, GraphQLObjectType } = require("graphql");
const schema = new GraphQLSchema({
  query: new GraphQLObjectType({
    name: "Query",
    fields: {
      ...require("./queries/aide"),
      ...require("./queries/user"),
      ...require("./queries/permission"),
      ...require("./queries/role"),
      ...require("./queries/menu"),
      ...require("./queries/enum")
    }
  }),
  mutation: new GraphQLObjectType({
    name: "Mutation",
    fields: {
      ...require("./mutations/email"),
      ...require("./mutations/aide"),
      ...require("./mutations/user")
    }
  })
});
module.exports = schema;
