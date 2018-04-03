export function parcours(state = [], action) {
  switch (action.type) {
    case "MY_ACTION":
      return [
        ...state,
        {
          user: action.author,
          text: action.comment
        }
      ];
    default:
      return state;
  }
}
