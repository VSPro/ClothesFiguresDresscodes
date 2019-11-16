const initialState = {
    testItem: null
}

export default function rootReducer(state = initialState, action) {
    switch (action.type) {
        case 'TEST':
            return {...state, testItem: action.payload}
        default:
            return state
    }
}