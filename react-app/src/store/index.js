import { createStore, applyMiddleware, combineReducers } from "redux";
import { reducer as formReducer } from "redux-form";
import { composeWithDevTools } from "redux-devtools-extension";
import thunkMiddleware from "redux-thunk";

/*
function exampleReducer(state = {}, action) {
  switch (action.type) {
    case "SET_VISIBILITY_FILTER":
      return Object.assign({}, state, {
        visibilityFilter: action.filter
      });
    default:
      return state;
  }
}*/

const rootReducer = combineReducers({
  // ...your other reducers here
  // you have to pass formReducer under 'form' key,
  // for custom keys look up the docs for 'getFormState'
  form: formReducer
});

const store = createStore(
  rootReducer,
  {},
  composeWithDevTools(applyMiddleware(thunkMiddleware))
);

export default store;
