import React from "react";
import Text from "../../components/ui/finalForm/Text";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import { Form, Field } from "react-final-form";
import { getDepartementsByName } from "../../lib/geoApi";

storiesOf("Final form", module).add("TextWithSuggestions", () => (
  <Form
    onSubmit={() => {
      action("submitted");
    }}
    render={({ handleSubmit, submitting, pristine, values, errors, form }) => (
      <form onSubmit={handleSubmit}>
        <Field
          name="perimetreApplicationCode"
          label="code territoire"
          component={Text}
          className="is-large"
          autocompleteCallback={getDepartementsByName}
        />
      </form>
    )}
  />
));
