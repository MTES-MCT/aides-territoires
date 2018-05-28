import queryString from "query-string";

/**
 * Determine if string looks like a postal code, suitable
 * to launch a search on postal code API.
 * You may call cleanPostalCode() to prepare string for this function
 *
 * @param {!string} string
 * @return {boolean} - true if string seems to be a postal code
 */
export const isPostalCode = string => {
  // check string contains only digit
  const isNumeric = /^\d+$/.test(string);
  if (isNumeric) {
    return true;
  }
  return false;
};

/**
 * Parfois le formulaire de filtres de recherche nous renvoie un objet
 * de la forme suivante, qui n'est pas considéré vide par notre code alors
 * qu'il signifie bien que rien n'est coché car type est vide.
 * {
 *    type:[]
 * }
 * la fonction le transforme en {}
 * @param {Object} filters
 */
export function cleanSearchFilters(filters) {
  Object.keys(filters).map(filterId => {
    if (filters[filterId] && filters[filterId].length === 0) {
      delete filters[filterId];
    }
  });
  return filters;
}

export function buildUrlParamsFromFilters(filters) {
  // je ne sais pas ce que fait cette clef data fait là, en attendant je la vire
  if (filters.data && Object.keys(filters.data).length === 0) {
    delete filters.data;
  }
  if (filters.perimetreAdditionalData) {
    delete filters.perimetreAdditionalData;
  }
  return queryString.stringify(filters);
}
