import React from "react";
import SearchFormSuggestion from "../searchFormSuggestion/SearchFormSuggestion";

export default ({ suggestions }) => {
  return (
    <div className="dropdown is-active">
      <div className="dropdown-menu" role="menu">
        <div className="dropdown-content">
          {suggestions.map((suggestion, index) => {
            return <SearchFormSuggestion key={index} suggestion={suggestion} />;
          })}
        </div>
      </div>
    </div>
  );
};
