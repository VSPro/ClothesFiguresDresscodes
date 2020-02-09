const initialState = {
  calculationItem: null
};

export default function figureCalculationPageReducer(state = initialState, action: any) {
  switch (action.type) {
    case "TEST_ITEM":
      return { ...state, calculationItem: action.payload };
    default:
      return state;
  }
}
