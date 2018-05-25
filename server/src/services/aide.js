// la fonction principale du moteur de recherche pour le site
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
