import moment from "moment";
/**
 * Manipule les values du redux-form searchFilters
 * @param {*} state
 * @param {*} action
 */
export default function searchFiltersReducer(state = {}, action) {
  // <----- 'login' is name of form given to reduxForm()
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
                  year: state.values.dateEchanceYear,
                  month: state.values.dateEcheanceMonth
                })
              : null
        }
      };
      console.log(newState);
      return newState;
    default:
      return state;
  }
}
