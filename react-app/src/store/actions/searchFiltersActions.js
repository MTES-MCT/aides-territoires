/**
 * @param {Array} filters - un tableau d'objets représentant les valeurs des filtres
 * e.g : {
 *   etape:['pre_operationnel', 'operationnel'],
 *   type:['financement']
 * }
 */
export function setFilterValues(filters) {
  return {
    type: "SET_FILTERS_VALUES",
    filters
  };
}
