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
 * Souvent le formulaire de filtres de recherche nous renvoie ce genre d'objet
 * qui n'est pas considéré comme vide en terme de code alors
 * qu'il signifie bien qu'ils sont vides côté métier
 * {
 *    type:[],
 *    etape: null
 * }
 * la fonction le transforme en {}
 * @param {Object} filters
 */
export function cleanSearchFilters(filters) {
  Object.keys(filters).forEach(filterId => {
    if (filters[filterId] && filters[filterId].length === 0) {
      delete filters[filterId];
    }
    if (filters[filterId] === null) {
      delete filters[filterId];
    }
  });
  // delete filters.perimetreAdditionalData for now, not handled by graphQL query
  if (filters.perimetreAdditionalData) {
    delete filters.perimetreAdditionalData;
  }
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
