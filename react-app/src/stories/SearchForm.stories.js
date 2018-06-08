import React from "react";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import SearchForm from "../components/search/SearchForm";
import { withInfo } from "@storybook/addon-info";

storiesOf("SearchForm", module).add(
  "SearchForm",
  withInfo(
    `Ce composant est conçu pour être couplé à SuuggestionList (ou autre) pour créer un autocomplete, les valeurs de ses champs doivent être entièrement controlé par un composant parent`
  )(() => (
    <div style={{ padding: "2rem" }}>
      <SearchForm
        value="la valeur de ce champ est passsée en props par le parent"
        onSubmit={action("form submitted")}
        onChange={action("input value changed")}
        placeholder="Entrez un code postal, une ville, un département ou une région"
      />
    </div>
  ))
);
