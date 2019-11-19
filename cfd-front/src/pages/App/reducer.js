const initialState = {
    typeOfShape: ''
}

export default function appReducer(state = initialState, action) {
    switch (action.type) {
        case 'TYPE_OF_SHAPE':
            return {...state, typeOfShape: action.payload}
        default:
            return state
    }
}