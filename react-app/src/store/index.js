import { createStore, applyMiddleware, combineReducers } from "redux";
import { reducer as formReducer } from "redux-form";
import { composeWithDevTools } from "redux-devtools-extension";
import searchFiltersReducer from "./reducers/searchFiltersReducer";
import thunkMiddleware from "redux-thunk";
// import searchFiltersReducer from "reducers/searchFiltersReducer";

const rootReducer = combineReducers({
  // ...your other reducers here
  // you have to pass formReducer under 'form' key,
  // for custom keys look up the docs for 'getFormState'
  searchFilters: searchFiltersReducer,
  form: formReducer
});

const store = createStore(
  rootReducer,
  {},
  composeWithDevTools(applyMiddleware(thunkMiddleware))
);

export default store;
