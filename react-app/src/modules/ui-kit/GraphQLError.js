import React from "react";

/**
 * Display details about encountered GraphQLErrors from react-apollo
 * Example :
 * <GraphQLError error={this.props.data.error} />;
 * @param {Object} error : this.props.data.error
 */
const GraphQLError = error => {
  const errors = error.error.networkError.result.errors
    .map(error => {
      return error.message;
    })
    .join(". ");
  return (
    <div style={{ padding: "2rem" }} className="message is-danger">
      {errors}
    </div>
  );
};

export default GraphQLError;
