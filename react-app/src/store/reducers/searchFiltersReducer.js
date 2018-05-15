export default function searchFiltersReducer(state = {}, action) {
  switch (action.type) {
    case "SET_FILTER":
      return Object.assign({}, state, {
        visibilityFilter: action.filter
      });
    default:
      return state;
  }
}
