// maintient l'état des filtres actifs de la recherche
export default function searchFiltersReducer(state = {}, action) {
  switch (action.type) {
    case "SET_FILTERS_VALUES":
      return state;
    default:
      return state;
  }
}
