const types = require("../types");
const { GraphQLID } = require("graphql");
const { getPermissionsFromRoles } = require("../../services/user");

module.exports = {
  user: {
    type: types.User,
    args: {
      id: {
        type: GraphQLID
      }
    },
    resolve: (_, args, { user }) => {
      const result = {
        id: user.id,
        name: user.name,
        roles: user.roles,
        // on ajoute les permissions, qui seront utiles en front pour afficher ou
        // pas certains élements de l'UI
        // avec un code de type : if(user.permission.includes('publish_aide'))
        permissions: getPermissionsFromRoles(user.roles)
      };
      return result;
    }
  }
};
