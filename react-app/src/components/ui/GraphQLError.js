import React from "react";

/**
 * Display details about encountered GraphQLErrors from react-apollo
 * Example :
 * <GraphQLError error={this.props.data.error} />;
 * @param {Object} error : this.props.data.error
 */
const GraphQLError = error => {
  let networkErrorMessage = "";
  let errorMessage = "";
  if (error && error.message) {
    errorMessage += error.error.message;
  }
  if (error.error.networkError && error.error.networkError.result) {
    networkErrorMessage = error.error.networkError.result.errors
      .map(error => {
        return error.message;
      })
      .join(". ");
  }
  errorMessage += ". " + networkErrorMessage;
  return (
    <div style={{ padding: "2rem" }} className="message is-danger">
      {errorMessage}
    </div>
  );
};

export default GraphQLError;
