import React from "react";
import SearchFormSuggestion from "./SearchFormSuggestion";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";

storiesOf("SearchFormSuggestion", module).add("SearchFormSuggestion", () => (
  <SearchFormSuggestion suggestion={{ text: "Nantes" }} />
));
