// la fonction principale du moteur de recherche pour le site
const AideModel = require("../mongoose/Aide");
const axios = require("axios");

// 01 : Guadeloupe
// 02 : Martinique
// 04 : La Réunion
// 06 : Mayotte
const codesGeoAPIOutreMer = ["01", "02", "03", "04", "05", "06"];

const getAide = id => {
  return AideModel.findById(id).populate("auteur", {
    name: 1,
    id: 1,
    roles: 1
  });
};

const searchAides = async (filters, { sort = null, context = null }) => {
  const groupesDeResultats = [];
  let aides = {};

  // si on a un code insee, on cherche d'abord des aides
  // sur les territoires spécifiés et alentour
  if (
    filters.typePerimetreInitialDeRecherche &&
    filters.codePerimetreInitialDeRecherche
  ) {
    //
    // * si on a demandé une COMMUNE en particulier :
    //
    if (
      filters.typePerimetreInitialDeRecherche === "commune" &&
      filters.codePerimetreInitialDeRecherche
    ) {
      // on créer un groupe de résultats pour les aides qu'on trouve
      // pour le territoire demandé
      let GroupeVosTerritoires = {
        label: "Pour votre territoire",
        type: "vos_territoires",
        aidesParTypeDeTerritoires: []
      };
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
      if (aides.length > 0) {
        GroupeVosTerritoires.aidesParTypeDeTerritoires.push({
          nombreAides: Object.keys(aides).length,
          type: "votre_departement",
          label: "Pour votre département",
          aides: aides
        });
      }

      // récupérer les aides de la région correspondante
      aides = await getAllAidesByTerritoire(
        "region",
        filters,
        geoApiResponse.data.codeRegion
      );
      if (aides.length > 0) {
        GroupeVosTerritoires.aidesParTypeDeTerritoires.push({
          nombreAides: Object.keys(aides).length,
          type: "votre_region",
          label: "Pour votre région",
          aides: aides
        });
      }

      // enregistrer les résultats
      if (GroupeVosTerritoires.aidesParTypeDeTerritoires.length > 0) {
        groupesDeResultats.push(GroupeVosTerritoires);
      }
    }

    //
    // * si on a demandé un DEPARTEMENT en particulier :
    //
    if (
      filters.typePerimetreInitialDeRecherche === "departement" &&
      filters.codePerimetreInitialDeRecherche
    ) {
      // on créer un groupe de résultats pour les aides qu'on trouve
      // pour le territoire demandé
      let GroupeVosTerritoires = {
        label: "Pour votre territoire",
        type: "vos_territoires",
        aidesParTypeDeTerritoires: []
      };
      // d'abord rechercher les aides pour cette commune
      aides = await getAllAidesByTerritoire(
        filters.typePerimetreInitialDeRecherche,
        filters,
        filters.codePerimetreInitialDeRecherche
      );
      if (aides.length > 0) {
        GroupeVosTerritoires.aidesParTypeDeTerritoires.push({
          nombreAides: Object.keys(aides).length,
          type: "departement_de_recherche",
          label: "Pour votre département",
          aides: aides
        });
      }

      // on récupère les données du département en question pour obtenir sa région
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
      if (aides.length > 0) {
        GroupeVosTerritoires.aidesParTypeDeTerritoires.push({
          nombreAides: Object.keys(aides).length,
          type: "departement_de_recherche_region",
          label: "Pour la région de votre déparement",
          aides: aides
        });
      }
      if (GroupeVosTerritoires.aidesParTypeDeTerritoires.length > 0) {
        groupesDeResultats.push(GroupeVosTerritoires);
      }
    }

    //
    // * si on a demandé une REGION en particulier :
    //
    if (
      filters.typePerimetreInitialDeRecherche === "region" &&
      filters.codePerimetreInitialDeRecherche
    ) {
      // on créer un groupe de résultats pour les aides qu'on trouve
      // pour le territoire demandé
      const GroupeVosTerritoires = {
        label: "Pour votre territoire",
        type: "vos_territoires",
        aidesParTypeDeTerritoires: []
      };
      // d'abord rechercher les aides pour cette région
      aides = await getAllAidesByTerritoire(
        filters.typePerimetreInitialDeRecherche,
        filters,
        filters.codePerimetreInitialDeRecherche
      );
      if (aides.length > 0) {
        GroupeVosTerritoires.aidesParTypeDeTerritoires.push({
          nombreAides: Object.keys(aides).length,
          type: "region_de_recherche",
          label: "Pour votre région",
          aides: aides
        });
      }
      // on récupère tous les dépatements du territoire en fonction
      // et on regarde si ils ont des aides !
      const geoApiResponse = await axios.get(
        `https://geo.api.gouv.fr/regions/${
          filters.codePerimetreInitialDeRecherche
        }/departements`
      );

      const promisesArray = await geoApiResponse.data.map(async departement => {
        aides = await getAllAidesByTerritoire(
          "departement",
          filters,
          departement.code
        );
        if (aides.length > 0) {
          GroupeVosTerritoires.aidesParTypeDeTerritoires.push({
            nombreAides: Object.keys(aides).length,
            type: "votre_region",
            label: "Pour votre région",
            aides: aides
          });
        }
        return aides;
      });
      // make sure all promises from our .map are resolved before continue
      await Promise.all(promisesArray);
      if (GroupeVosTerritoires.aidesParTypeDeTerritoires.length > 0) {
        // ajouter aux résultats de recherche
        groupesDeResultats.push(GroupeVosTerritoires);
      }
    }
  }
  //
  // les aides pour tous le territoires
  //
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

  // Ne pas afficher si on on est en train de chercher pour une région de métropole !
  if (
    !filters.codePerimetreInitialDeRecherche ||
    (filters.codePerimetreInitialDeRecherche &&
      codesGeoAPIOutreMer.includes(filters.codePerimetreInitialDeRecherche))
  ) {
    aides = await getAllAidesByTerritoire("outre_mer", filters);
    if (aides.length > 0) {
      GroupeTousLesTerritoires.aidesParTypeDeTerritoires.push({
        count: Object.keys(aides).length,
        type: "outre_mer",
        label: "Outre mer",
        aides: aides
      });
    }
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
    for (let territoire of groupeDeResultat.aidesParTypeDeTerritoires) {
      accumulator += territoire.aides.length;
    }
    return accumulator;
  }, 0);
  return count;
}

