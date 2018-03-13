const graphql = require("graphql");
const aideModel = require("../mongoose/aideModel");

module.exports = {
  query: {
    // describe our field for this type of entity
    type: new graphql.GraphQLObjectType({
      name: "aideGet",
      fields: {
        id: { type: graphql.GraphQLString },
        title: { type: graphql.GraphQLString },
        description: { type: graphql.GraphQLString }
      }
    }),
    // `args` describes the arguments that our query accepts
    args: {
      id: { type: graphql.GraphQLString }
    },
    // data returned for this query
    resolve: function(_, { id }) {
      return {
        id: id,
        title: "aide de test",
        description: "description aide de test"
      };
    }
  },
  mutation: {
    // describe our field for this type of entity
    type: new graphql.GraphQLObjectType({
      name: "aideSave",
      fields: {
        id: { type: graphql.GraphQLString },
        title: { type: graphql.GraphQLString },
        description: { type: graphql.GraphQLString }
      }
    }),
    // `args` describes the arguments that our query accepts
    args: {
      title: { type: graphql.GraphQLString },
      description: { type: graphql.GraphQLString }
    },
    // data returned for this query
    resolve: function(_, { title, description }) {
      const aide = new aideModel({ title, description });
      return aide
        .save()
        .then(result => {
          return result;
        })
        .catch(e => console.log(e.message));
    }
  }
};
