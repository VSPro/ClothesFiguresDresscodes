type state = {
  paramsOfUser: {
    shape: string;
    sizeParams: {
      sizeOfChest: string;
      sizeOfHips: string;
      height: number;
      shoes: number;
    };
  };
  relevantPhotos: null | string[];
};

// TODO: уменьшить вложенность или призятять экшены к последним по уровню вложенность значениям
const initialState: state = {
  paramsOfUser: {
    shape: "",
    sizeParams: {
      sizeOfChest: "",
      sizeOfHips: "",
      height: 0,
      shoes: 0
    }
  },
  relevantPhotos: null
};

export default function appReducer(state = initialState, action: any) {
  switch (action.type) {
    case "PARAMS_OF_USER":
      return { ...state, paramsOfUser: action.payload };
    case "RELEVANT_PHOTOS":
      return { ...state, relevantPhotos: action.payload };
    default:
      return state;
  }
}
