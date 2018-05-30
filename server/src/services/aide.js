// la fonction principale du moteur de recherche pour le site
const AideModel = require("../mongoose/Aide");
const axios = require("axios");

const getAide = id => {
  return AideModel.findById(id);
};

/**
 * @param {*} filters
 * @param {*} sort
 */
const searchAides = async (filters, sort) => {
  const groupesDeResultats = [];
  let totalNombreAides = 0;
  let newFilters = {};
  let aides = {};

  // si on a un code insee, on cherche d'abord des aides
  // sur les territoires spécifiés et alentour
  if (
    filters.typePerimetreInitialDeRecherche &&
    filters.codePerimetreInitialDeRecherche
  ) {
    // on créer un groupe de résultats pour les aides qu'on trouve
    // pour le territoire demandé
    const GroupeVosTerritoires = {
      label: "Pour votre territoire",
      type: "vos_territoires",
      aidesParTypeDeTerritoires: []
    };

    //
    // si on a demandé une commune en particulier :
    //
    if (
      filters.typePerimetreInitialDeRecherche === "commune" &&
      filters.codePerimetreInitialDeRecherche
    ) {
      // d'abord rechercher les aides pour cette commune
      aides = await getAllAidesByTerritoire(
        filters.typePerimetreInitialDeRecherche,
        filters,
        filters.codePerimetreInitialDeRecherche
      );
      if (aides.length > 0) {
        GroupeVosTerritoires.aidesParTypeDeTerritoires.push({
          nombreAides: Object.keys(aides).length,
          type: "votre_commune",
          label: "Pour votre commune",
          aides: aides
        });
      }

      // récupérer toutes les données concernant la commune auprès de la Geo Api
      const geoApiResponse = await axios.get(
        `https://geo.api.gouv.fr/communes/${
          filters.codePerimetreInitialDeRecherche
        }`
      );
      // récupérer les aides du département correspondant
      aides = await getAllAidesByTerritoire(
        "departement",
        filters,
        geoApiResponse.data.codeDepartement
      );
      GroupeVosTerritoires.aidesParTypeDeTerritoires.push({
        nombreAides: Object.keys(aides).length,
        type: "votre_departement",
        label: "Pour votre département",
        aides: aides
      });

      // récupérer les aides de la région correspondante
      aides = await getAllAidesByTerritoire(
        "region",
        filters,
        geoApiResponse.data.codeRegion
      );
      GroupeVosTerritoires.aidesParTypeDeTerritoires.push({
        nombreAides: Object.keys(aides).length,
        type: "votre_region",
        label: "Pour votre région",
        aides: aides
      });

      // enregistrer les résultats
      groupesDeResultats.push(GroupeVosTerritoires);
    }

    //
    // si on a demandé un département en particulier :
    //
    if (
      filters.typePerimetreInitialDeRecherche === "departement" &&
      filters.codePerimetreInitialDeRecherche
    ) {
      // d'abord rechercher les aides pour cette commune
      aides = await getAllAidesByTerritoire(
        filters.typePerimetreInitialDeRecherche,
        filters,
        filters.codePerimetreInitialDeRecherche
      );
      if (aides.length > 0) {
        GroupeVosTerritoires.aidesParTypeDeTerritoires.push({
          nombreAides: Object.keys(aides).length,
          type: "votre_departement",
          label: "Pour votre département",
          aides: aides
        });

        // récupérer toutes les données concernant la commune auprès de la Geo Api
        const geoApiResponse = await axios.get(
          `https://geo.api.gouv.fr/departements/${
            filters.codePerimetreInitialDeRecherche
          }`
        );
        // récupérer les aides de la région correspondante
        aides = await getAllAidesByTerritoire(
          "region",
          filters,
          geoApiResponse.data.codeRegion
        );
        GroupeVosTerritoires.aidesParTypeDeTerritoires.push({
          nombreAides: Object.keys(aides).length,
          type: "votre_region",
          label: "Pour votre région",
          aides: aides
        });

        groupesDeResultats.push(GroupeVosTerritoires);
      }
    }
    //
    // si on a demandé une région en particulier :
    //
    if (
      filters.typePerimetreInitialDeRecherche === "region" &&
      filters.codePerimetreInitialDeRecherche
    ) {
      // d'abord rechercher les aides pour cette commune
      aides = await getAllAidesByTerritoire(
        filters.typePerimetreInitialDeRecherche,
        filters,
        filters.codePerimetreInitialDeRecherche
      );
      if (aides.length > 0) {
        GroupeVosTerritoires.aidesParTypeDeTerritoires.push({
          nombreAides: Object.keys(aides).length,
          type: "votre_region",
          label: "Pour votre région",
          aides: aides
        });
      }
      groupesDeResultats.push(GroupeVosTerritoires);
    }
  }

  // les aides pour tous le territoires
  const GroupeTousLesTerritoires = {
    label: "Pour tous les territoires",
    type: "tous_les_territoires",
    aidesParTypeDeTerritoires: []
  };

  // toutes les aides communales
  aides = await getAllAidesByTerritoire("commune", filters);
  if (aides.length > 0) {
    GroupeTousLesTerritoires.aidesParTypeDeTerritoires.push({
      nombreAides: Object.keys(aides).length,
      type: "commune",
      label: "Département",
      aides: aides
    });
  }

  // toutes les aides départementales

  aides = await getAllAidesByTerritoire("departement", filters);
  if (aides.length > 0) {
    GroupeTousLesTerritoires.aidesParTypeDeTerritoires.push({
      count: Object.keys(aides).length,
      type: "departement",
      label: "Département",
      aides: aides
    });
  }

  aides = await getAllAidesByTerritoire("region", filters);
  if (aides.length > 0) {
    GroupeTousLesTerritoires.aidesParTypeDeTerritoires.push({
      count: Object.keys(aides).length,
      type: "region",
      label: "Région",
      aides: aides
    });
  }
  aides = await getAllAidesByTerritoire("outre_mer", filters);
  if (aides.length > 0) {
    GroupeTousLesTerritoires.aidesParTypeDeTerritoires.push({
      count: Object.keys(aides).length,
      type: "outre_mer",
      label: "Outre mer",
      aides: aides
    });
  }

  if (aides.length > 0) {
    aides = await getAllAidesByTerritoire("metropole", filters);
    GroupeTousLesTerritoires.aidesParTypeDeTerritoires.push({
      count: Object.keys(aides).length,
      type: "metropole",
      label: "metropole",
      aides: aides
    });
  }

  // metropole + outre_mer

  aides = await getAllAidesByTerritoire("france", filters);
  if (aides.length > 0) {
    GroupeTousLesTerritoires.aidesParTypeDeTerritoires.push({
      count: Object.keys(aides).length,
      type: "france",
      label: "France",
      aides: aides
    });
  }

  aides = await getAllAidesByTerritoire("europe", filters);
  if (aides.length > 0) {
    GroupeTousLesTerritoires.aidesParTypeDeTerritoires.push({
      count: Object.keys(aides).length,
      type: "europe",
      label: "Europe",
      aides: aides
    });
  }

  groupesDeResultats.push(GroupeTousLesTerritoires);

  // toutes les aides régionales
  const response = {
    totalNombreAides: getTotalCountFromResultsGroups(groupesDeResultats),
    groupesDeResultats
  };
  return response;
};