const getAllAidesByTerritoire = async (perimetreId, filters, code = null) => {
  if (
    filters.perimetreApplicationType &&
    !filters.perimetreApplicationType.includes(perimetreId)
  ) {
    return [];
  }
  const newFilters = { ...filters };
  delete newFilters.texte;
  if (perimetreId) {
    newFilters.perimetreApplicationType = [perimetreId];
    delete newFilters.typePerimetreInitialDeRecherche;
  }
  if (code) {
    newFilters.perimetreApplicationCode = code;
    delete newFilters.codePerimetreInitialDeRecherche;
  }

  // si on a d'abord affiché des aides localisées (présence de "codePerimetreInitialDeRecherche")
  // alors il n faut afficher ensuite QUE les aides qui ne sont pas localisées (perimetreApplicationCode vide),
  // sinon la même aide apparaitra à la fois en localisée et en non localisées
  if (code === null && filters.codePerimetreInitialDeRecherche) {
    delete newFilters.codePerimetreInitialDeRecherche;
    // s'assurer qu'on ne récupère que les aides qui s'appliquent partout
    // (et pas uniquement sur un territoire particulier), lorsque le code est null
    newFilters.perimetreApplicationCode = "";
  }

  const sort = [["dateEcheance", 1]];
  const aides = await getAides(newFilters, {
    sort,
    showExpired: false,
    showUnpublished: false
  });
  // on met les "null" ou "undefined" après les aides qui ont une date
  // d'échéance renseignée
  aides.sort(function(a, b) {
    if (a.dateEcheance && !b.dateEcheance) {
      return -1;
    }
    return 1;
  });
  return aides;
};

const getAides = (
  queryFilters = {},
  options = {
    context: null,
    showUnpublished: false,
    showExpired: true,
    sort: {}
  }
) => {
  const filters = { ...queryFilters };
  const { showUnpublished, showExpired, sort, context } = options;
  // contiendra nos différents groupes de "or"
  const $and = [];
  // convert ['operationnel', 'pre_operationnel', 'fonctionnement']
  // to {etape:{$in:["operationnel", "pre_operationnel", "fonctionnement"]}}
  for (let filter in filters) {
    if (Array.isArray(filters[filter])) {
      filters[filter] = { $in: filters[filter] };
    }
  }

  //  { "authors": /Alex/i },
  if (filters.motsCles) {
    filters.motsCles = { $regex: filters.motsCles, $options: "i" };
  }

  // * only show published aides by default
  if (showUnpublished === false) {
    filters.statusPublication = "published";
  }

  // convert dateEchance to mongodb filter
  // convert {dateEcheance:{lte:"Mon Jan 01 2018 00:00:00 GMT+0100"}} to
  // { dateEcheance: { $lte: "Mon Jan 01 2018 00:00:00 GMT+0100" } },
  // or([
  // { dateEcheance: null },
  // { dateEcheance: { $exists: false } }
  // ])
  const orDateEcheance = [];
  if (filters.dateEcheance) {
    orDateEcheance.push({
      dateEcheance: {
        ["$" + filters.dateEcheance.operator]: filters.dateEcheance.value
      }
    });
    // on veut aussi les dates nulles ou non-existantes
    orDateEcheance.push({ dateEcheance: null });
    orDateEcheance.push({ dateEcheance: { $exists: false } });
    // on récupère aussi les aides avec une date undefined (dans le doute)
    // orDateEcheance.push({ dateEcheance: { $type: 6 } });
  }
  // remove dateEchance sent by graphQL filter
  delete filters.dateEcheance;

  const query = AideModel.find(filters);
  query.sort(sort);
  // ne montrer que les aides dont la date de fin est supérieur à la date d'échéance
  // demandée par l'utilisateur. Autrement dit, ne montrer que les aides encore
  // existante à cette date.
  if (orDateEcheance.length > 0) {
    $and.push({ ["$or"]: orDateEcheance });
  }
  if (showExpired === false) {
    //ne pas afficher les aides qui sont expirées
    $and.push({
      ["$or"]: [
        { dateEcheance: { ["$gte"]: new Date() } },
        // il faut faire attentation à ne pas virer les aides avec les dates null, undefined
        // ou avec une clef non-définnies
        { dateEcheance: null },
        { dateEcheance: { $exists: false } }
        // on récupère aussi les aides avec une date undefined (dans le doute)
        // { dateEcheance: { $type: 6 } }
      ]
    });
  }
  if ($and.length > 0) {
    query.and($and);
  }
  // ajouter le champ auteur. N'ajouter le champ email que si l'utilisateur
  // connecté est l'admin ou un contributeur
  const auteurFields = { name: 1, roles: 1, id: 1 };
  if (
    context &&
    context.user &&
    (context.user.roles.includes("admin") ||
      context.user.roles.includes("contributeur"))
  ) {
    auteurFields.email = 1;
  }
  query.populate("auteur", auteurFields);
  return query;
};

module.exports = {
  getAide,
  getAides,
  searchAides
};
