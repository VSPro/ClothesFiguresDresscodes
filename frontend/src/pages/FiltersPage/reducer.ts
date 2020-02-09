const initialState = {
  filterItem: null
};

export default function filterPageReducer(state = initialState, action: any) {
  switch (action.type) {
    case "FILTER_ITEM":
      return { ...state, filterItem: action.payload };
    default:
      return state;
  }
}
