import React from "react";
import Number from "../../components/ui/finalFormBulma/Number";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import { Form, Field } from "react-final-form";

storiesOf("Final form & Bulma", module).add("Number", () => (
  <Form
    onSubmit={() => {
      action("submitted");
    }}
    render={({ handleSubmit, submitting, pristine, values, errors, form }) => (
      <form onSubmit={handleSubmit}>
        <Field name="Number" component={Number} label="Number" />
      </form>
    )}
  />
));
