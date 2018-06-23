import moment from "moment";
/**
 * Manipule les values du redux-form searchFilters
 * @param {*} state
 * @param {*} action
 */
export default function searchFiltersReducer(state = {}, action) {
  switch (action.type) {
    case "@@redux-form/CHANGE":
      const newState = {
        ...state,
        values: {
          ...state.values,
          // la date d'échéance est construite en concaténant le champ année et le champ mois
          dateEcheance:
            state.values &&
            state.values.dateEcheanceYear &&
            state.values.dateEcheanceMonth
              ? moment({
                  year: state.values.dateEcheanceYear,
                  month: state.values.dateEcheanceMonth
                }).endOf("month")
              : null
        }
      };
      return newState;
    default:
      return state;
  }
}