function getTotalCountFromResultsGroups(groupesDeResultats) {
  const count = groupesDeResultats.reduce((accumulator, groupeDeResultat) => {
    for (territoire of groupeDeResultat.aidesParTypeDeTerritoires) {
      accumulator += territoire.aides.length;
    }
    return accumulator;
  }, 0);
  return count;
}

const getAllAidesByTerritoire = async (perimetreId, filters, code = null) => {
  const newFilters = { ...filters };
  delete newFilters.texte;
  if (perimetreId) {
    newFilters.perimetreApplicationType = perimetreId;
    delete newFilters.typePerimetreInitialDeRecherche;
  }
  if (code) {
    newFilters.perimetreApplicationCode = code;
    delete newFilters.codePerimetreInitialDeRecherche;
  }
  // enlever la localisation sur par code si ce
  // n'est n'est pas explicitement demandé
  if (code === null && newFilters.perimetreApplicationCode) {
    delete newFilters.perimetreApplicationCode;
  }

  console.log(JSON.stringify(newFilters, 0, 2));
  return await getAides(newFilters);
};

const getAides = (filters = {}, sort = {}) => {
  // convert all array to mongoose $in syntax
  // example : {etape:{$in:["operationnel", "pre_operationnel", "fonctionnement"]}}
  for (filter in filters) {
    if (Array.isArray(filters[filter])) {
      filters[filter] = { $in: filters[filter] };
    }
  }
  if (filters.motsCles) {
    filters.motsCles = { $regex: filters.motsCles, $options: "i" };
  }
  //  { "authors": /Alex/i },
  const query = AideModel.find(filters);
  query.sort(sort);
  return query;
};

module.exports = {
  getAide,
  getAides,
  searchAides
};
