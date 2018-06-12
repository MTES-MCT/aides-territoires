import React from "react";
import Text from "../../components/ui/finalFormBulma/Text";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import { Form, Field } from "react-final-form";

storiesOf("Final form & Bulma", module).add("Text", () => (
  <Form
    onSubmit={() => {
      action("submitted");
    }}
    render={({ handleSubmit, submitting, pristine, values, errors, form }) => (
      <form onSubmit={handleSubmit}>
        <Field name="Text" component={Text} label="Text" />
      </form>
    )}
  />
));
