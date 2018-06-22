const roles = [
  {
    id: "admin",
    label: "Admin",
    permissions: [
      "create_aide",
      "delete_any_aide",
      "edit_any_aide",
      "see_permissions_overview",
      "publish_aide"
    ]
  },
  {
    id: "contributeur",
    label: "Contributeur",
    permissions: ["create_aide", "delete_own_aide", "edit_own_aide"]
  }
];

const permissions = [
  {
    id: "create_aide",
    label: "Créer une aide"
  },
  {
    id: "edit_any_aide",
    label: "Editer n'importe quelle aide"
  },
  {
    id: "delete_any_aide",
    label: "Supprimer n'importe quelle aide"
  },
  {
    id: "delete_own_aide",
    label: "Supprimer uniquement ses propres aides",
    resolve: (user, args) => {
      const { aide } = args;
      if (!aide.auteur || !aide.auteur.id) return false;
      if (user.id === aide.auteur.id) {
        return true;
      }
      return false;
    }
  },
  {
    id: "edit_own_aide",
    label: "éditer uniquement ses propres aides",
    resolve: (user, args) => {
      const { aide } = args;
      if (!aide.auteur || !aide.auteur.id) return false;
      if (user.id === aide.auteur.id) {
        return true;
      }
      return false;
    }
  },
  { id: "see_permissions_overview", label: "voir les permissions et rôles" },
  { id: "publish_aide", label: "publier une aide" }
];

module.exports = { roles, permissions };
