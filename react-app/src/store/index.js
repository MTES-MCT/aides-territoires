import { createStore, applyMiddleware, combineReducers } from "redux";
import { reducer as formReducer } from "redux-form";
import { composeWithDevTools } from "redux-devtools-extension";
import searchFiltersReducer from "./reducers/searchFiltersReducer";
import thunkMiddleware from "redux-thunk";

const rootReducer = combineReducers({
  // you have to pass formReducer under 'form' key for reduxForm
  // searchFiltersReducer permet de manipuler les données du formulaire "searchFilters"
  // pour ajuster la manière dont elles sont stockée dans le store.
  form: formReducer.plugin({
    searchFilters: searchFiltersReducer
  })
});

const store = createStore(
  rootReducer,
  {},
  composeWithDevTools(applyMiddleware(thunkMiddleware))
);

export default store;
