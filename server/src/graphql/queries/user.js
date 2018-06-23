const types = require("../types");
const { GraphQLID } = require("graphql");
const { getPermissionsFromRoles } = require("../../services/user");

// query pour le user actuellement connecté
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
        email: user.email,
        // on ajoute les permissions, qui peuvent être parfois utiles en front
        // pour afficher ou pas certains élements de l'UI
        // exemple : this.props.user.permission.includes('publish_aide') && <Component />
        // !DEPRECATED mauvaise pratique, certaines permissions ont besoin d'un argument,
        // !seule la fonction userHasPermission() permet une vérification complètement
        permissions: getPermissionsFromRoles(user.roles)
      };
      return result;
    }
  }
};
