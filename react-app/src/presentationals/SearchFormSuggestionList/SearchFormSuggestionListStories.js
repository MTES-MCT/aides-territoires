import React from "react";
import SearchFormSuggestionList from "./SearchFormSuggestionList";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";

storiesOf("SearchFormSuggestionList", module).add(
  "SearchFormSuggestionList",
  () => (
    <SearchFormSuggestionList
      suggestions={[
        { text: "Nantes" },
        { text: "Meymac" },
        { text: "Limoges" }
      ]}
    />
  )
);
